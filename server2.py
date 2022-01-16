import requests
import RPi.GPIO as GPIO
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit
from gpiozero.pins.pigpio import PiGPIOFactory
from mfrc522 import SimpleMFRC522
from gpiozero import LED, Buzzer
from time import sleep
from smbus2 import SMBus
from mlx90614 import MLX90614

GPIO.setwarnings(False)
pigpio_factory = PiGPIOFactory()

reader = SimpleMFRC522()
raspId = 'm2ShOB1OdMtwIhdPzciH12Oqf5sEVA7C'
url = 'https://sscsystem.tech/api'
rfidUrl = url + '/rfid/'
greenLED = LED(24, pin_factory=pigpio_factory, initial_value=True)
buzz = Buzzer(23, pin_factory=pigpio_factory)
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

def checkRfid():
    id, text = reader.read()
    greenLED.off()
    
    try:
        getRfid = requests.get(rfidUrl + str(id) + '?id=' + raspId)
        print('rfid request', getRfid)

        if (getRfid.status_code == 404):
            urlString = rfidUrl + '?id=' + raspId + '&value=' + str(id)
            print ('url', urlString)
            postRfid = requests.post(urlString)
            if (postRfid.status_code == 200 or postRfid.status_code == 201):
                print ('RFID added')
                buzz.beep(0.10,0.10,3, False)
            else:
                print ('body', postRfid.body)
                print (str(postRfid.status_code) + ' Cannot register the RFID, contact the administrator')
                buzz.beep(0.10,0.10,2, False)
        elif (getRfid.status_code == 419):
            print ('You do not have a schedule for today')
            buzz.beep(0.10,0.10,2, False)
        elif (getRfid.status_code == 200):
            print ('Logged in')
            buzz.on()
            sleep(0.5)
        elif (getRfid.status_code == 204):
            print ('Logged out')
            buzz.on()
            sleep(0.10)
        else:
            print ('Error, contact the administrator')
        emit('new_data', 'from server', broadcast=True)
    except Exception:
        print ('Unable to connect')
    
    postTemperature = requests.post(url + '/temperature' + '?id=' + raspId, data={'temperature': sensor.get_object_1(), 'user_id': id})
    print ('temp status', postTemperature.status_code)
    print ("Ambient Temperature :", sensor.get_ambient())
    print ("Object Temperature :", sensor.get_object_1())
    
    buzz.off()
    sleep(1)    
    greenLED.on()
    GPIO.cleanup()
    bus.close()
    # return

socketio = SocketIO(logger=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

def some_function():
    id, text = reader.read()
    emit('schedule_response', 'foo', broadcast=True)
    return

@app.route('/')

def index():
 return render_template('index.html')

@app.route('/check')
def check():
    checkRfid()
    
@socketio.on('connect')
def client_connect():
    print('connecteds')
    id, text = reader.read()
    emit('schedule_response', 'foo', broadcast=True)
    return

if __name__ == '__main__':
    socketio.run(app)

