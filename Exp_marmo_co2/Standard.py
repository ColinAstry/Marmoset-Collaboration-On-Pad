#!/usr/bin/env python3.7  
import os 
# import RPi.GPIO as GPIO
#### Checked on 16th August 2024, Standard.html(For Exp1) is also correct
# #设置GPIO输出模式，此处使用13号端子作为输出正极
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(33,GPIO.OUT)
# #设置PWM信号，此处使用477Hz，对应蠕动泵转速4.77rpm，流量1.82mL/min，在5s内流出0.15mL
# p = GPIO.PWM(33,477)
# p.start(0)

from bottle import route,run,request,template,static_file

experiment = "Standard" #此处填写实验网页的文件名
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
    if press == "correct" or press == "wrong":
       print(press)
    #    if press == "correct":
    #       p.ChangeDutyCycle(50)
    # elif press == "finish":
    #      p.ChangeDutyCycle(0)
#启动监听
run(host="0.0.0.0",port="8010",debug=True,reloader=False) 