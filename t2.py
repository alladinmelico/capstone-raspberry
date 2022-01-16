import serial
import time
import requests
import re
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 115200
ser.timeout = 0
ser.open()
key = "'Ambience Compensate\r\nT body = '"
while True:
    try:
        data = ser.read(9999)
        print(data)
        if len(data) > 1:
            body_temp_index = int(data.find(key.encode()))
            print (body_temp_index)            
            
            if body_temp_index > 1:
                byte_temp = data[body_temp_index + 9 : body_temp_index + 9 + 7]
                temp_full = float(byte_temp.decode())
                temp = round(temp_full, 1)
                print(temp)

                        

                time.sleep(1)
    except Exception as e:
        print(e)
        break
    except KeyboardInterrupt:
        print("Keyboard Interrupt registered.")
        break
ser.close()
