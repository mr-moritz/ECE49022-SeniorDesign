

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()


def read_NFC():
    id, text = reader.read()

    user = text 

def write_NFC(person):
    reader.write(person)
    print("RFID successfully written!")

# try:
#     read_NFC()

# except KeyboardInterrupt:
#     GPIO.cleanup()
