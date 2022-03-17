import serial
from time import sleep
import requests
from getmac import get_mac_address

raspId = get_mac_address().replace(':','')

port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
url = 'https://phplaravel-745170-2505664.cloudwaysapps.com/api/temperature'

def sendReq(temp):    
    try:
        postTemperature = requests.post(url + '?id=' + raspId, data={'temperature': temp})
        print ('temp status', postTemperature.status_code)
    except Exception:
        print ('[Error]: Sending temperature data to remote server.')

while True:
    
    data = ser.read(9999)

    if len(data) > 1:
        temp = ((data[5] * 256) + data[4]) * 0.1
        print (temp)
        sendReq(temp)
        print ("---")            

ser.close()