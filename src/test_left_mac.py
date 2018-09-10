import micropython
from  machine import Pin,Timer
import utime

from car_config import gpio_dict, car_property

from user_button import UserButton
from motor import Motor
from encoder import Encoder
from pid_motor import MotorAngleControl


# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)

# 左侧电机
left_motor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B'], 
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

# 左侧电机速度控制PID
kp = car_property['LEFT_MOTOR_ANGLE_CTL_KP']
ki = car_property['LEFT_MOTOR_ANGLE_CTL_KI']
kd = car_property['LEFT_MOTOR_ANGLE_CTL_KD']

left_mac = MotorAngleControl(left_motor, left_encoder, 
        kp = kp, ki = ki, kd = kd,
        max_bias_sum=car_property['LEFT_MOTOR_ANGLE_CTL_MAX_BIAS_SUM'],
        is_debug=False)

def btn_callback(pin):
    '''
    回调函数
    改变小车的标志位
    '''
    global left_mac
    print('User Button Pressed')
    utime.sleep_ms(500)
    left_mac.is_debug = not left_mac.is_debug

# 用户按键引脚编号
USER_BUTTON = gpio_dict['USER_BUTTON']
# 创建UserButton对象
btn = UserButton(USER_BUTTON, btn_callback)


def callback(timer):
    # 速度控制回调函数
    left_mac.callback(timer, min_threshold=3)
    
# 创建定时器 这里用的是定时器4
timer = Timer(4)
# 设置定时器回调 100ms执行一次

timer.init(period=25, mode=Timer.PERIODIC, callback=callback)