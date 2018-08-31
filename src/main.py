'''
程序入口

注：目前各个子功能还在开发中，暂时还没有合并在一起。
'''
from car_config import gpio_dict
from motor import Motor

def init_motor():
    # 设定两个电机刚开始的转速为0
    # 不设定pwm的话，开发板上电电机会转

    # 左侧电机
    lmotor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B']) #,motor_install_dir=False)
    # 左侧电机的速度设定为0
    lmotor.set_pwm(0)
    # 释放PWM资源
    lmotor.deinit()

    # 右侧电机
    rmotor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])
    rmotor.set_pwm(0)
    rmotor.deinit()

# 初始化电机
init_motor()

# 设定程序执行入口
# exec(open('uart_pid_motor_angle_control.py').read(), globals())