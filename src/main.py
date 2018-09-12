'''
程序入口

注：目前各个子功能还在开发中，暂时还没有合并在一起。
'''
from machine import Pin
import utime
from car_config import gpio_dict
from motor import Motor
from servo import Servo

if __name__ == '__main__':
    # 初始化舵机云台
    # init_servo()
    
    # 初始化电机
    # init_motor()
    

    # 设定程序执行入口

    # 测试舵机
    # exec(open('test_servo.py').read(), globals())
    # 测试电机旋转
    # exec(open('test_motor.py').read(), globals())

    # 测试编码器
    # exec(open('test_encoder.py').read(), globals())

    # 串口PID控制电机旋转角度
    # exec(open('test_uart_left_mac.py').read(), globals())

    # 测试电机角度控制
    # exec(open('test_left_mac.py').read(), globals())

    # 测试电机转速PID控制
    # exec(open('test_motor_speed_pid.py').read(), globals())

    # 测试串口调节电机转速
    # exec(open('test_uart_left_msc.py').read(), globals())

    # 测试car
    # exec(open('test_car.py').read(), globals())
    # 小车前进1m
    # car.move(1)