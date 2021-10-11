#!/usr/bin/python3
import os
from functools import lru_cache
from time import sleep
import spidev

def sleep_ms(msecs):
    sleep(float(msecs) / 1000.0)

PAGE_SIZE=256

class spiflash(object):

    def __init__(self, bus, cs, mode=0, max_speed_hz=1000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, cs)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode

    def __del__(self):
        self.spi.close()

    def read_id(self):
        device_id = self.spi.xfer2([0x9F, 0x9F])[1:]
        return device_id

    def write_enable(self):
        self.spi.xfer2([0x06])
        sleep_ms(5)

    def erase_all(self):
        self.write_enable()
        self.spi.xfer2([0xC7])
        sleep_ms(10)
        self.wait_until_not_busy()

    def wait_until_not_busy(self):
        while (self.spi.xfer2([0x5, 0x5])[1] & 0x1) == 0x1:
            sleep_ms(5)

    def write_page_to_flash(self, page, bytes):
        self.write_enable()
        self.spi.xfer2([0x2, int(page / 256), page % 256, 0] + bytes)  # Write page 255
        sleep_ms(10)
        self.wait_until_not_busy()

    def get_page_from_flash(self, page):
        xfer=[0x3, int(page/256), page%256, 0] + [255 for _ in range(256)]
        return self.spi.xfer2(xfer)[4:]  # skip 4 first bytes (dummies)


    def write_pages(self, pages):
        for page_nbr, page_bytes in enumerate(pages):
            print(f"Writing page:{page_nbr}", end='\r')
            self.write_page_to_flash(page_nbr, page_bytes)

    def verify_pages(self, pages):
        for page_nbr, page_bytes in enumerate(pages):
            print(f"Verifying page:{page_nbr}", end='\r')
            bytes_flash = self.get_page_from_flash(page_nbr)
            if bytes_flash != page_bytes:
                print("Verify error:")
                print(bytes_flash)
                print(page_bytes)
                exit(1)


# 		pCSpiDev = new CSpi("HLD FPGA", "/dev/spidev1.3", cMode, 8, 8000, 0, FALSE, FALSE);		// active low cs
#       	cMode |= SPI_CPHA; // Phase, data is clocked out on falling_edge and sampled on rising_edge
# 	cMode |= SPI_CPOL; // Polarity => Clock is default high
# SPI_MODE_3		(SPI_CPOL|SPI_CPHA)

def get_pages_from_file(file_name:str, pad_last_page=0xff):
    pages=[]
    with open(file_name, 'rb') as f:
        while (chunk := f.read(PAGE_SIZE)) != b'':
            pages.append(list(chunk))
    # Fill last page to PAGE_SIZE
    last_page = pages[-1]
    for i in range(PAGE_SIZE - len(last_page)):
        last_page.append(pad_last_page)
    return pages


def setGPIO(pin, value):
    if not os.path.exists("/sys/class/gpio/gpio"+str(pin)):
        os.system('echo '+str(pin)+' > /sys/class/gpio/export')
        os.system('echo out > /sys/class/gpio/gpio'+str(pin)+'/direction')
    os.system('echo '+str(value)+ ' > /sys/class/gpio/gpio'+str(pin)+'/value')


def getGPIO(pin):
    if not os.path.exists("/sys/class/gpio/gpio"+str(pin)):
        os.system('echo '+str(pin)+' > /sys/class/gpio/export')
        os.system('echo in > /sys/class/gpio/gpio'+str(pin)+'/direction')
    gpiopin = "gpio%s" % (str(pin), )
    pin = open("/sys/class/gpio/"+gpiopin+"/value","r")
    value = pin.read()
    pin.close()
    return int(value)


@lru_cache(maxsize=None)
def reverse(byte):
    return int('{:08b}'.format(byte)[::-1], 2)

def reverse_bits(pages):
    reversed_pages=[]
    for page in pages:
        l = []
        for byte in page:
            l.append(reverse(byte))
        reversed_pages.append(l)
    return reversed_pages

'''
setlow /sys/class/gpio/gpio125/value
setlow /sys/class/gpio/gpio127/value
Info: File size: 162976 bytes.
sethigh /sys/class/gpio/gpio125/value
setlow /sys/class/gpio/gpio127/value
setlow /sys/class/gpio/gpio125/value
sethigh /sys/class/gpio/gpio127/value
'''
def enable_flash_mode():
    NCONFIG=125
    NCE=127
    setGPIO(NCONFIG, 0)
    setGPIO(NCE, 0)
    setGPIO(NCONFIG, 1)
    setGPIO(NCE, 0)
    setGPIO(NCONFIG, 0)
    setGPIO(NCE, 1)

def disable_flash_mode():
    NCONFIG=125
    NCE=127
    setGPIO(NCE, 0)
    setGPIO(NCONFIG, 1)


def test():
    chip = spiflash(bus=1, cs=3, mode=3, max_speed_hz=12000000)
    print("ID:", chip.read_id())
    print("Enable flash mode")
    enable_flash_mode()
    sleep_ms(100)

    print("ID:", chip.read_id())

    print("Erasing")
    chip.erase_all()
    pages = get_pages_from_file('hld_fpga_0400_0001.rpd')
    reverse_pages = reverse_bits(pages)
    chip.write_pages(reverse_pages)

    print('\nVerify!')
    chip.verify_pages(reverse_pages)

    disable_flash_mode()
    print("ID:", chip.read_id())
    print('\nSuccess!')




