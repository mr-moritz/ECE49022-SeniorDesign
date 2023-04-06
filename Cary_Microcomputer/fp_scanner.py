
#import RPi.gpio as GPIO
import time, serial

FINGERPRINT_CAPACITY=     80      #Fingerprint module capacity
MODULE_SN_SIZE=           16      #Module SN length 


DELALL=                   0xFF    #Delete all fingerprints 

CMD_PREFIX_CODE=          b'\U\xaa'  #Command packet prefix code 
RCM_PREFIX_CODE=          b'\xaaU'   #Response packet prefix code 
CMD_DATA_PREFIX_CODE=     0xA55A  #Command data packet prefix code 
RCM_DATA_PREFIX_CODE=     0x5AA5  #Response data packet prefix code 

CMD_TYPE=                 0xF0    #Command packet type 
RCM_TYPE=                 0xF0    #Response packet type 
DATA_TYPE=                0x0F    #Data packet type 

CMD_TEST_CONNECTION=      b'\x01\x00'  #Test connection 
CMD_SET_PARAM=            b'\x02\x00' #0X0002  #Set parameter
CMD_GET_PARAM=            b'\x03\x00' #0X0003  #Read parameter 
CMD_DEVICE_INFO=          b'\x04\x00' #0X0004  #Read device information 
CMD_SET_MODULE_SN=        0X0008  #Set module serial number 
CMD_GET_MODULE_SN =       0X0009  #Read module serial number
CMD_ENTER_STANDBY_STATE=  0X000C  #Enter sleep mode 
CMD_GET_IMAGE=            0X0020  #Capture fingerprint image 
CMD_FINGER_DETECT=        b'\x21\x00' #0X0021  #Detect fingerprint 
CMD_UP_IMAGE_CODE=        0X0022  #Upload fingerprint image to host 
CMD_DOWN_IMAGE=           0X0023  #Download fingerprint image to module 
CMD_SLED_CTRL=            b'\x24\x00' #0X0024  #Control collector backlight 
CMD_STORE_CHAR=           0X0040  #Save fingerprint template data into fingerprint library 
CMD_LOAD_CHAR=            0X0041  #Read fingerprint in module and save it in RAMBUFFER temporarily  
CMD_UP_CHAR=              0X0042  #Upload the fingerprint template saved in RAMBUFFER to host 
CMD_DOWN_CHAR=            0X0043  #Download fingerprint template to module designated RAMBUFFER
CMD_DEL_CHAR=             0X0044  #Delete fingerprint in specific ID range 
CMD_GET_EMPTY_ID=         0X0045  #Get the first registerable ID in specific ID range 
CMD_GET_STATUS=           0X0046  #Check if the designated ID has been registered 
CMD_GET_BROKEN_ID=        0X0047  #Check whether there is damaged data in fingerprint library of specific range
CMD_GET_ENROLL_COUNT=     0X0048  #Get the number of registered fingerprints in specific ID range 
CMD_GET_ENROLLED_ID_LIST= 0X0049  #Get registered ID list
CMD_GENERATE=             0X0060  #Generate template from the fingerprint images saved in IMAGEBUFFER temporarily 
CMD_MERGE=                0X0061  #Synthesize fingerprint template data 
CMD_MATCH=                0X0062  #Compare templates in 2 designated RAMBUFFER 
CMD_SEARCH=               0X0063  #1:N Recognition in specific ID range 
CMD_VERIFY=               0X0064  #Compare specific RAMBUFFER template with specific ID template in fingerprint library 

ERR_SUCCESS=              b'\x00'    #Command processed successfully 
ERR_ID809=                b'\xff'    #error

ser = serial.Serial(port = "/dev/serial0", baudrate = 115200, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, timeout = 2)

# contents of a command packet: 26 byes: 10 frame header, 14 data, 2 cks
# cmd_prefix_code: b'U\xaa,
# source device id: x00
# destination device id: x00
# command code: four bytes 
# data length: 
if(ser.isOpen() == False):
    ser.open()
ser.flushInput()
ser.flushOutput()

def test_connection():
    ser.flushInput()
    ser.flushOutput()
    
    print('testing connection')
    
    ser.write(CMD_PREFIX_CODE) #prefix: 2 bytes
    ser.write(b'\x00')#source device id: 1 byte
    ser.write(b'\x00')#destination device id: 1 byte
    ser.write(CMD_TEST_CONNECTION) #command: 2 bytes
    ser.write(b'\x00\x00') #data length: 2 bytes
    ser.write(b'\x00\x00') #payload: 2 bytes
    ser.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') #data: 14 bytes
    cks = getCmdCKS(CMD_TEST_CONNECTION, b'\x00',b'\x00', b'\x00',b'\x00')
    ser.write(cks[1:2])
    ser.write(cks[0:1])  #cks: 2 bytes

    #print(getCmdCKS(CMD_TEST_CONNECTION, b'\x00', b'\x00', b'\x00\x00', b'\x00\x00'))
   
    recieved = ser.readline()
    ret, data = responsePayload(recieved)

    #print(recieved)
    
    if(ret == ERR_SUCCESS):
        print('connection test successfull')
        return True
    else:
        print('connection test unsuccessfull')
        return False

