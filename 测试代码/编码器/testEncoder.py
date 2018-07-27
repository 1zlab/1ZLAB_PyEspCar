from Encoder import *

LEFT_ENCODER_A = 5
LEFT_ENCODER_B = 18
RIGHT_ENCODER_A = 21
RIGHT_ENCODER_B = 19

# 初始化右侧编码器
print('init right encoder')
right_encoder = Encoder(RIGHT_ENCODER_A, RIGHT_ENCODER_B, is_debug=True)
# 初始或左侧的编码器
print('init left encoder')
right_encoder = Encoder(LEFT_ENCODER_A, LEFT_ENCODER_B, is_debug=True, name="LeftEncoder", motor_install_dir=False)
# right_encoder = Encoder(LEFT_ENCODER_B, LEFT_ENCODER_A, is_debug=True, name="LeftEncoder", motor_install_dir=False)
