import micropython
from  machine import Pin,Timer,UART
import utime

from car_config import gpio_dict, car_property

from user_button import UserButton
from motor import Motor
from encoder import Encoder
from pid_motor import MotorSpeedPID


# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)

# 左侧电机
left_motor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B'], 
        motor_install_dir=car_property['LEFT_MOTOR_INSTALL_DIR'])
left_motor.stop()

# 左侧编码器
left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
left_encoder = Encoder(left_pin_a, left_pin_b,
    reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
    scale=car_property['LEFT_ENCODER_ANGLE_SCALE'])

# 左侧电机速度控制PID
kp = car_property['LEFT_MOTOR_SPEED_CTL_KP']
ki = car_property['LEFT_MOTOR_SPEED_CTL_KI']
kd = car_property['LEFT_MOTOR_SPEED_CTL_KD']

max_bias_sum = 500
# 创建电机速度PID控制的对象
left_speed_pid = MotorSpeedPID(left_motor, left_encoder, 
        kp = kp, ki = ki, kd = kd,
        max_bias_sum = max_bias_sum,
        is_debug=False)

# 初始化UART对象
uart = UART(1, baudrate=115200, rx=gpio_dict['UART1_RX'], tx=gpio_dict['UART1_TX'], timeout=10)

def update_pid(new_kp, new_ki, new_kd):
    '''
    更新速度控制的PID参数
    '''
    global left_speed_pid
    left_speed_pid.pid.kp = float(new_kp)
    left_speed_pid.pid.ki = float(new_ki)
    left_speed_pid.pid.kd = float(new_kd)
    print('new pid: {}'.format(left_speed_pid.pid))

def update_target(new_target):
    '''
    设置速度目标值
    '''
    global left_speed_pid
    new_target = float(new_target)
    left_speed_pid.pid.set_target_value(new_target)
    print('new target: {}'.format(left_speed_pid.pid.target_value))


def process_command(data_str):
    '''
    处理串口发过来的指令
    '''
    cmd_list = {
        'SET_PID': update_pid,
        'SET_TARGET': update_target,
    }

    print('[INFO] Recieve： {}'.format(data_str))
    params = data_str.split(',')
    cmd_str = params[0]
    if cmd_str in cmd_list:
        cmd_list[cmd_str](*params[1:])
    else:
        print('[ERROR] Ukown Command : {}'.format(cmd_str))

def send_real_value(real_value):
    '''
    发送当前速度的真实值
    '''
    global uart
    data_str = ','.join(['REAL_VALUE', str(real_value)])
    data_str += '\n' # 添加换行符号
    data_byte = data_str.encode('utf-8')
    uart.write(data_byte)


def pid_callback(timer):
    '''
    PID控制回调函数
    '''
    global left_speed_pid

    # 速度控制回调函数
    left_speed_pid.callback(timer, min_threshold=0)
    # 发送真实的速度
    send_real_value(left_speed_pid.speed())

    if uart.any():
        data_byte = uart.readline()
        data_str = data_byte.decode('utf-8')
        process_command(data_str)


timer = Timer(2)
# 设置定时器回调 100ms执行一次
timer.init(period=100, mode=Timer.PERIODIC, callback=pid_callback)

try:
    while True:
        pass
except:
    # 注意要先释放timer
    timer.deinit()
    # 释放speed控制
    left_speed_pid.deinit()
    