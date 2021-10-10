#!/usr/bin/python3

WREN = 6
WRDI = 4
RDSR = 5
RDSR2 = 0x35
WRSR = 1
READ = 3
WRITE = 2
SECTOR_ERASE = 0xD8
# CHIP_ERASE = 0xC7
CHIP_ERASE = 0xC7

READ_FLAG_STATUS_REGISTER = 0x70

import sys, struct, os, collections

from array import array
import random

from time import sleep
import spidev
from datetime import datetime
from importlib import reload

def sleep_ms(msecs):
    sleep(float(msecs) / 1000.0)


class spiflash(object):

    def __init__(self, bus, cs, mode=0, max_speed_hz=1000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, cs)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode

    def __del__(self):
        try:
            self.spi.close()
        except:
            pass

    # reads ----------------------------------------------------------------------------------
    def read_id(self):
        # device_id = self.spi.xfer2([0x9E,0x9F])[1]
        #AS_CHECK_SILICON_ID			0x9F
        #device_id = self.spi.xfer2([0x9E, 0x9F, 0])[1:]
        device_id = self.spi.xfer2([0x9F, 0x9F])[1:]
        return device_id

    def read_status(self):
        statreg = self.spi.xfer2([RDSR, RDSR])[1]
        # statreg2 = self.spi.xfer2([RDSR2,RDSR2])[1]
        return statreg

    def read_flag_status(self):
        statreg = self.spi.xfer2([READ_FLAG_STATUS_REGISTER, READ_FLAG_STATUS_REGISTER])[1]
        # statreg2 = self.spi.xfer2([RDSR2,RDSR2])[1]
        return statreg

    def read_page_old(self, byte_1, byte_2):
        xfer = [READ, 0, byte_2, byte_1] + [255 for _ in range(256)]  # command + 256 dummies
        return self.spi.xfer2(xfer)[4:]  # skip 4 first bytes (dummies)

    # writes ----------------------------------------------------------------------------------
    def write_enable(self):
        self.spi.xfer2([WREN])
        sleep_ms(5)

    def write_disable(self):
        self.spi.xfer2([WRDI])
        sleep_ms(5)

    def write_status(self, s1, s2):
        self.write_enable()

        self.spi.xfer2([WRSR, s1, s2])
        sleep_ms(10)

        self.wait_until_not_busy()

    def write_page_old(self, byte_1, byte_2, page):
        self.write_enable()

        # print self.read_status()

        xfer = [WRITE, 0, byte_2, byte_1] + page[:256]
        self.spi.xfer2(xfer)
        sleep_ms(10)

        self.wait_until_not_busy()

    def write_and_verify_page(self, addr1, addr2, page):
        self.write_page_to_flash(addr1, addr2, page)
        return self.read_page(addr1, addr2)[:256] == page[:256]

    # erases ----------------------------------------------------------------------------------
    def erase_sector(self, addr1, addr2):
        self.write_enable()

        xfer = [SECTOR_ERASE, 0, addr2, addr1]
        self.spi.xfer2(xfer)
        sleep_ms(10)

        self.wait_until_not_busy()

    def erase_all(self):
        self.write_enable()

        self.spi.xfer2([CHIP_ERASE])
        sleep_ms(10)

        self.wait_until_not_busy()

    # misc ----------------------------------------------------------------------------------
    def wait_until_not_busy(self):
        statreg = 0x1;
        while (statreg & 0x1) == 0x1:
            # Wait for the chip.
            statreg = self.spi.xfer2([RDSR, RDSR])[1]
            # print "%r \tRead %X" % (datetime.now(), statreg)
            sleep_ms(5)

    # helpers -------------------------------------------------------------------------------
    def print_status(self, status):
        print("status %s %s" % (bin(status[1])[2:].zfill(8), bin(status[0])[2:].zfill(8)))

    def print_page(self, page):
        s = ""
        for row in range(16):
            for col in range(16):
                s += "%02X " % page[row * 16 + col]
            s += "\n"
        print(s)

    def fill_memory(self, start_page, stop_page):
        for page in range(start_page, stop_page):
            self.write_page_to_flash(page, [x + page for x in range(256)])

    def write_page_to_flash(self, page, bytes):
        self.write_enable()
        self.spi.xfer2([6])  # WREN  Write enable
        self.spi.xfer2([0x2, int(page / 256), page % 256, 0] + bytes)  # Write page 255
        sleep_ms(10)
        self.wait_until_not_busy()

    def read_memory(self, start_page, stop_page):
        for page in range(start_page, stop_page):
            print(f'Page:{page}')
            bytes = self.spi.xfer2([0x3, int(page/256), page%256, 0] + [255 for _ in range(256)])
            print(f'{bytes}')

    def get_page_from_flash(self, page):
        xfer=[0x3, int(page/256), page%256, 0] + [255 for _ in range(256)]
        return self.spi.xfer2(xfer)[4:]  # skip 4 first bytes (dummies)


# TESTS -------------------------------------------------------------------

# 		pCSpiDev = new CSpi("HLD FPGA", "/dev/spidev1.3", cMode, 8, 8000, 0, FALSE, FALSE);		// active low cs
#       	cMode |= SPI_CPHA; // Phase, data is clocked out on falling_edge and sampled on rising_edge
# 	cMode |= SPI_CPOL; // Polarity => Clock is default high
# SPI_MODE_3		(SPI_CPOL|SPI_CPHA)
chip = spiflash(bus=1, cs=3, mode=3, max_speed_hz=180000)
print(chip.read_id())


PAGE_SIZE=256
def get_pages_from_file(file_name:str, fill_last_page=0xff):
    pages=[]
    with open(file_name, 'rb') as f:
        while (chunk := f.read(PAGE_SIZE)) != b'':
            pages.append(list(chunk))
    last_page = pages[-1]
    for i in range(PAGE_SIZE - len(last_page)):
        last_page.append(fill_last_page)
    return pages

def test():
    print("Erasing")
    chip.erase_all()
    pages = get_pages_from_file('hld_fpga_0400_0001.rpd')
    for page_nbr,page_bytes in enumerate(pages):
        print(f"Writing page:{page_nbr}", end='\r')
        chip.write_page_to_flash(page_nbr, page_bytes)

    print('\nVerify!')
    for page_nbr,page_bytes in enumerate(pages):
        print(f"Verifying page:{page_nbr}", end='\r')
        bytes_flash=chip.get_page_from_flash(page_nbr)
        if bytes_flash!=page_bytes:
            print("Verify error")
            exit(1)

    print('\nSuccess!')
