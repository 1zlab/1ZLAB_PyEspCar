from encoder import Encoder
from car_config import gpio_dict

'''
由于是基于定时器的 最小分辨率为1ms
1. 如果电机旋转速度快了，编码器数值增量就会变小
2. 可能会出现正转时测量出来反转脉冲的情况（细节问题，大体上不会影响）
'''
left_encoder = Encoder(gpio_dict['LEFT_ENCODER_A'], gpio_dict['LEFT_ENCODER_B'], 
        3, motor_install_dir=False,name='LeftEncoder', is_debug=True)

right_encoder = Encoder(gpio_dict['RIGHT_ENCODER_A'], gpio_dict['RIGHT_ENCODER_B'], 
         4, motor_install_dir=True, is_debug=True)