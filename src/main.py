'''
程序入口

注：目前各个子功能还在开发中，暂时还没有合并在一起。
'''
from car_config import gpio_dict
from motor import Motor
import webrepl

def init_motor():
    # 设定两个电机刚开始的转速为0
    # 不设定pwm的话，开发板上电电机会转

    # 左侧电机
    lmotor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B']) #,motor_install_dir=False)
    # 左侧电机的速度设定为0
    lmotor.pwm(0)
    # 释放PWM资源
    lmotor.deinit()

    # 右侧电机
    rmotor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])
    rmotor.pwm(0)
    rmotor.deinit()

if __name__ == '__main__':
    # 初始化电机
    init_motor()

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