import serial

ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

#Sending data to the device
while True:
	ser.write(b'A')

# data = ser.readline().decode('utf-8')
# print(data)

ser.close()
