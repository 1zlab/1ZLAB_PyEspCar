'''
car的测试文件
'''
from car import Car
from car_config import gpio_dict,pid_param_dict
from battery_voltage import BatteryVoltage
from motor import Motor
from encoder import Encoder
from pid_motor import MotorAngleControl
from machine import Timer,Pin

# 左侧电机
left_motor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B'], motor_install_dir=False)
left_motor.stop()
# 右侧电机
right_motor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])
right_motor.stop()

# 左侧编码器管脚
left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
# 左侧编码器
left_encoder = Encoder(left_pin_a, left_pin_b, reverse=0, scale=0.247)

# 右侧编码器管脚
right_pin_a = Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN)
right_pin_b = Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN)
# 右侧编码器
right_encoder = Encoder(right_pin_a, right_pin_b, reverse=1, scale=0.247)

# PID参数
kp = pid_param_dict['MOTOR_ANGLE_CTL_KP']
ki = pid_param_dict['MOTOR_ANGLE_CTL_KI']
kd = pid_param_dict['MOTOR_ANGLE_CTL_KD']

# 电机角度PID控制
# 设置对大积分上限
left_mac = MotorAngleControl(left_motor, left_encoder,
		kp=kp, ki=ki, kd=kd, max_bias_sum=45, is_debug=False)

right_mac = MotorAngleControl(right_motor, right_encoder,
		kp=kp, ki=ki, kd=kd, max_bias_sum=45, is_debug=False)

car = Car(left_mac, right_mac)


# 创建定时器 这里用的是定时器4
timer = Timer(1)
# 设置定时器回调 100ms执行一次
timer.init(period=100, mode=Timer.PERIODIC, callback=car.callback)