def getDeviceInfo():
    ser.flushInput()
    ser.flushOutput()

    print('getting device info')

    ser.write(CMD_PREFIX_CODE)
    ser.write(b'\x00')
    ser.write(b'\x00')
    ser.write(CMD_DEVICE_INFO)
    ser.write(b'\x00\x00') #data length: 2 bytes
    ser.write(b'\x00\x00') #payload: 2 bytes
    ser.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') #data: 14 bytes
    cks = getCmdCKS(CMD_DEVICE_INFO, ERR_SUCCESS, ERR_SUCCESS, b'\x00\x00', b'\x00\x00')
    ser.write(cks[1:2])
    ser.write(cks[0:1])

    recieved = ser.readline()
    print(recieved)

def getDeviceID():
    ser.flushInput()
    ser.flushOutput()

    print('getting device ID')
    data = b'\x00\x00'

    ser.write(CMD_PREFIX_CODE)
    ser.write(b'\x00')
    ser.write(b'\x00')
    ser.write(CMD_GET_PARAM)
    ser.write(b'\x01\x00')
    ser.write(data)
    ser.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    cks = getCmdCKS(CMD_PREFIX_CODE, ERR_SUCCESS, ERR_SUCCESS, data, b'\x01\x00')
    ser.write(cks[1:2])
    ser.write(cks[0:1])

    recieved = ser.readline()
    print(recieved)

#works
def fingerDetect():
    ser.flushInput()
    ser.flushOutput()

    print('detecting finger...')

    ser.write(CMD_PREFIX_CODE)
    ser.write(b'\x00')
    ser.write(b'\x00')
    ser.write(CMD_FINGER_DETECT)
    ser.write(b'\x00\x00')
    ser.write(b'\x00\x00')
    ser.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    cks = getCmdCKS(CMD_FINGER_DETECT, ERR_SUCCESS, ERR_SUCCESS, b'\x00', b"\x00\x00")
    ser.write(cks[1:2])
    ser.write(cks[0:1])

    recieved = ser.readline()
    ret,data = responsePayload(recieved)
    if(ret == ERR_SUCCESS):
        if(data == b'\x00\x01'):
            print('finger detected')
        else:
            print('no finger detected')
    else:
        print('error')


def led_control(status, color):
    ser.flushInput()
    ser.flushOutput()
    
    print('led_control')
    def switch(status):
        if status == "on":
            d_status = b'\x01'
        elif status == 'off':
            d_status = b'\x00'
        elif status == 'breath':
            d_status = b'\x02'
        else:
            d_status = b'\x00'

    
    data = b'\x03\x83'
    
    ser.write(CMD_PREFIX_CODE) #prefix: 2
    ser.write(b'\x00') # source device id: 1
    ser.write(b'\x00') # dest device id: 1
    ser.write(CMD_SLED_CTRL) # command: 2: 0x2400
    ser.write(b'\x02\x00') # data length : 2
    ser.write(data) # payload: 2
    ser.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    #ser.write(data)
    cks = getCmdCKS(CMD_SLED_CTRL, b'\x00', b'\x00', data, b'\x02\x00')
    ser.write(cks[1:2])
    ser.write(cks[0:1])

    
    recieved = ser.readline()
    print(recieved)
#     ser.write(b'U\xaa')
#     ser.write()

def responsePayload(recieved):          #0:2 2:3 3:4 4:5 5:6 6:7 7:8 8:9 9:10
    packet = recieved
    data = b''
    if(recieved[0:2] == RCM_PREFIX_CODE): #b'\xaaU\x01\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01'
        dataLen = int.from_bytes((recieved[7:8]+recieved[6:7]),'big')
        for i in range(dataLen, 1, -1):
            data = data + recieved[8+i:9+i]
        ret = recieved[8:9]
        cks = packet[24:26]
        if((cks[1:2]+cks[0:1]) != getRcmCKS(packet)):
            ret = ERR_ID809
            print('data transfer error')
    else:
        ret = ERR_ID809

    return ret, data
    #else: #recieved[0:2] == b'\xa5\x5a'):

