'''
小车对象

功能描述：
* 设置两个电机的转速（速度采样）
* 设置两个电机的旋转角度/圈数

'''
class Car(object):
    def __init__(self, battery_adc, user_button, 
                left_motor, right_motor,
                left_encoder, right_encoder)
        # 电池ADC采样
        self.battery_adc = battery_adc
        # 用户按键
        self.user_button = user_button
        # 左侧电机
        self.left_motor = left_motor
        # 右侧电机
        self.right_motor = right_motor
        # 左侧编码器
        self.left_encoder = left_encoder
        # 右侧编码器
        self.right_encoder = right_encoder
        

        # 小车停止标志为
        self.stop_flag = False