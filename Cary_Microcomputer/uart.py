import serial
import time
import sys

ser = serial.Serial('/dev/serial0', baudrate=115200 , parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, timeout=2)


#def unlock_cary():
	# Sending data to the device
	# data = bytes([0x02, 0x01])
	# bytes_written = ser.write(data)
	
	# if bytes_written == len(data):
		# print('Data successfully written to serial port!')
	# else:
		# print('Error while writing data to serial port.')
		# pass
	
	# response = ser.readlines()
	# print(response)
	# if response:
		# response = response.decode('utf-8')
		# print(response)
		# ser.close()
		# pass
		
	# print('Reading from UART')
	# response = ser.read(2)
	# print(response.hex())

	
	

#if __name__ == "__main__":
#	if sys.argv[1] == '-u':
#		unlock_cary()
#	elif sys.argv[1] == '-s':
#		trigger_fingerprint()
		
try:
	ser.open()
	print('Reading again')
	ser.flushInput()
	ser.flushOutput()
	while(True):
		response = ser.readline()
		print(response)
		# if response:
			# # response = response.decode('utf-8')
			# print(response)
			# # ser.close()
			# continue
		# else:
			# continue
except KeyboardInterrupt:
	ser.close()
	print("task ended")
	
finally:
	ser.close()
	print('task ended')