def getCmdCKS(CMD, SID, DID, payload, LEN):
    cks = b'\xff'

    #print("CMD:")
    #print(CMD)
    #print("SID:")
    #print(SID)
    #print("DID:")
    #print(DID)
    #print("payload:")
    #print(payload)
    #print("LEN:")
    #print(LEN)


    temp = int.from_bytes(cks,'big') + int.from_bytes(SID,'big')
    cks = temp.to_bytes(2,'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(DID,'big')
    cks = temp.to_bytes(2,'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(CMD[0:1], 'big')
    cks = temp.to_bytes(2, 'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(CMD[1:2], 'big')
    cks = temp.to_bytes(2, 'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(LEN[0:1], 'big')
    cks = temp.to_bytes(2,'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(LEN[1:2], 'big')
    cks = temp.to_bytes(2,'big')

    len = int.from_bytes(LEN[1:2] + LEN[0:1],'big')

    if(len > 0):
        for i in range(1, len+1):
            temp = int.from_bytes(payload[i-1:i], 'big') + int.from_bytes(cks,'big')
            cks = temp.to_bytes(2,'big')

    #print(cks)
    return cks[0:2]

def getRcmCKS(packet):
    cks = b'\xff'
    SID = packet[2:3]
    DID = packet[3:4]
    RCM = packet[4:6]
    LEN = packet[7:8] + packet[6:7]
    RET = packet[8:10]

    #print("SID:")
    #print(SID)
    #print("DID:")
    #print(DID)
    #print("RCM:")
    #print(RCM)
    #print("LEN:")
    #print(LEN)
    #print("RET:")
    #print(RET)

    temp = int.from_bytes(cks,'big') + int.from_bytes(SID,'big')
    cks = temp.to_bytes(2,'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(DID,'big')
    cks = temp.to_bytes(2,'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(RCM[0:1], 'big')
    cks = temp.to_bytes(2, 'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(RCM[1:2], 'big')
    cks = temp.to_bytes(2, 'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(LEN[0:1], 'big')
    cks = temp.to_bytes(2,'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(LEN[1:2], 'big')
    cks = temp.to_bytes(2,'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(RET[0:1], 'big')
    cks = temp.to_bytes(2,'big')

    temp = int.from_bytes(cks,'big') + int.from_bytes(RET[1:2], 'big')
    cks = temp.to_bytes(2,'big')

    len = int.from_bytes(LEN,'big')

    if(len > 0):
        for i in range(0, len):
            temp = int.from_bytes(packet[10+i:11+i], 'big') + int.from_bytes(cks,'big')
            cks = temp.to_bytes(2,'big')
    
    return cks[0:2]

try:
    ser.flushInput()
    ser.flushOutput()
    print('sending code')
    #packet = bytearray()
    
    #CMD_PREFIX_CODE

    #test_connection()
    
    #getDeviceInfo()
    #getDeviceID()

    #while(True):
    #    fingerDetect()

    led_control()

    #while(True):
    #    recieved = ser.readline()
    #    print(recieved)
    #    if(recieved == (b'U\xaa\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')):
    #        ser.write(b'\xaaU\x01\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01')
    #    recieved = ser.readline()
    #    print(recieved)
    #FingerDetect()
    
    
    #while(True):
    #    test_connection()
        #led_control()
    #    recieved = ser.readline()
    #    print(recieved)
    
    #ser.write(packet) # 0X
        #print('sent: ', cw)
    # type, cmd, payload, length
    #prefix, payload, sid, did, cmd, len
    #prefix = CMD_PREFIX_CODE, payload= 0x0000, SID = 0, DID = 0x0, cmd = CMD_TEST_CONNECTION, len = 0x0 
    
        #ser.write(CMD_TEST_CONNECTION) # 0X0001 -> 0000 0000 0001
        #ser.write(0X00)
        #ser.write(0)
    #while(True):
    #    print('reading')
    #    time.sleep(0.5)
    #    recieved = ser.readline()
    #    if(recieved):
    #        print(recieved)
    #if (recieved == ERR_SUCCESS):
    #    print('connection test successfull')
    #else:
    #    print('connection test unsuccessfull')

except KeyboardInterrupt:
    ser.close()
    print('stopped')
    
    #command packet structure
    #typedef struct{
  #uint16_t  PREFIX;
  #uint8_t   SID;
  #uint8_t   DID;
  #uint16_t  CMD;
  #uint16_t  LEN;
  #uint8_t payload[0];
#}__attribute__ ((packed)) sCmdPacketHeader_t, *pCmdPacketHeader_t;    

    #response packet structure
    #typedef struct{
  #uint16_t  PREFIX;
  #uint8_t   SID;
  #uint8_t   DID;
  #uint16_t  RCM;
  #uint16_t  LEN;
  #uint16_t  RET;
  #uint8_t   payload[0];
#}__attribute__ ((packed)) sRcmPacketHeader_t, *pRcmPacketHeader_t;

    #sends an is connected packet



finally:
    ser.close()
    print('stopped')
    #GPIO.cleanup()