'''
校准舵机云台
初始化舵机角度

'''
from machine import Pin,PWM

pwm_freq = 50

servo_bottom = PWM(Pin(25, Pin.OUT), freq=pwm_freq)
servo_top = PWM(Pin(26, Pin.OUT), freq=pwm_freq)

servo_bottom.duty(77)
servo_top.duty(80)