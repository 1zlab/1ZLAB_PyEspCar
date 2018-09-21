'''
带电机的编码器测试
'''
import time
from motor import Motor
from button import Button
from encoder import Encoder


def move(pwm, time_ms):
    '''
    小车前进
    '''
    print('Car Move')
    left_motor.pwm = pwm
    right_motor.pwm = pwm
    utime.sleep_ms(time_ms)
    stop()

def stop():
    global left_motor
    global right_motor
    print('STOP')
    left_motor.stop()
    right_motor.stop()

def encoder_clear():
    '''
    编码器计数清零
    '''
    global left_encoder
    global right_encoder

    left_encoder.distance = 0
    right_encoder.distance = 0 

def print_encoder_info():
    global left_encoder
    global right_encoder

    print('Left Distance: {}'.format(left_encoder.distance))
    print('Right Distance: {}'.format(right_encoder.distance))

def callback(irq_handler):
    encoder_clear()
    move(500, 1000)
    print_encoder_info()

def quit():
    global left_motor
    global right_motor
    global left_encoder
    global right_encoder

    left_motor.deinit()
    right_motor.deinit()
    left_encoder.deinit()
    right_encoder.deinit()
    button.deinit()

# 左侧电机
left_motor = Motor(0)
# 左侧编码器
left_encoder = Encoder(0, is_quad_freq=False, motor=left_motor)

# 右侧电机
right_motor = Motor(1)
# 右侧编码器
right_encoder = Encoder(1, is_quad_freq=False, motor=right_motor)

button = Button(0, callback=callback)