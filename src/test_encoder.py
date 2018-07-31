'''
BUG: Left编码器，不会有输出 ？定时器设置错误？

'''
from encoder import Encoder
from car_config import gpio_dict


left_encoder = Encoder(gpio_dict['LEFT_ENCODER_A'], gpio_dict['LEFT_ENCODER_A'], 
        3, motor_install_dir=False,name='LeftEncoder', is_debug=True)

right_encoder = Encoder(gpio_dict['RIGHT_ENCODER_A'], gpio_dict['RIGHT_ENCODER_A'], 
         2, is_debug=True)