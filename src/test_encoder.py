'''
编码器测试
'''
from machine import Pin
import time
from encoder import Encoder
from car_config import gpio_dict

left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
left_encoder = Encoder(left_pin_a, left_pin_b, reverse=1, scale=1)

right_pin_a = Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN)
right_pin_b = Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN)
right_encoder = Encoder(right_pin_a, right_pin_b, reverse=0, scale=1)

print('test encoder')

left_counter = 0
right_counter = 0

while True:
  if left_counter != left_encoder.position:
    print('LEFT: {}'.format(left_encoder.position))
    left_counter = left_encoder.position
  
  if right_counter != right_encoder.position:
    print('RIGHT: {}'.format(right_encoder.position))
    right_counter = right_encoder.position
