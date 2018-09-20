'''
电机类的测试文件
'''
import time
from motor import Motor
from button import Button

# 左侧电机
lmotor = Motor(0)
# 右侧电机
rmotor = Motor(1)


lmotor.pwm = 300
rmotor.pwm = 300


def stop(irq_pin):
    global lmotor
    global rmotor
    print('STOP')
    lmotor.stop()
    rmotor.stop()

button = Button(0, callback=stop)

def quit():
    lmotor.deinit()
    rmotor.deinit()
    button.deinit()

