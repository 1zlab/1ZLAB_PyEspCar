'''
编码器测试
-------------------------
注意： print频次不能高，会影响计数
电机旋转一周的计数是1480， 折算成360度角度，对应的scale取0.247
电机旋转一周的精度在 1度以内
'''
from machine import Pin
import time
from encoder import Encoder
from car_config import gpio_dict, car_property

left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
left_encoder = Encoder(left_pin_a, left_pin_b,
    reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
    scale=car_property['LEFT_ENCODER_ANGLE_SCALE'])

right_pin_a = Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN)
right_pin_b = Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN)
right_encoder = Encoder(right_pin_a, right_pin_b,
    reverse=car_property['RIGHT_ENCODER_IS_REVERSE'],
    scale=car_property['RIGHT_ENCOER_ANGLE_SCALE'])


print('test encoder')
left_counter = 0
right_counter = 0

try:
  while True:
    if abs(left_counter-left_encoder.position) > 10:
      print('Left Angle: {}'.format(left_encoder.position))
      left_counter = left_encoder.position
    
    if abs(right_counter-right_encoder.position) > 10:
      print('Right Angle: {}'.format(right_encoder.position))
      right_counter = right_encoder.position
except:
  # 释放资源
  left_encoder.deinit()
  right_encoder.deinit()
