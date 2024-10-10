#!/usr/bin/env python3.7  
####### 这个试图在py内部设置一个timer，但是好像不太行
from bottle import route,run,request,template,static_file
import RPi.GPIO as GPIO
import os
import threading

#设置GPIO输出模式，此处使用13号端子作为输出正极
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(33,GPIO.OUT)
#设置PWM信号，此处使用477Hz，对应蠕动泵转速4.77rpm，流量1.82mL/min，在5s内流出0.15mL
p = GPIO.PWM(33,477)
p.start(0)
experiment = "habit3" #此处填写实验网页的文件名
#平板电脑端输入“树莓派ip：端子”进入实验网页
@route("/",method="GET") 
def index():
    return template(experiment)
#载入图片文件
@route('/img/<filename:path>')
def send_static(filename):
     return static_file(filename, root='./img/')
#改变pwmcycle的函数，方便threading调用
def set_pwm_dutycycle(dutycycle):
    p.ChangeDutyCycle(dutycycle)
#接收到平板电脑端控制信号时启动或停止PWM输出
@route("/cmd",method="POST") 
def cmd():
    press = request.body.read().decode()
    if press == "correct":
        print("press the button: "+press)
        if hasattr(cmd, "timer") and cmd.timer.is_alive():
            cmd.timer.cancel()  # 取消之前的计时器
            cmd.timer = threading.Timer(1, set_pwm_dutycycle, args=(50,))
            cmd.timer.start()
    elif press == "finish":
        p.ChangeDutyCycle(0)
    #在平板电脑端全屏时启动motion输出视频流
    elif press == "Fullscreen":
        os.system("sudo killall -TERM motion")
        os.system("sudo modprobe bcm2835-v4l2")
        os.system("sudo motion")
        return "OK"
#笔记本电脑端输入“树莓派ip:端子/controler”进入监控网页
@route("/controler",method="GET") 
def show_clock():
    return template("control")
#接收到笔记本电脑端人工控制信号时更改中间文件control.txt
@route("/control",method="POST") 
def control():
    control = request.body.read().decode()
    with open("control.txt","w+") as f:
        f.write(control)
    return "OK"
#接收到平板电脑端轮询信号时查询中间文件control.txt内容
@route("/get_control",method="POST") 
def get_control():
    with open("control.txt","r") as f:
        control = f.read()
    return "{0}".format(control)
#启动监听
run(host="192.168.251.94",port="8010",debug=True,reloader=False)