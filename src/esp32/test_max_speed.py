'''
测试小车的最大速度

最大速度， 测试得到1.25m/s
'''
from motor import Motor
from car_config import car_property, gpio_dict
from button import Button
import utime

# 左侧电机
left_motor = Motor(
    gpio_dict['LEFT_MOTOR_A'],
    gpio_dict['LEFT_MOTOR_B'], 
    motor_install_dir=car_property['LEFT_MOTOR_INSTALL_DIR'])
left_motor.stop() # 左侧电机停止
        
# 右侧电机
right_motor = Motor(
    gpio_dict['RIGHT_MOTOR_A'], 
    gpio_dict['RIGHT_MOTOR_B'], 
    motor_install_dir=car_property['RIGHT_MOTOR_INSTALL_DIR'])
right_motor.stop() # 右侧电机停止



def callback(pin, pwm=1023, delay_ms=2000):
    global left_motor
    global right_motor

    left_motor.pwm(pwm)
    right_motor.pwm(pwm)

    utime.sleep_ms(delay_ms)

    left_motor.stop() # 左侧电机停止
    right_motor.stop() # 右侧电机停止


button = Button(0, callback=lambda pin: callback(pin, pwm=400, delay_ms=2000))