#!/usr/bin/python3
import os
from functools import lru_cache
from time import sleep

import typer
from pathlib import Path

import spidev

def sleep_ms(msecs):
    sleep(float(msecs) / 1000.0)

def spibus_from_spipath(spi:str) -> [int,int]:
    spi_bus = spi.split(".")[0][-1]
    device = spi.split(".")[1]
    return int(spi_bus), int(device)



class SpiActiveFlash(object):
    def __init__(self, spi_path:str, mode:int=0, max_speed_hz:int=1000000):
        spi_bus, spi_bus_cs = spibus_from_spipath(spi_path)
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_bus_cs)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode
        self.spi.bits_per_word=8
        self.spi.xfer2([0xb7])  # Enter 4-byte mode

    def __del__(self):
        self.spi.close()

    def read_id(self) -> [int]:
        device_id = self.spi.xfer2([0x9F, 0x9F ,0 ,0 ,0 ,0 ,0 ,0 ,0,0 ,0 ,0 ,0])[1:]
        return device_id

    def write_enable(self) -> None:
        self.spi.xfer2([0x06])

    def bulk_erase(self) -> None:
        print("Bulk erase start")
        self.spi.xfer2([0x06]) # Write enable
        self.spi.xfer2([0xC4,0,0,0,0]) #4 dummy bytes must be sent, otherwise no bulk erase will start.
        sleep_ms(10) # Prob not needed
        print("Waiting for bulk erase to finnish")
        while (self.spi.xfer2([0x70, 0x70])[1] & 128) == 0:
            #Read status register bit 7 Program or erase controller 0 = Busy 1 = Ready
            sleep_ms(1)
        print("Bulk erase done")

    def wait_until_not_busy(self) -> None:
        while (self.spi.xfer2([0x5, 0x5])[1] & 0x1) == 0x1:
            pass

    def write_page_to_flash(self, page:int, bytes:[int]) -> None:
        self.write_enable()
        self.spi.xfer2([0x2, int(page / (256*256)), int(page / 256), page % 256, 0] + bytes)  # Write page 255
        self.wait_until_not_busy()

    def get_page_from_flash(self, page:int) -> [int]:
        xfer=[0x3, int(page / (256*256)), int(page/256), page%256, 0] + [255 for _ in range(256)]
        return self.spi.xfer2(xfer)[5:]  # skip 4 first bytes (dummies)

    def write_pages(self, pages:[[int]]) -> int:
        for page_nbr, page_data in enumerate(pages):
            if not page_nbr%10:
                perc = int(100*(page_nbr/(len(pages)-1)))
                print(f"Writing page:{page_nbr:03}/{len(pages)-1} {perc}% ", end='')
            self.write_page_to_flash(page_nbr, page_data)
            if page_nbr%2000==0:
                print(f"Fast verify page:{page_nbr}  ", end='')
                bytes_flash = self.get_page_from_flash(page_nbr)
                if bytes_flash != page_data:
                    print("\nVerify error:")
                    print("Flash:", bytes_flash)
                    print("File:", page_data)
                    return 1
                print("   OK!!!", end='')
            print("", end='\r')
        return 0

    def verify_pages(self, pages:[[int]]) -> int:
        for page_nbr, page_data in enumerate(pages):
            print(f"Verifying page:{page_nbr}/{len(pages)-1}", end='\r')
            bytes_flash = self.get_page_from_flash(page_nbr)
            if bytes_flash != page_data:
                print("Verify error:")
                print("Flash:", bytes_flash)
                print("File:", page_data)
                return 1
        print("\nVerify OK!")
        return 0


def get_pages_from_file(file_name:Path, page_size:int=256, pad_last_page=0xff, reverse_bit_order: bool = False) -> [[int]]:
    pages=[]
    print("Reading flashfile")
    with open(file_name.absolute(), 'rb') as f:
        while (chunk := f.read(page_size)) != b'':
            pages.append(list(chunk))
    # Fill last page to PAGE_SIZE
    last_page = pages[-1]
    for i in range(page_size - len(last_page)):
        last_page.append(pad_last_page)
    if reverse_bit_order:
        print("Reversing bitorder")
        pages = reverse_bits(pages)
    print("Done reading flashfile")
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

def reverse_bits(pages:[[int]]) -> [[int]]:
    reversed_pages=[]
    for page in pages:
        l = []
        for byte in page:
            l.append(reverse(byte))
        reversed_pages.append(l)
    return reversed_pages





app = typer.Typer()

