'''
霍尔AB相正交编码器类
'''
import math
from machine import Pin
from car_config import car_property,gpio_dict


class Encoder(object):
    # 编码器字典
    encoder_list = [
        (
            gpio_dict['LEFT_ENCODER_A'],
            gpio_dict['LEFT_ENCODER_B'],
            car_property['LEFT_ENCODER_IS_REVERSE']
        ),
        (
            gpio_dict['RIGHT_ENCODER_A'],
            gpio_dict['RIGHT_ENCODER_B'],
            car_property['RIGHT_ENCODER_IS_REVERSE']
        )
    ]


    def __init__(self, idx, motor=None, is_quad_freq=False):
        
        gpio_x, gpio_y, reverse = Encoder.encoder_list[idx]

        self.pin_x = Pin(gpio_x, Pin.IN) # 编码器A相
        self.pin_y = Pin(gpio_y, Pin.IN) # 编码器B相
        self.reverse = reverse # 编码器安装方向
        self.motor = motor

        self.forward = True # 判断电机旋转方向 是否向前
        self._pos = 0 # 编码器的脉冲计数

        # 轮子的半径
        self.wheel_radius =  car_property['WHEEL_RADIUS']
        # 电机减速比
        self.motor_reduction_gear_ratio = car_property['MOTOR_REDUNCTION_GEAR_RATIO']
        # 编码器分辨率： 电机旋转一周对应的脉冲数
        self.encoder_resolution = car_property['ENCODER_RESOLUTION']
        
        self.is_quad_freq = is_quad_freq # 是否开启四倍频

        self.angle_scale = 0 # 编码器脉冲计数与电机旋转角度之间的缩放因子
        self.set_angle_scale()
        self.distance_scale = 0 # 编码器脉冲计数与电机前进距离之间的缩放因子
        self.set_distance_scale()
        
        if self.is_quad_freq:
            # 开启四倍频，检测编码器的AB相上升沿与下降沿
            self.x_interrupt = self.pin_x.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.x_callback)
            self.y_interrupt = self.pin_y.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.y_callback)
        else:
            # A相编码器上升沿触发中断
            self.x_interrupt = self.pin_x.irq(trigger=Pin.IRQ_RISING, handler=self.x_callback)
        
    def x_callback(self, line):
        '''
        编码器A相外部中断处理函数
        '''
        if self.motor is not None and abs(self.motor.pwm) > 0:
            # 根据电机的PWM信号判断方向
            if self.motor.pwm > 0:
                self._pos += 1
            else:
                self._pos -= 1
        else:
            # 根据AB相的值判断方向
            self.forward = self.pin_x.value() ^ self.pin_y.value() ^ self.reverse
            self._pos += 1 if self.forward else -1

    def y_callback(self, line):
        '''
        编码器B相外部中断处理函数
        '''
        if self.motor is not None and abs(self.motor.pwm) > 0:
            # 根据电机的PWM信号判断方向
            if self.motor.pwm > 0:
                self._pos += 1
            else:
                self._pos -= 1
        else:
            # 根据AB相的值判断方向
            self.forward = self.pin_x.value() ^ self.pin_y.value() ^ self.reverse ^ 1
            self._pos += 1 if self.forward else -1

    def set_angle_scale(self):
        '''设置编码器脉冲计数与电机旋转角度之间的比例因子'''
        # 电机旋转一圈对应的脉冲
        one_circle_pulse = self.encoder_resolution * self.motor_reduction_gear_ratio
        if self.is_quad_freq:
            # 如果开启四倍频就*4
            one_circle_pulse *= 4
        
        # 计算一个脉冲相当于多少度
        self.angle_scale = 360 / one_circle_pulse

    def set_distance_scale(self):
        '''设置编码器脉冲计数与电机前进距离之间的比例因子'''
        # 电机旋转一圈对应的脉冲
        one_circle_pulse = self.encoder_resolution * self.motor_reduction_gear_ratio
        if self.is_quad_freq:
            # 如果开启四倍频就*4
            one_circle_pulse *= 4
        
        # 计算一个脉冲相当于前进了多少米
        self.distance_scale = ( 2 * math.pi * self.wheel_radius) / one_circle_pulse

    @property
    def angle(self):
        '''电机旋转角度 单位:度'''
        return self._pos * self.angle_scale
    
    @angle.setter
    def angle(self, value):
        '''设定电机旋转角度 单位：度'''
        self._pos = value // self.angle_scale
    

    @property
    def distance(self):
        return self._pos * self.distance_scale
    
    @distance.setter
    def distance(self, value):
        self._pos = value // self.distance_scale
    
    def deinit(self):
        '''
        资源释放
        '''
        # 注销引脚的IRQ
        self.pin_x.irq(trigger=0, handler=None)
        self.pin_y.irq(trigger=0, handler=None)
