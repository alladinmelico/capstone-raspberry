import serial
from time import sleep
import codecs
import base64
import struct

port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

while True:
    
    data = ser.read(9999)

    if len(data) > 1:
        temp = ((data[5] * 256) + data[4]) * 0.1
        print (data)
        print (temp)
        print ("---")


    sleep(1)
            

ser.close()