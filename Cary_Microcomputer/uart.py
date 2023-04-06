import serial
import time
import sys

ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=5, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)


def unlock_cary():
	# Sending data to the device
	data = bytes([0x0a])
	ser.write(data)
	time.sleep(2)
	
	while True:
		response = ser.read()
		if response:
			response = response.decode('utf-8')
		else:
			ser.close()
			pass

def trigger_fingerprint():
	pass

if __name__ == "__main__":
	if sys.argv[1] == '-u':
		unlock_cary()
	elif sys.argv[1] == '-s'
		trigger_fingerprint():
