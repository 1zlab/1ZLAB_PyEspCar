from motor_angle_control import MotorAngleControl
from motor import Motor
from encoder import Encoder
from car_config import gpio_dict


# 左侧电机
lmotor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B']) #,motor_install_dir=False)
# 右侧电机
rmotor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])

# 左侧编码器
lencoder = Encoder(gpio_dict['LEFT_ENCODER_A'], gpio_dict['LEFT_ENCODER_A'], 
        3, motor_install_dir=False,name='LeftEncoder', is_debug=False)


mac = MotorAngleControl(lmotor, lencoder, kp=-10, is_debug=True)
mac.set_angle(90, is_reset=True)
