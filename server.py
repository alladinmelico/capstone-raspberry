import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_socketio import send, emit
import serial

raspId = 'm2ShOB1OdMtwIhdPzciH12Oqf5sEVA7C'
#url = 'https://safe-and-smart-campus.herokuapp.com/api'
url = "http://192.168.0.14/api"
rfidUrl = url + '/rfid/'
port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

def sendReq(temp, tag):
    
    try:
        getRfid = requests.get(rfidUrl + str(tag) + '?id=' + raspId)
        print('rfid request', getRfid)

        if (getRfid.status_code == 404):
            urlString = rfidUrl + '?id=' + raspId + '&value=' + str(tag)
            print ('url', urlString)
            postRfid = requests.post(urlString)
            print ('postRfid', postRfid)
            if (postRfid.status_code == 201):
                print ('RFID added')
            else:
                print ('body', postRfid.body)
                print (str(postRfid.status_code) + ' Cannot register the RFID, contact the administrator')
        elif (getRfid.status_code == 419):
            print ('You do not have a schedule for today')
        elif (getRfid.status_code == 200):
            print ('Logged in')
            sleep(0.5)
        elif (getRfid.status_code == 204):
            print ('Logged out')
            sleep(0.10)
        else:
            print ('Error, contact the administrator')
        emit('new_data', 'from server', broadcast=True)
    except Exception:
        print ('Unable to connect')
        return
    
    postTemperature = requests.post(url + '/temperature' + '?id=' + raspId, data={'temperature': temp, 'user_id': id})
    print ('temp status', postTemperature.status_code)
    
    return

socketio = SocketIO(logger=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

def some_function():
    emit('schedule_response', 'foo', broadcast=True)
    return

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check')
def check():
    #checkRfid()
    tag = request.args.get('tag')
    if (tag and len(tag) >= 10):        
        temperature = 0.0
        while True:
            data = ser.read(9999)

            if len(data) > 1:
                temperature = ((data[5] * 256) + data[4]) * 0.1
                print (data)
                print (temperature)
                print ("---")
                break
        print ('tag', tag)
        sendReq(temperature, tag)
        return {"temp": str(temperature), "tag": str(tag)}
    
    return {"temp": 0, "tag": 0}
    
@socketio.on('connect')
def client_connect():
    print('connecteds')
    emit('schedule_response', 'foo', broadcast=True)
    return

if __name__ == '__main__':
    socketio.run(app)
