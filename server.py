import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_socketio import send, emit
import serial
import json 

raspId = 'm2ShOB1OdMtwIhdPzciH12Oqf5sEVA7C'
#url = 'https://safe-and-smart-campus.herokuapp.com/api'
url = "http://192.168.0.14/api"
rfidUrl = url + '/rfid/'
port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

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

@app.route('/display')
def display():
    data = {
        'name': request.args.get('name'),
        'photo': request.args.get('photo'),
        'schoolId': request.args.get('school_id'),
        'start': request.args.get('start_at'),
        'end': request.args.get('end_at'),
        'temp': request.args.get('temp'),
    }
    emit('schedule_response',json.dumps(data, indent = 4),json=True, namespace="/", broadcast=True)
    return "ok"

@app.route('/check')
def check():
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
        return str(temperature)
    
    return {"temp": 0, "tag": 0}
    
@socketio.on('connect')
def client_connect():
    print('connected')
    return

if __name__ == '__main__':
    socketio.run(app)
