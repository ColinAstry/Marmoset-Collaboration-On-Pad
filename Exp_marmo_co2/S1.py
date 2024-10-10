#!/usr/bin/env python3.7  
import os 
# import RPi.GPIO as GPIO

# #设置GPIO输出模式，此处使用13号端子作为输出正极
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(33,GPIO.OUT)
# #设置PWM信号，此处使用477Hz，对应蠕动泵转速4.77rpm，流量1.82mL/min，在5s内流出0.15mL
# p = GPIO.PWM(33,477)
# p.start(0)

#from bottle import route,run,request,template,static_file


experiment = "G1" #此处填写实验网页的文件名
#平板电脑端输入“树莓派ip：端子”进入实验网页
@route("/",method="GET") 
def index():
    return template(experiment)
#载入图片文件
@route('/img/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./img/')
#接收到平板电脑端控制信号时启动或停止PWM输出
@route("/cmd",method="POST") 
def cmd():
    press = request.body.read().decode()
    if press == "correct" or press == "wrong" or press == "finish":
        print("press the button: " + press)
    elif press.isdigit():
        num = int(press)
        print(num)
        if 0 <= num <= 35:
         broadcast_number()
        return 'Data received'
    #    p.ChangeDutyCycle(50)
    # elif press == "finish":
    #      p.ChangeDutyCycle(0)


from bottle import get, post, run, template

from geventwebsocket import WebSocketError

from bottle import app, Bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler


#广播rand_ini给所有连接的平板电脑端
sockets = set()
@get('/websocket', apply=[WebSocketHandler])
def handle_websocket():
    global sockets
    ws = request.environ.get('wsgi.websocket')
    sockets.add(ws)
    while True:
        try:
            message = ws.receive()
        except WebSocketError:
            break
    sockets.remove(ws)

def broadcast_number():
    global sockets, num
    for ws in sockets:
        try:
            ws.send(str(num))
        except WebSocketError:
            sockets.remove(ws)

#启动监听
#run(host="192.168.230.94",port="8010",debug=True,reloader=False) 

# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler
# server = WSGIServer(("192.168.174.94", 8010), app, handler_class=WebSocketHandler)
# server.serve_forever()

# from bottle import default_app

# app = default_app()
# server = WSGIServer(('0.0.0.0', 8010), app, handler_class=WebSocketHandler)
# server.serve_forever()

from bottle import default_app
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = default_app()  # Ensure app is a valid WSGI application
server = WSGIServer(('0.0.0.0', 8010), app, handler_class=WebSocketHandler)
server.serve_forever()


