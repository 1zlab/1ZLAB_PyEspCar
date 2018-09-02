'''
舵机测试
'''
from machine import Pin
from car_config import gpio_dict

# 270度舵机  duty范围 24 - 130 中间：77
servo_down = Servo(Pin(gpio_dict['SERVO_1'],Pin.OUT), angle_range=270,
        min_duty=24, max_duty=130, default_angle=135)
# servo_down.angle(90)
# 180度舵机  duty范围 30 - 130 中间：80 
servo_top = Servo(Pin(gpio_dict['SERVO_2'], Pin.OUT), angle_range=180, 
        min_duty=30, max_duty=130, default_angle=90)
# servo_top.angle(100)


try:
    while True:
        pass
except:
    # 销毁资源
    servo_down.deinit()
    servo_top.deinit()