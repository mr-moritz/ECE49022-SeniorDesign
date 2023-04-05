from smbus2 import *

DEVICE_BUS = 1
DEVICE_ADDR = 0x15
bus = SMBus(DEVICE_BUS)

# Writing data to the I2C bus
bus.write_byte_data(DEVICE_ADDR, 0x01, 0x01)

# Reading data from the I2C bus
# bus.read_byte_data(DEVICE_ADDR, 0x00, 2)