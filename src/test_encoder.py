from encoder import Encoder
from car_config import gpio_dict


left_encoder = Encoder(gpio_dict['LEFT_ENCODER_A'], gpio_dict['LEFT_ENCODER_B'], 
        3, motor_install_dir=False,name='LeftEncoder', is_debug=True)

right_encoder = Encoder(gpio_dict['RIGHT_ENCODER_A'], gpio_dict['RIGHT_ENCODER_B'], 
         4, motor_install_dir=True, is_debug=True)