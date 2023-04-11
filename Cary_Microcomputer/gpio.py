import RPi.GPIO as GPIO
import serial
import time
import sys

##########################################
#	We have depreacted the use of this	 #
#	file. All GPIO and UART 			 #
#	functionality is done through		 #
#	the uart.py file					 #
##########################################

ser = serial.Serial('/dev/serial0', baudrate=115200 , parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, timeout=5)

# Sending data to the device
data = bytes([0x02, 0x01])
bytes_written = ser.write(data)

if bytes_written == len(data):
	print('Data successfully written to serial port!')
else:
	print('Error while writing data to serial port.')
	pass

ser.close()
time.sleep(5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

input_value = GPIO.input(4)
print("Input value: ", input_value)

GPIO.cleanup()
