from car_config import gpio_dict
from motor import Motor
import time

# 左侧电机
lmotor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B']) #,motor_install_dir=False)
lmotor.set_pwm(250)

# 右侧电机
rmotor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])
rmotor.set_pwm(250)


try:
    while True:
        pass
except:
     lmotor.destroy ()
     rmotor.destroy ()