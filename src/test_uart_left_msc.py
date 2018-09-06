'''
小车串口调试电机速度控制
'''
import micropython
from  machine import Pin,Timer,UART
import utime

from car_config import gpio_dict, car_property

from user_button import UserButton
from motor import Motor
from encoder import Encoder
from pid_motor import MotorSpeedControl
from uart_debug_tool import UartPidParamAdjust


# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)

# 左侧电机
left_motor = Motor(
    gpio_dict['LEFT_MOTOR_A'],
    gpio_dict['LEFT_MOTOR_B'], 
    motor_install_dir=car_property['LEFT_MOTOR_INSTALL_DIR'])
left_motor.stop()

# 右侧电机
right_motor = Motor(
    gpio_dict['RIGHT_MOTOR_A'], 
    gpio_dict['RIGHT_MOTOR_B'], 
    motor_install_dir=car_property['RIGHT_MOTOR_INSTALL_DIR'])
right_motor.stop()


# 左侧编码器
left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
left_encoder = Encoder(left_pin_a, left_pin_b,
    reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
    scale=car_property['LEFT_ENCODER_ANGLE_SCALE'])

# # 左侧电机速度控制PID
# kp = car_property['LEFT_MOTOR_SPEED_CTL_KP']
# ki = car_property['LEFT_MOTOR_SPEED_CTL_KI']
# kd = car_property['LEFT_MOTOR_SPEED_CTL_KD']

max_bias_sum = 500

# 创建电机速度PID控制的对象
left_msc = MotorSpeedControl(left_motor, left_encoder, 
        kp = 0, ki = 0, kd = 0,
        max_bias_sum = car_property['LEFT_MOTOR_SPEED_CTL_MAX_BIAS_SUM'],
        is_debug=False)

# 初始化UART对象
uart = UART(1, baudrate=115200, rx=gpio_dict['UART1_RX'], tx=gpio_dict['UART1_TX'], timeout=10)

# 创建一个UART参数调节对象
uart_ppa = UartPidParamAdjust(left_msc.pid, uart, is_debug=True)

def callback(timer):
    '''
    回调函数
    '''
    global left_msc
    global uart_ppa

    uart_ppa.callback(timer, left_msc.speed())
    left_msc.callback(timer)

# 创建定时器 这里用的是定时器4
timer = Timer(1)
# 设置定时器回调 100ms执行一次
period = int(car_property['PID_CTL_PERIOD'] * 1000)

timer.init(
    period=period, 
    mode=Timer.PERIODIC, 
    callback=callback)

try:
    while True:
        pass
except:
    # 注意要先释放timer
    timer.deinit()
    # 释放speed控制
    left_msc.deinit()
    