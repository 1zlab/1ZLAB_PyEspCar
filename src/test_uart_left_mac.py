'''
串口通信，调试PID电机角度控制
-----------------
控制左侧电机的角度
'''
import utime
import micropython
from machine import Timer,Pin,UART
from car_config import gpio_dict
from pid_motor import MotorAngleControl
from motor import Motor
from encoder import Encoder

from car_config import gpio_dict, car_property
from uart_debug_tool import UartPidParamAdjust


# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)

# 左侧电机
left_motor = Motor(
    gpio_dict['LEFT_MOTOR_A'],
    gpio_dict['LEFT_MOTOR_B'], 
    motor_install_dir=car_property['LEFT_MOTOR_INSTALL_DIR'])
# 左侧电机停止
left_motor.stop()

# 右侧电机
right_motor = Motor(
    gpio_dict['RIGHT_MOTOR_A'], 
    gpio_dict['RIGHT_MOTOR_B'], 
    motor_install_dir=car_property['RIGHT_MOTOR_INSTALL_DIR'])
right_motor.stop()

# 左侧编码器
left_encoder = Encoder(
    Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN),
    Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN),
    reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
    scale=car_property['LEFT_ENCODER_ANGLE_SCALE'])

# 电机角度PID控制
left_mac = MotorAngleControl(
    left_motor,
    left_encoder,
	kp=0, ki=0, kd=0,
    max_bias_sum = 1000,
    is_debug=False)

# 初始化UART对象
uart = UART(1, baudrate=115200, rx=gpio_dict['UART1_RX'], tx=gpio_dict['UART1_TX'], timeout=10)

# 创建一个UART参数调节对象
uart_ppa = UartPidParamAdjust(left_mac.pid, uart, is_debug=True)


def callback(timer):
    '''
    回调函数
    '''
    global left_mac
    global uart_ppa

    uart_ppa.callback(timer, left_mac.encoder.position)
    left_mac.callback(timer)
# 创建定时器 这里用的是定时器4
timer = Timer(1)
# 设置定时器回调 100ms执行一次
timer.init(period=100, mode=Timer.PERIODIC, callback=callback)

try:
    while True:
        pass
except:
    # 关闭UART总线, UART没有deinit方法
    # uart.deinit()
    # 释放定时器
    timer.deinit()
    # 释放编码器与电机资源
    left_mac.deinit()
