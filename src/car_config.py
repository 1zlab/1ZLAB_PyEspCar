'''
小车的配置文件
'''
# 小车属性
car_property = {
    'CAR_WIDTH': 0.17667, # 小车的后轮轮距离，单位m
    'CAR_LENGTH': 0.15300, # 小车前后轮轮距，单位m
    'WHEEL_RADIUS': 0.0325, # 轮胎半径，单位m

    'CAR_CTL_MODE' :{ # 小车控制模式
        'SPEED': 1, # 速度控制(同时控制 speed与旋转角度)
        'STOP': 2, # 停止状态, 控制编码器旋转角度保持不变
        'GO_STRAIGHT': 3, # 走直线
        'POINT_TURN': 4, # 原地旋转
    },
    'PWM_FREQUENCY': 1000, # 电机控制与舵机控制的PWM
                            # 推荐频率 500Hz - 30000HZ
    'PID_CTL_PERIOD': 0.100, # PID控制周期 单位s 0.025
    'CAR_MAX_SPEED': 5.89, # 小车的最大直线速度, m/s
    'MOTOR_MAX_ANGLE': 2600, # 25ms内,电机最多转65度 1s -> 65 * 40
    'LEFT_MOTOR_INSTALL_DIR': False, # 左侧电机的安装方向
    'LEFT_ENCODER_IS_REVERSE': False, # 左侧编码器是否为反
    'LEFT_ENCODER_ANGLE_SCALE': 360/1320, # 编码器计数与旋转角度之间的缩放因子
    'LEFT_MOTOR_ANGLE_CTL_KP': -11.00, # 左侧电机角度控制的PID参数
    'LEFT_MOTOR_ANGLE_CTL_KI': -1.20,
    'LEFT_MOTOR_ANGLE_CTL_KD': -60.00,
    'LEFT_MOTOR_ANGLE_CTL_MAX_BIAS_SUM': 1000, # 积分上限
    'LEFT_MOTOR_SPEED_CTL_KP': -10.00, # 左侧电机速度控制的PID参数 -30.0
    'LEFT_MOTOR_SPEED_CTL_KI': -0.51,
    'LEFT_MOTOR_SPEED_CTL_KD': -5.00,
    'LEFT_MOTOR_SPEED_CTL_MAX_BIAS_SUM': 1000, # 积分上限
    
    'RIGHT_MOTOR_INSTALL_DIR': True, # 右侧电机的安装方向
    'RIGHT_ENCODER_IS_REVERSE': True, # 右侧编码器是否为反
    'RIGHT_ENCODER_ANGLE_SCALE': 360/1320, # 编码器计数与旋转角度之间的缩放因子
    'RIGHT_MOTOR_ANGLE_CTL_KP': -11.00, # 右侧电机角度控制的PID参数
    'RIGHT_MOTOR_ANGLE_CTL_KI': -1.20,
    'RIGHT_MOTOR_ANGLE_CTL_KD': -60.00,
    'RIGHT_MOTOR_ANGLE_CTL_MAX_BIAS_SUM': 1000, # 积分上限
    'RIGHT_MOTOR_SPEED_CTL_KP': -10.00, # 左侧电机速度控制的PID参数 -30.0
    'RIGHT_MOTOR_SPEED_CTL_KI': -0.51,
    'RIGHT_MOTOR_SPEED_CTL_KD': -5.00,
    'RIGHT_MOTOR_SPEED_CTL_MAX_BIAS_SUM': 1000, # 设置积分上限

    'CAR_ONE_SHOT_TIMER_ID': 2, # 单次计时器的ID
}

# GPIO字典
gpio_dict = {
    "BATTERY_ADC": 36, # 电池ADC采样(SVP) 

    "USER_BUTTON": 39, # 用户按键(SVN) 
    
    "LEFT_MOTOR_A": 32, # 左侧电机A相
    "LEFT_MOTOR_B": 33, # 左侧电机B相  
    
    "RIGHT_MOTOR_A": 25, # 右侧电机A相
    "RIGHT_MOTOR_B": 26, # 右侧电机B相  
    
    "LEFT_ENCODER_A": 34, # 左侧编码器A相
    "LEFT_ENCODER_B": 35, # 左侧编码器B相   
    
    "RIGHT_ENCODER_A": 23, # 右侧编码器A相
    "RIGHT_ENCODER_B": 22, # 右侧编码器B相 
    
    "UART_LCD_RX": 5, # 串口液晶屏 接收端
    "UART_LCD_TX": 21, # 串口液晶屏 发送
    
    "UART_USER_RX": 18, # 用户串口接收端
    "UART_USER_TX": 19, # 用户串口 发送端
    "UART1_RX": 5, # 串口1 接收端
    "UART1_TX": 21, # 串口1 发送端


    "UART2_RX": 18, # 串口2 接收端
    "UART2_TX": 19, # 串口2 发送端 

    "USER_IIC_SCL": 0, # 用户IIC SCL
    "USER_IIC_SDA": 4, # 用户IIC SDA

    "SERVO_1": 27, # 舵机1
    "SERVO_2": 12 # 舵机2
}