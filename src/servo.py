
'''
TODO 添加舵机控制的代码
270度舵机  duty范围 24 - 130 中间：77
180度舵机  duty范围 30 - 130 中间：80 
'''
class Servo:
    def __init__(pin, min_angle=0, max_angle=180, min_duty=30, max_duty=130, default_angle=90):
        '''
        构造器函数
        '''
        self.pin = pin
        self.pwm = PWM(pin)
        self.angle = 90
        self.angle(90)
    def angle(self, angle):
        if angle is None:

from machine import Pin

pin5 = Pin(5, Pin.OUT)
pin17 = Pin(17, Pin.OUT)

pin5.value(1)
pin17.value(0)