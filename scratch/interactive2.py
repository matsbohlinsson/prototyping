export PYTHONPATH=/home/root/firmware/firmware.d/ssi/



import spidev

SPI_BUS = 1
SPI_BUS_CS = 3
SPI_SPEED = 14000000
SPI_MODE = 3
VERIFY = True


spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_BUS_CS)
spi.max_speed_hz = SPI_SPEED
spi.mode=SPI_MODE
spi.bits_per_word = 8

spi.xfer2([0x9F, 0x9F,0,0,0,0,0]) #ID

spi.xfer2([0x06]) #Write enable
spi.xfer2([0xC7]) # BULK erase
spi.xfer2([0x5, 0x5])[1] #Wait for bulk erase

#READ
spi.xfer2([0x3, 0, 0, 0] + [255 for _ in range(256)])
spi.xfer2([0x3, 0, 0, 1, 0] + [255 for _ in range(256)])
spi.xfer2([0x3, 0, 0, 2, 0] + [255 for _ in range(256)])

#WRITE
spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,0,0] + [(x)%256 for x in range(256)]) #Write

spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,1,0] + [(x-3)%256 for x in range(256)]) #Write

spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,1,1] + [(x-3)%256 for x in range(256)]) #Write


spi.xfer2([0x06]) #Write enable



spi.xfer2([0x9F, 0x9F,0,0,0,0,0]) #ID
[255, 32, 186, 24, 16, 68, 0]
# 24 = 0x18 = 128Mb



import spidev

SPI_BUS = 0
SPI_BUS_CS = 1
SPI_SPEED = 1400000
SPI_MODE = 3
VERIFY = True


spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_BUS_CS)
spi.max_speed_hz = SPI_SPEED
spi.mode=SPI_MODE
spi.bits_per_word = 8

spi.xfer2([0x9F, 0x9F,0,0,0,0,0]) #ID

spi.xfer2([0x06]) #Write enable
spi.xfer2([0xC7]) # BULK erase
spi.xfer2([0x5, 0x5])[1] #Wait for bulk erase

spi.xfer2([0xb7]) #Enter 4-byte mode


#READ
spi.xfer2([0x03, 0, 0, 0] + [255 for _ in range(256)])
spi.xfer2([0x13, 0, 0, 1, 0] + [255 for _ in range(256)])
spi.xfer2([0x13, 0, 0, 2, 0] + [255 for _ in range(256)])





#WRITE
spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,0,0] + [(x)%256 for x in range(256)]) #Write

spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,0,0,0] + [(x)%256 for x in range(256)]) #Write

spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,1,0] + [(x-3)%256 for x in range(256)]) #Write

spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,1,1] + [(x-3)%256 for x in range(256)]) #Write


spi.xfer2([0x06]) #Write enable



spi.xfer2([0x9F, 0x9F,0,0,0,0,0]) #ID
# [255, 32, 187, 34, 16, 68, 0]
# 34 = 0x22 = sGb





# 2Gb chhip
spi.xfer2([0x06]) #Write enable
spi.xfer2([0xC4,0,0,0,0]) # BULK erase
spi.xfer2([0x5, 0x5])[1] #Wait for bulk erase
spi.xfer2([0x70, 0x70])[1] #Wait for bulk erase

#READ 4-bytes
spi.xfer2([0xb7]) #Enter 4-byte mode
spi.xfer2([0x03, 0, 0, 0,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 1,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 2,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 3,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 4,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 5,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 6,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 7,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 8,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 9,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 10,0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x03, 0, 0, 11,0] + [255 for _ in range(256)]) #READ


#WRITE
spi.xfer2([0xb7]) #Enter 4-byte mode
spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,0,0,0] + [(x)%256 for x in range(256)]) #Write
spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,0,9,0] + [(255-x)%256 for x in range(256)]) #Write

spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,1,0,0] + [1+x for x in range(63)]) #Write



spi.xfer2([0x03, 0, 0, 0] + [255 for _ in range(256)]) #READ
spi.xfer2([0x06]) #Write enable
spi.xfer2([0x2, 0,12,0] + [(x)%256 for x in range(256)]) #Write
spi.xfer2([0x03, 0, 12, 0] + [255 for _ in range(256)]) #READ

spi.xfer2([0x70, 0x70])
[255, 1] = 4bytes - address
