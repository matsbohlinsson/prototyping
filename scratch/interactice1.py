export PYTHONPATH=/home/root/firmware/firmware.d/ssi/



import spidev
SPI_BUS=0
SPI_BUS_CS=1
SPI_SPEED = 14000000
SPI_MODE = 3
VERIFY = True
GPIO_VP_CSN=68
setGPIO(GPIO_VP_CSN, 0)
setGPIO(GPIO_VP_CSN, 1)
setGPIO(GPIO_VP_CSN, 0)
setGPIO(127,0)

spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_BUS_CS)
spi.max_speed_hz = SPI_SPEED
spi.mode=SPI_MODE
spi.bits_per_word = 8

spi.xfer2([0x9F, 0x9F])[1:][0] #ID

spi.xfer2([0x06]) #Write enable
spi.xfer2([0xC7]) # BULK erase
spi.xfer2([0x5, 0x5])[1] #Wait for bulk erase

#READ
spi.xfer2([0x3, 0, 0, 0] + [255 for _ in range(256)])
spi.xfer2([0x3, 0, 0, 1, 0] + [255 for _ in range(256)])
spi.xfer2([0x3, 0, 0, 2, 0] + [255 for _ in range(256)])

#WRITE
spi.xfer2([0x06]) #Write enable
spi.xfer2([0xC7]) # BULK erase
spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,0,1] + [(x+3)%256 for x in range(256)]) #Write

spi.xfer2([0x06]) #Write enable
