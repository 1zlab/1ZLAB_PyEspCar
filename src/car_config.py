'''
小车的管脚配置
'''
# GPIO字典
gpio_dict = {
    'BATTERY_ADC': 35,  # 电池ADC采样
    'USER_BUTTON': 22,  # 用户按键
    'LEFT_MOTOR_A': 23, # 左侧电机A相
    'LEFT_MOTOR_B': 15, # 左侧电机B相
    'RIGHT_MOTOR_A': 25,    # 右侧电机A相
    'RIGHT_MOTOR_B': 27,    # 右侧电机B相
    'LEFT_ENCODER_A': 5,    # 左侧编码器A相
    'LEFT_ENCODER_B': 18,   # 左侧编码器B相
    'RIGHT_ENCODER_A': 21,  # 右侧编码器A相
    'RIGHT_ENCODER_B': 19, # 右侧编码器B相
    'UART_LCD_RX': 16,  # 串口液晶屏 接收端
    'UART_LCD_TX': 17   # 串口液晶屏 发送端
}
# PID控制参数
pid_param_dict = {
    'MOTOR_ANGLE_CTL_KP': -9,
    'MOTOR_ANGLE_CTL_KI': -0.3,
    'MOTOR_ANGLE_CTL_KD': -4
}