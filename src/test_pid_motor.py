from pid_motor import MotorAngleControl
from motor import Motor
from encoder import Encoder
from car_config import gpio_dict


# 左侧电机
lmotor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B']) #,motor_install_dir=False)
lmotor.stop()

# 右侧电机
rmotor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])
rmotor.stop()

# 左侧编码器
lencoder = Encoder(gpio_dict['LEFT_ENCODER_A'], gpio_dict['LEFT_ENCODER_B'], 
        3, motor_install_dir=False,name='LeftEncoder', is_debug=True)

mac = MotorAngleControl(lmotor, lencoder, kp=-250, ki=0, kd=0, is_debug=False, scalar=4.5)
# 90度 差不多是20个脉冲（不稳）
mac.set_angle(90, is_reset=False)


'''
BUG
有时候 电机明明反转 计数器+1

旋转电机 复位的时候跟原来的位置差很多
'''