#!/usr/bin/python3
import typer
from pathlib import Path
from common import sleep_ms, SpiActiveFlash, get_pages_from_file, setGPIO, \
    reverse_bit_order
import binascii
import spidev

PAGE_SIZE=256
DEVICE_ID = 0x20
PAD_VALUE=0xff

GPIO_VP_CSN=68
GPIO_SPI_DIRECT = 132

if 0: #TI flash
    SPI_BUS=0
    SPI_BUS_CS=0
    SPI_SPEED = 12000
    SPI_MODE = 3
    VERIFY = True
    FILE_DEFAULT = '/home/root/firmware/binary/ssi-fpga/hld_fpga_p65.rpd'
    def enable_flash_mode() -> None:
        setGPIO(GPIO_SPI_DIRECT, 1)
        #i2c command
    def disable_flash_mode() -> None:
        setGPIO(GPIO_SPI_DIRECT, 0)
        #i2c command

if 1: #VP flash
    SPI_BUS=0
    SPI_BUS_CS=1
    SPI_SPEED = 12000000
    SPI_MODE = 3
    VERIFY = True
    FILE_DEFAULT = '/home/root/firmware/binary/vp-fpga/vp-fpga_mux_spi_ti_flash.bin'
    #FILE_DEFAULT = '/home/root/firmware/binary/ssi-fpga/hld_fpga_p65.rpd'
    def enable_flash_mode() -> None:
        setGPIO(GPIO_VP_CSN, 0)
    def disable_flash_mode() -> None:
        setGPIO(GPIO_VP_CSN, 1)
if 0: #HLD
    GPIO_NCONFIG = 125
    GPIO_NCE = 127
    SPI_BUS=1
    SPI_BUS_CS=3
    SPI_SPEED = 14000000
    SPI_MODE = 3
    VERIFY = True
    FILE_DEFAULT = '/home/root/firmware/binary/ssi-fpga/hld_fpga_p65.rpd'
    def enable_flash_mode() -> None:
        setGPIO(GPIO_NCONFIG, 0)
        setGPIO(GPIO_NCE, 0)
        setGPIO(GPIO_NCONFIG, 1)
        setGPIO(GPIO_NCE, 0)
        setGPIO(GPIO_NCONFIG, 0)
        setGPIO(GPIO_NCE, 1)

    def disable_flash_mode() -> None:
        setGPIO(GPIO_NCE, 0)
        setGPIO(GPIO_NCONFIG, 1)



def flash(filename: Path, spi_hz:int=SPI_SPEED) -> int:
    # cMode |= SPI_CPHA; // Phase, data is clocked out on falling_edge and sampled on rising_edge
    # cMode |= SPI_CPOL; // Polarity => Clock is default high
    # /dev/spidev1.3 mode=3 (SPI_CPOL|SPI_CPHA)
    chip = SpiActiveFlash(bus=SPI_BUS, bus_cs=SPI_BUS_CS, mode=SPI_MODE, max_speed_hz=spi_hz)
    print("Enable flash mode")
    enable_flash_mode()
    sleep_ms(100)

    id = chip.read_id()
    print("ID:", id)
    if id != DEVICE_ID:
        print("Wrong device id:", id)
        return 1
    chip.erase_all_start()
    chip.erase_wait_until_done()
    reverse_pages = pages = get_pages_from_file(filename, page_size=PAGE_SIZE)
    #reverse_pages = reverse_bit_order(pages)
    chip.write_pages(reverse_pages)

    if VERIFY:
        print('\nVerify!')
        exit_code = chip.verify_pages(reverse_pages)

    #disable_flash_mode()
    id=chip.read_id()
    print("\nID:", id)
    '''
    if id != 0:
        print("Error: Device id should be 0 when FPGA active")
        return 1
    '''
    return exit_code

def main(filename: Path = Path(FILE_DEFAULT), spi_hz:int=SPI_SPEED, retry:int=1) -> None:
    exitcode=0
    for i in range(retry):
        exitcode = flash(filename, spi_hz)
        if exitcode==0: break
        print(f'\nError Retry:{i+1}')
    if exitcode!=0:
        typer.echo("Failed")
        raise typer.Exit(code=1)
    print('\nSuccess!')

if __name__ == "__main__":
    #print(f"Currentversion:{getFlashVersion()}")
    typer.run(main)


