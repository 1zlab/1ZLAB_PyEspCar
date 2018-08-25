'''
小车的配置文件
'''

# GPIO字典
gpio_dict = {
    "BATTERY_ADC": 36, # 电池ADC采样(SVN) 
                       # TODO 我当前使用的测试开发板板载有其他元器件，有影响
                       # 在NodeMCU32S上面单独测试36pin的ADC没有问题
    "USER_BUTTON": 39, # 用户按键(SVP)
    
    "LEFT_MOTOR_A": 17, # 左侧电机A相
    "LEFT_MOTOR_B": 5, # 左侧电机B相
    
    "RIGHT_MOTOR_A": 18, # 右侧电机A相
    "RIGHT_MOTOR_B": 19, # 右侧电机B相
    
    "LEFT_ENCODER_A": 15, # 左侧编码器A相
    "LEFT_ENCODER_B": 4, # 左侧编码器B相
    
    "RIGHT_ENCODER_A": 14, # 右侧编码器A相
    "RIGHT_ENCODER_B": 27, # 右侧编码器B相
    
    "UART_LCD_RX": 33, # 串口液晶屏 接收端
    "UART_LCD_TX": 32, # 串口液晶屏 发送端
    "UART_USER_RX": 35, # 用户串口接收端
    "UART_USER_TX": 34, # 用户串口 发送端

    "UART1_RX": 33, # 串口1 接收端
    "UART1_TX": 32, # 串口1 发送端
    "UART2_RX": 35, # 串口2 接收端
    "UART2_TX": 34, # 串口2 发送端
    
    "USER_IIC_SCL": 22, # 用户IIC SCL
    "USER_IIC_SDA": 23, # 用户IIC SDA
 
    "SERVO_1": 25, # 舵机1
    "SERVO_2": 26 # 舵机2
}


# PID控制参数
pid_param_dict = {
    'MOTOR_ANGLE_CTL_KP': -9,
    'MOTOR_ANGLE_CTL_KI': -0.3,
    'MOTOR_ANGLE_CTL_KD': -4
}