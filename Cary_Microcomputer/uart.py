import serial
import time

ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=2, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)

#Sending data to the device
data = bytes([0x0a])
while True:
	ser.write(data)
	time.sleep(2)

# data = ser.readline().decode('utf-8')
# print(data)

ser.close()
