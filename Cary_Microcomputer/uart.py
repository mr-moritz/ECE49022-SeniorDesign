import serial
import time
import sys
import RPi.GPIO as GPIO


# Serial port for UART and GPIO setup
ser = serial.Serial('/dev/serial0', baudrate=9600 , parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, timeout=5, stopbits=serial.STOPBITS_ONE)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

def unlock_cary():
	# Sending data to the device
	data = bytes([0x01, 0x02])
	time.sleep(1)
	ser.flushInput()
	ser.flushOutput()
	bytes_written = ser.write(data)
	
	if bytes_written == len(data):
		print('Data successfully written to serial port!')
	else:
		print('Error while writing data to serial port.')
		pass
	
	# Sleep to allow GPIO signal to propagate
	time.sleep(0.25)
	
	# Reading GPIO input
	while GPIO.input(4) == 1:
		print("Waiting for process to finish")
		time.sleep(1)
		
	print("Process complete")
	GPIO.cleanup()


def trigger_fingerprint():
	pass
	

if __name__ == "__main__":
	if sys.argv[1] == '-u':
		unlock_cary()
	elif sys.argv[1] == '-s':
		trigger_fingerprint()
		
# try:
	# print('Reading again')
	# ser.flushInput()
	# ser.flushOutput()
	# response = ser.read_until(expected=b'ff')
	# print(response)
	# if response:
		# print("found")
	# else:
		# print("not found")
	# # while response.endswith(expected_response):
		# # data = ser.read()
		# # print(data)
		# # if data:
			# # response += data.encode('utf-8')
		# # else:
			# # continue
	# ser.close()
	# # print("response matches")
# except KeyboardInterrupt:
	# ser.close()
	# print("task ended")
	
# finally:
	# ser.close()
	# print('task ended')
