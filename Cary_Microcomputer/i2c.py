from smbus2 import *
import time

##########################################
#	We have deprecated the use of		 #
#	I2C in our project. We are using	 #
#	UART instead of I2C					 #
##########################################

DEVICE_BUS = 1
DEVICE_ADDR = 0x30
bus = SMBus(DEVICE_BUS)
time.sleep(1)

address_list = [0x27]

# Writing data to the I2C bus
print("Writing data to I2C bus\n")
while True:
	for address in address_list:
		try:
			bus.write_byte(address, 0xab)
			print("check %d" % address)
		except:
			print("error %d" % address)
		time.sleep(0.5)
	print("CYCLE")

# Reading data from the I2C bus
# bus.read_byte_data(DEVICE_ADDR, 0x00, 2)
