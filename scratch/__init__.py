import os
from functools import lru_cache
from pathlib import Path
from time import sleep

import spidev

def sleep_ms(msecs):
    sleep(float(msecs) / 1000.0)

class SpiActiveFlash(object):
    def __init__(self, bus: int, bus_cs: int, mode:int=0, max_speed_hz:int=1000000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, bus_cs)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode
        self.spi.xfer2([0xb7])  # Enter 4-byte mode


    def __del__(self):
        self.spi.close()

    def read_id(self) -> int:
        device_id = self.spi.xfer2([0x9F, 0x9F])[1:][0]
        return device_id

    def write_enable(self) -> None:
        self.spi.xfer2([0x06])
        sleep_ms(1)

    def erase_all_start(self) -> None:
        print("Bulk erase start")
        self.spi.xfer2([0x06]) # Write enable
        self.spi.xfer2([0xC4,0,0,0,0]) #4 dummy bytes must be sent, otherwise no bulk erase will start.
        sleep_ms(10) # Prob not needed


    def erase_wait_until_done(self):
        print("Waiting for bulk erase to finnish")
        while (self.spi.xfer2([0x70, 0x70])[1] & 128) == 0:
            #Read status register bit 7 Program or erase controller 0 = Busy 1 = Ready
            sleep_ms(1)
        print("Bulk erase done")
        sleep_ms(1000)

    def wait_until_not_busy(self) -> None:
        while (self.spi.xfer2([0x5, 0x5])[1] & 0x1) == 0x1:
            sleep_ms(1)

    def write_page_to_flash(self, page:int, bytes:[int]) -> None:
        self.write_enable()
        self.spi.xfer2([0x2, int(page / (256*256)), int(page / 256), page % 256, 0] + bytes)  # Write page 255
        self.wait_until_not_busy()

    def get_page_from_flash(self, page:int) -> [int]:
        xfer=[0x3, int(page / (256*256)), int(page/256), page%256, 0] + [255 for _ in range(256)]
        return self.spi.xfer2(xfer)[5:]  # skip 4 first bytes (dummies)

    def write_pages(self, pages:[[int]]) -> None:
        for page_nbr, page_bytes in enumerate(pages):
            if not page_nbr%10:
                perc = int(100*(page_nbr/(len(pages)-1)))
                print(f"Writing page:{page_nbr:03}/{len(pages)-1} {perc}%", end='\r')
            self.write_page_to_flash(page_nbr, page_bytes)

    def verify_pages(self, pages:[[int]]) -> int:
        for page_nbr, page_data in enumerate(pages):
            print(f"Verifying page:{page_nbr:03}/{len(pages)-1}", end='\r')
            bytes_flash = self.get_page_from_flash(page_nbr)
            if bytes_flash != page_data:
                print("Verify error:")
                print("Flash:", bytes_flash)
                print("File:", page_data)
                return 1
        print("Verify OK!")
        return 0


def get_pages_from_file(file_name:Path, page_size:int=256, pad_last_page=0xff) -> [[int]]:
    pages=[]
    with open(file_name.absolute(), 'rb') as f:
        while (chunk := f.read(page_size)) != b'':
            pages.append(list(chunk))
    # Fill last page to PAGE_SIZE
    last_page = pages[-1]
    for i in range(page_size - len(last_page)):
        last_page.append(pad_last_page)
    return pages


def setGPIO(pin:int, value:int) -> None:
    if not os.path.exists("/sys/class/gpio/gpio"+str(pin)):
        os.system('echo '+str(pin)+' > /sys/class/gpio/export')
        os.system('echo out > /sys/class/gpio/gpio'+str(pin)+'/direction')
    os.system('echo '+str(value)+ ' > /sys/class/gpio/gpio'+str(pin)+'/value')


def getGPIO(pin:int) -> int:
    if not os.path.exists("/sys/class/gpio/gpio"+str(pin)):
        os.system('echo '+str(pin)+' > /sys/class/gpio/export')
        os.system('echo in > /sys/class/gpio/gpio'+str(pin)+'/direction')
    gpiopin = "gpio%s" % (str(pin), )
    pin = open("/sys/class/gpio/"+gpiopin+"/value","r")
    value = pin.read()
    pin.close()
    return int(value)


@lru_cache(maxsize=None)
def reverse(byte) -> int:
    return int('{:08b}'.format(byte)[::-1], 2)


def reverse_bit_order(pages:[[int]]) -> [[int]]:
    reversed_pages=[]
    for page in pages:
        l = []
        for byte in page:
            l.append(reverse(byte))
        reversed_pages.append(l)
    return reversed_pages