@app.command()
def erase_m252g(spi_path='/dev/spidev0.1', spi_mode:int=3, speed_hz:int=12000000):
    '''
        Performs bulk erase. Checks first page is 255 only.
    '''
    chip = SpiActiveFlash(spi_path, mode=spi_mode, max_speed_hz=speed_hz)
    chip.bulk_erase()
    page0_bytes = chip.get_page_from_flash(0)
    print("Checking page:0 contains only 255")
    if len(set(page0_bytes)) != 1 or page0_bytes[0]!=255:
        print(f"Erase didn't work.\nPage contains:{page0_bytes}")
        raise typer.Exit(code=1)
    print("Erase OK!")

@app.command()
def flash_m252g(spi_path='/dev/spidev0.1', spi_mode:int=3, speed_hz:int=12000000, image_filename:Path=Path('/home/root/firmware/binary/vp-fpga/vp-fpga_mux_spi_ti_flash.bin'), reverse_bit_order:bool=False):
    '''
        Flash image_filename to flash, NO erase
    '''
    chip = SpiActiveFlash(spi_path, mode=spi_mode, max_speed_hz=speed_hz)
    pages = get_pages_from_file(image_filename, page_size=256, reverse_bit_order=reverse_bit_order)
    exit_code = chip.write_pages(pages)
    if exit_code!=0:
        raise typer.Exit(code=1)
    print("Flash OK")

@app.command()
def chip_id(spi_path='/dev/spidev0.1', spi_mode:int=3, speed_hz:int=12000000):
    '''
    Displays info about the chip. If 0xff there is no connection over spi
    2 Memory type (1 byte) BAh = 3V Manufacturer BBh = 1.8V
    3 Memory capacity (1 byte) 22h = 2Gb 21h = 1Gb 20h = 512Mb 19h = 256Mb 18h = 128Mb 17h = 64Mb
    '''
    chip = SpiActiveFlash(spi_path, mode=spi_mode, max_speed_hz=speed_hz)
    id = chip.read_id()
    print("Raw:", id)
    print(f"Chip ID:{id[0]:02x}")
    print(f"Mem type:{id[1]:02x}")
    print(f"Size:{id[2]:02x}")

@app.command()
def dump_m252g(spi_path='/dev/spidev0.1', spi_mode:int=3, speed_hz:int=12000000, reverse_bit_order:bool=False, number_of_pages:int=99999):
    '''
        Dump flash to stdout. Pipe to file for saving data. Can be used with reverse_bit_order.
    '''
    chip = SpiActiveFlash(spi_path, mode=spi_mode, max_speed_hz=speed_hz)
    pages = []
    for page in range(0, number_of_pages):
        pages.append(chip.get_page_from_flash(page))
    if reverse_bit_order:
        pages = reverse_bits(pages)
    for page in pages:
        os.write(1, bytearray(page))

@app.command()
def verify_m252g(spi_path='/dev/spidev0.1', spi_mode:int=3, speed_hz:int=12000000, image_filename:Path=Path('/home/root/firmware/binary/vp-fpga/vp-fpga_mux_spi_ti_flash.bin'), reverse_bit_order:bool=False):
    '''
        Verify a flashed image with a image_filename. Exitcode 1 if not pass
    '''
    chip = SpiActiveFlash(spi_path, mode=spi_mode, max_speed_hz=speed_hz)
    pages = get_pages_from_file(image_filename, page_size=256, reverse_bit_order=reverse_bit_order)
    exit_code = chip.verify_pages(pages)
    if exit_code!=0:
        raise typer.Exit(code=1)

@app.command()
def read_page_m252g(spi_path='/dev/spidev0.1', spi_mode:int=3, speed_hz:int=12000000, page_number:int=0):
    '''
        Read one page from flash.
    '''
    chip = SpiActiveFlash(spi_path, mode=spi_mode, max_speed_hz=speed_hz)
    print(chip.get_page_from_flash(page_number))


@app.command()
def test_max_spi_speed(spi_path='/dev/spidev0.1', spi_mode:int=3):
    '''
    Test the highest speed possible without errors. Starting on 1000Hz to 25MHz in 1000hz steps
    '''
    start, stop, step = 1000, 25000000, 1000
    for i in range(10):
        for speed_hz in range(start, stop, step):
            print(f"Testing {speed_hz} Hz", end='\r')
            chip = SpiActiveFlash(spi_path, mode=spi_mode, max_speed_hz=speed_hz)
            id = chip.read_id()[0]
            del chip
            if id!=0x20:
                print(f"max speed:{speed_hz-step} Hz        ")
                break


if __name__ == "__main__":
    app()


