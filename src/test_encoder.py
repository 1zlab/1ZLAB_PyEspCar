'''
编码器测试
-------------------------
注意： print频次不能高，会影响计数

电机旋转一圈 A B相各 11个脉冲
减速比为1:30, 同时因为采用了四倍频技术,
所以轮子旋转一圈对应 11 * 4 * 30 = 1320个脉冲

电机旋转一周的计数是1320， 折算成360度角度，
对应的scale = 360/1320 = 3 / 11

'''
from machine import Pin,Timer
import time
from encoder import Encoder
from user_button import UserButton
from car_config import gpio_dict, car_property


# left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
# left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
# left_encoder = Encoder(left_pin_a, left_pin_b,
#     reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
#     scale=car_property['LEFT_ENCODER_ANGLE_SCALE'])

# right_pin_a = Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN)
# right_pin_b = Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN)
# right_encoder = Encoder(right_pin_a, right_pin_b,
#     reverse=car_property['RIGHT_ENCODER_IS_REVERSE'],
#     scale=car_property['RIGHT_ENCODER_ANGLE_SCALE'])


left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
left_encoder = Encoder(left_pin_a, left_pin_b,
    reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
    scale=1)

right_pin_a = Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN)
right_pin_b = Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN)
right_encoder = Encoder(right_pin_a, right_pin_b,
    reverse=car_property['RIGHT_ENCODER_IS_REVERSE'],
    scale=1)
    
print('Test Encoder')

def callback(timer):
    print('Left Angle: {}'.format(left_encoder.position))
    print('Right Angle: {}'.format(right_encoder.position))


def encoder_clear(pin):
	'''
	编码器计数清零
	'''
	left_encoder.position = 0
	right_encoder.position = 0 

# 用户按键引脚编号
USER_BUTTON = gpio_dict['USER_BUTTON']
# 创建UserButton对象
btn = UserButton(USER_BUTTON, encoder_clear)

timer = Timer(4)
# 3s 打印一次数据
timer.init(period=1000, mode=Timer.PERIODIC, callback=callback)

while True:
    try:
        pass
    except:
        # 释放资源
        left_encoder.deinit()
        right_encoder.deinit()