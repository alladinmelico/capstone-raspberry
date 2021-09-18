import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
GPIO.setwarnings(False)

reader = SimpleMFRC522()
raspId = 'm2ShOB1OdMtwIhdPzciH12Oqf5sEVA7C'

try:
    id, text = reader.read()
    print(id)
    print(text)
finally:
    GPIO.cleanup()

#try:
#    text = input('New data:')
#    print("Now place your tag to write")
#    reader.write(text)
#    print("Written")
#finally:
#    GPIO.cleanup()
    
url = 'http://192.168.0.14/api'
r = requests.get(url + '/facility')
print (r.status_code)
print (r.headers)
print (r.text[0:1000])