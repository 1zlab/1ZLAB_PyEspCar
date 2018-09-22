'''
小车的配置文件
'''
from machine import Pin

# PyCar配置文件
config = {    
    # 电池电压采样
    'BATTERY_ADC_GPIO': 'X5', # 电压采样的GPIO  ESP32->SVP
    'BATTERY_ADC_SAMPLE_PERIOD': 100, # 电池采样的周期（均值）
    'BATTERY_OVER_DISCHARGE_VOLT': 11.0, # 电池过放的参考电压值
    'BATTERY_ADC_RESOLUTION': 4096, # 满量程的读数
    'BATTERY_ADC_SCALAR': 11, # 电池电压缩放因子

    # 用户按键
    'USER_BUTTON': 0, # PyBoard自带用户按键， Switch()
    
    # 电机通用配置
    'MOTOR_PWM_FREQUENCY': 1000, # 电机控制的PWM, 推荐频率 500Hz - 30000HZ
    'MOTOR_PWM_MAX_DUTY':  84000, # 电机PWM信号占空比的最大取值
    'MOTOR_PWM_MAX_DUTY_PERCENT': 100, # 电机PWM占空比 （百分比）
    'MOTOR_REDUNCTION_GEAR_RATIO': 30/1, # 电机减速比
    'MOTOR_SPEED_PID_CTL_PERIOD': 0.010, # 电机速度控制PID控制周期

    # 左侧电机
    'LEFT_MOTOR_A_GPIO': 'X3', # 左侧电机A相 ESP32 -> 32
    'LEFT_MOTOR_B_GPIO': 'X4', # 左侧电机B相 ESP32 -> 33
    'LEFT_MOTOR_TIMER_ID': 5, 
    'LEFT_MOTOR_A_CHANNEL': 3,
    'LEFT_MOTOR_B_CHANNEL': 4,
    'LEFT_MOTOR_IS_REVERSE': False, # 左侧电机的安装方向
    'LEFT_MOTOR_SPEED_CTL_KP': -30, # 左侧电机速度控制的PID参数 Kp
    'LEFT_MOTOR_SPEED_CTL_KI': -60,  # 左侧电机速度控制的PID参数 Ki
    'LEFT_MOTOR_SPEED_CTL_KD': 0,   # 左侧电机速度控制的PID参数 Kd

    # 右侧电机
    'RIGHT_MOTOR_A_GPIO': 'Y7', # 右侧电机A相 ESP32 -> 25
    'RIGHT_MOTOR_B_GPIO': 'Y8', # 右侧电机B相  ESP32 -> 26
    'RIGHT_MOTOR_TIMER_ID': 12, 
    'RIGHT_MOTOR_A_CHANNEL': 1,
    'RIGHT_MOTOR_B_CHANNEL': 2,
    'RIGHT_MOTOR_IS_REVERSE': True, # 右侧电机的安装方向
    'RIGHT_MOTOR_SPEED_CTL_KP': -30, # 左侧电机速度控制的PID参数 kp
    'RIGHT_MOTOR_SPEED_CTL_KI': -60,  # 左侧电机速度控制的PID参数 ki
    'RIGHT_MOTOR_SPEED_CTL_KD': -0,  # 左侧电机速度控制的PID参数 kd

    # 编码器通用属性
    'ENCODER_RESOLUTION': 11, # 编码器分辨率： 电机旋转一周对应的脉冲数

    # 左侧编码器
    'LEFT_ENCODER_IS_REVERSE': False, # 左侧编码器是否为反
    'LEFT_ENCODER_A_GPIO': 'X1', # 左侧编码器A相  ESP32 -> 22
    'LEFT_ENCODER_B_GPIO': 'X2', # 左侧编码器B相  ESP32 -> 23
    'LEFT_ENCODER_TIMER_ID': 2, # 左侧编码器定时器的标号
    'LEFT_ENCODER_AF_TIM': Pin.AF1_TIM2,
    
    # 右侧编码器
    'RIGHT_ENCODER_IS_REVERSE': False, # 右侧编码器是否为反
    'RIGHT_ENCODER_A_GPIO': 'X9', # 右侧编码器A相 ESP32 -> 34
    'RIGHT_ENCODER_B_GPIO': 'X10', # 右侧编码器B相 ESP32 -> 35
    'RIGHT_ENCODER_TIMER_ID': 4,
    'RIGHT_ENCODER_AF_TIM': Pin.AF2_TIM4,
    
    # 小车机械属性
    'CAR_WIDTH': 0.17667, # 小车的后轮轮距离，单位m
    'CAR_LENGTH': 0.15300, # 小车前后轮轮距，单位m
    'CAR_WHEEL_RADIUS': 0.0325, # 轮胎半径，单位m
    'CAR_MAX_SPEED': 3.0, # 小车的最大直线速度, m/s
    
    # 舵机通用配置
    'SERVO_PWM_FREQUENCY': 50, # 舵机控制的PWM
    'SERVO_PWM_PERIOD':  1023, # 电机PWM的最大取值
    'SERVO_TIMER_ID': 8,

    # 云台底部舵机
    'SERVO_BOTTOM_GPIO': 'Y1', # 底部舵机的序号
    'SERVO_BOTTOM_CHANNEL_ID': 1,
    'SERVO_BOTTOM_PWM_DUTY_PERCENT_MIN': 2.50, # 底部舵机 最小占空比
    'SERVO_BOTTOM_PWM_DUTY_PERCENT_MAX': 12.50, # 底部舵机 最大占空比
    'SERVO_BOTTOM_ANGLE_RANGE': 270, # 底部舵机角度范围
    'SERVO_BOTTOM_DEFAULT_ANGLE': 135, # 底部舵机的默认角度
    
    # 云台顶部舵机
    'SERVO_TOP_GPIO': 'Y2', # 底部舵机的序号
    'SERVO_TOP_CHANNEL_ID': 2,
    'SERVO_TOP_PWM_DUTY_PERCENT_MIN': 3.0, # 底部舵机 最小占空比
    'SERVO_TOP_PWM_DUTY_PERCENT_MAX': 13.0, # 底部舵机 最大占空比
    'SERVO_TOP_ANGLE_RANGE': 180, # 底部舵机角度范围
    'SERVO_TOP_DEFAULT_ANGLE': 90, # 底部舵机的默认角度
}