'''
串口通信协议

指令格式构成 （参考Light飞控的通信协议 做一下对应的简化）
帧头 + 功能字 + 长度 + 数据 + 校验码(长度) 

测试的时候只用到左侧电机

TODO 回传目标值（电机旋转角度）1个float值 左右
TODO 拓展协议，支持设置两个电机角度
'''
from machine import Timer,Pin,UART
import micropython
from car_config import gpio_dict
import struct
import utime
from pid_motor import MotorAngleControl
from motor import Motor
from encoder import Encoder
from car_config import gpio_dict, pid_param_dict


# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)


# 左侧电机
left_motor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B']) #,motor_install_dir=False)
left_motor.stop()
# 右侧电机
right_motor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])
right_motor.stop()
# 左侧编码器管脚

left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
# 左侧编码器
left_encoder = Encoder(left_pin_a, left_pin_b, reverse=1, scale=0.247)

# 右侧编码器管脚
right_pin_a = Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN)
right_pin_b = Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN)
# 右侧编码器
right_encoder = Encoder(right_pin_a, right_pin_b, reverse=0, scale=0.247)

# PID参数
# kp = pid_param_dict['MOTOR_ANGLE_CTL_KP']
# ki = pid_param_dict['MOTOR_ANGLE_CTL_KI']
# kd = pid_param_dict['MOTOR_ANGLE_CTL_KD']
kp = 0
ki = 0
kd = 0

# 电机角度PID控制
left_mac = MotorAngleControl(left_motor, left_encoder,
		kp=kp, ki=ki, kd=kd, is_debug=False)

right_mac = MotorAngleControl(right_motor, right_encoder,
		kp=kp, ki=ki, kd=kd, is_debug=False)

def pid_callback(timer):
    global left_mac
    global right_mac

    right_mac.callback(timer)
    send_real_value(right_mac.encoder.position)
    # left_mac.callback(timer)
    # # 串口发送当前电机的角度
    # send_real_value(left_mac.encoder.position)
    # right_mac.callback(timer)

    if uart.any():
        data_byte = uart.readline()
        data_str = data_byte.decode('utf-8')
        process_command(data_str)


# 初始化UART对象
uart = UART(1, baudrate=115200, rx=gpio_dict['UART1_RX'], tx=gpio_dict['UART1_TX'], timeout=10)
uart_protocal_len = 15 # 每帧数据的长度

def update_left_motor_pid(new_kp, new_ki, new_kd):
    '''
    更新PID
    '''
    global left_mac
    left_mac.pid.kp = float(new_kp)
    left_mac.pid.ki = float(new_kd)
    left_mac.pid.kd = float(new_kd)
    print('new pid: {}'.format(left_mac.pid))

def update_right_motor_pid(new_kp, new_ki, new_kd):
    global right_mac
    right_mac.pid.kp = float(new_kp)
    right_mac.pid.ki = float(new_ki)
    right_mac.pid.kd = float(new_kd)
    print('new pid: {}'.format(right_mac.pid))

def update_left_motor_target(new_target):
    global left_mac
    new_target = float(new_target)
    left_mac.pid.target_value = new_target
    print('new target: {}'.format(left_mac.pid.target_value))

def update_right_motor_target(new_target):
    global right_mac
    new_target = float(new_target)
    right_mac.pid.target_value = new_target
    print('new target: {}'.format(right_mac.pid.target_value))

def process_command(data_str):
    cmd_list = {
        'SET_PID': update_right_motor_pid,
        'SET_TARGET': update_right_motor_target,
    }
    print('[INFO] Recieve： {}'.format(data_str))
    params = data_str.split(',')
    cmd_str = params[0]
    if cmd_str in cmd_list:
        cmd_list[cmd_str](*params[1:])
    else:
        print('[ERROR] Ukown Command : {}'.format(cmd_str))

def send_real_value(real_value):
    global uart
    data_str = ','.join(['REAL_VALUE', str(real_value)])
    data_str += '\n' # 添加换行符号
    data_byte = data_str.encode('utf-8')
    uart.write(data_byte)


# 创建定时器 这里用的是定时器4
timer = Timer(4)
# 设置定时器回调 100ms执行一次
timer.init(period=100, mode=Timer.PERIODIC, callback=pid_callback)
