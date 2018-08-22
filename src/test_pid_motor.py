from machine import Timer,Pin
from pid_motor import MotorAngleControl
from motor import Motor
from encoder import Encoder
from car_config import gpio_dict


# 左侧电机
left_motor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B']) #,motor_install_dir=False)
left_motor.stop()

# 右侧电机
right_motor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])
right_motor.stop()

left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
left_encoder = Encoder(left_pin_a, left_pin_b, reverse=1, scale=0.247)

right_pin_a = Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN)
right_pin_b = Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN)
right_encoder = Encoder(right_pin_a, right_pin_b, reverse=0, scale=0.247)

# 15
mac = MotorAngleControl(left_motor, left_encoder, kp=-9, ki=-0.3, kd=-4, is_debug=False)

# 创建定时器 
# 这里用的是定时器4
timer = Timer(4)
# 设置定时器回调 100ms执行一次
# TODO 编码器是不是也会干扰到编码器计数
timer.init(period=100, mode=Timer.PERIODIC, callback=mac.callback)

# 90度 差不多是20个脉冲（不稳）
mac.set_angle(90, is_reset=False)