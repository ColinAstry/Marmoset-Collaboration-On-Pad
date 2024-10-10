import os 
# import RPi.GPIO as GPIO

# #设置GPIO输出模式，此处使用13号端子作为输出正极
# GPIO.cleanup()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(32,GPIO.OUT)
# GPIO.setup(33,GPIO.OUT)
# #设置PWM信号，此处使用477Hz，对应蠕动泵转速4.77rpm，流量1.82mL/min，在5s内流出0.15mL
# p = GPIO.PWM(32,477)
# p = GPIO.PWM(33,477)
# p.start(0)

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='.')
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'G2.html')


#establish a socket connection
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Load image files
@app.route('/img/<path:filename>')
def send_static(filename):
    return send_from_directory('./img/', filename)

# Start or stop PWM output when control signal is received from the tablet


@socketio.on('cmd')
def handle_cmd(data):
    # Handle the data
    # print('Received: ' + data)
    if data == "correct" or data == "wrong" or data == "finish":
        print(data)
        # if data == "correct":
            # GPIO.output(32,GPIO.HIGH)
            # GPIO.output(33,GPIO.HIGH)
            # p.ChangeDutyCycle(50)
        #elif data == "finish":
            # GPIO.output(32,GPIO.LOW)
            # GPIO.output(33,GPIO.LOW)
            # p.ChangeDutyCycle(0)
    else:
        print(data)
        broadcast_number(data)  # Pass data to broadcast_number
    return 'Data received', 200

#broadcast num to all connected clients
def broadcast_number(num):
    socketio.emit('number', {'num': num})

# Start the server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8010)