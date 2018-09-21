'''
霍尔AB相正交编码器类
'''
import math
from machine import Pin
from config import config
from pyb import Timer

class Encoder(object):

    ENCODER_PERIOD = 60000

    # 编码器字典
    encoder_list = [
        (
            config['LEFT_ENCODER_A_GPIO'],
            config['LEFT_ENCODER_B_GPIO'],
            config['LEFT_ENCODER_TIMER_ID'],
            config['LEFT_ENCODER_AF_TIM'],
            config['LEFT_ENCODER_IS_REVERSE']
        ),
        (
            config['RIGHT_ENCODER_A_GPIO'],
            config['RIGHT_ENCODER_B_GPIO'],
            config['RIGHT_ENCODER_TIMER_ID'],
            config['RIGHT_ENCODER_AF_TIM'],
            config['RIGHT_ENCODER_IS_REVERSE']
        )
    ]

    def __init__(self, idx, is_quad_freq=False, reverse=False):
        
        gpio_a, gpio_b, timer_id, af_tim, reverse = Encoder.encoder_list[idx]
        
        self.pin_a = Pin(gpio_a, Pin.AF_PP, pull=Pin.PULL_NONE, af=af_tim)
        self.pin_b = Pin(gpio_b, Pin.AF_PP, pull=Pin.PULL_NONE, af=af_tim)
        self.enc_timer = Timer(timer_id, prescaler=0, period=Encoder.ENCODER_PERIOD)
        
        self.is_quad_freq = is_quad_freq # 是否开启四倍频
        if self.is_quad_freq:
            self.enc_channel = self.enc_timer.channel(1,Timer.ENC_AB)
        else:
            self.enc_channel = self.enc_timer.channel(1,Timer.ENC_A)

        # 轮子的半径
        self.CAR_WHEEL_RADIUS =  config['CAR_WHEEL_RADIUS']
        # 电机减速比
        self.motor_reduction_gear_ratio = config['MOTOR_REDUNCTION_GEAR_RATIO']
        # 编码器分辨率： 电机旋转一周对应的脉冲数
        self.encoder_resolution = config['ENCODER_RESOLUTION']
        
         # 电机旋转一圈对应的脉冲
        self.one_circle_pulse = self.encoder_resolution * self.motor_reduction_gear_ratio
        if self.is_quad_freq:
            # 如果开启四倍频就*4
            self.one_circle_pulse *= 4


        self.reverse = reverse

        self.angle_scale = 0 # 编码器脉冲计数与电机旋转角度之间的缩放因子
        self.set_angle_scale()
        self.distance_scale = 0 # 编码器脉冲计数与电机前进距离之间的缩放因子
        self.set_distance_scale()
    


    def set_angle_scale(self):
        '''设置编码器脉冲计数与电机旋转角度之间的比例因子'''
        # 计算一个脉冲相当于多少度
        self.angle_scale = 360 / self.one_circle_pulse

    def set_distance_scale(self):
        '''设置编码器脉冲计数与电机前进距离之间的比例因子'''
        # 计算一个脉冲相当于前进了多少米
        self.distance_scale = ( 2 * math.pi * self.CAR_WHEEL_RADIUS) / self.one_circle_pulse

    @property
    def counter(self):
        '''计数器计数'''
        cnt = 0
        if self.enc_timer.counter() > (Encoder.ENCODER_PERIOD / 2):
            cnt = -1 * (Encoder.ENCODER_PERIOD - self.enc_timer.counter())
        else:
            cnt = self.enc_timer.counter()

        if self.reverse:
            cnt *= -1
        return cnt
    @counter.setter
    def counter(self, value):
        '''设置计数器的取值'''
        if self.reverse:
            value *= -1
        
        value = int(value)
        if value > 0:
            self.enc_timer.coutner(value)
        else:
            self.enc_timer.counter(Encoder.ENCODER_PERIOD - value)
    
    @property
    def angle(self):
        '''电机旋转角度 单位:度'''
        return self.counter * self.angle_scale
    
    @angle.setter
    def angle(self, value):
        '''设定电机旋转角度 单位：度'''
        self.counter = value // self.angle_scale
    

    @property
    def distance(self):
        return self.counter * self.distance_scale
    
    @distance.setter
    def distance(self, value):
        self.counter = value // self.distance_scale
    
    def reset(self):
        '''重置编码器'''
        self.counter = 0
    
    def deinit(self):
        '''
        资源释放
        '''
        del(self)
    
    def __str__(self):
        
        return 'Encoder Counter: {}, Distance: {}, Angle: {}'.format(self.counter, self.distance, self.angle)