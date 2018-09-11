# -*- coding:utf-8 -*-
'''
基于PCA9685 I2C舵机控制模块对舵机进行控制的库

上臂舵机 控制精度: 0.45度
下臂舵机 控制精度: 0.63度
'''
import pca9685
import math
from car_config import car_property

class Servo:
    '''
    利用PCA9685控制Servo
    '''
    def __init__(self, pca9685, servo_idx, min_duty=30, max_duty=130, angle_range=180, default_angle=90):
        '''
        Servo的构造器
        '''
        # PCA9685舵机驱动板
        self.pca9685 = pca9685
        # 舵机在PCA9695舵机驱动板上的编号
        self.servo_idx = servo_idx
        # 舵机最小角度时候的占空比
        self.min_duty = min_duty
        # 舵机最大角度时候的占空比
        self.max_duty = max_duty
        # 舵机角度范围
        self.angle_range = angle_range
        # 舵机默认角度
        self.default_angle = default_angle
        # 当前的角度值
        self._angle = default_angle
        # 舵机旋转到默认的角度
        self.angle(default_angle)
        

    def _angle2duty(self, angle):
        duty = self.min_duty + (self.max_duty - self.min_duty)*( angle / self.angle_range)
        return int(duty)

    def angle(self, value=None):
        if value is None:
            # 返回当前舵机的角度
            return self._angle
        else:
            # 计算舵机的占空比
            duty = self._angle2duty(value)
            # 执行指令
            self.pca9685.duty(self.servo_idx, duty)
            # 更新当前的角度值
            self._angle = value
    

class CloudPlatform:
    '''
    舵机云台
    PCA9685的Duty取值范围为 0- 4095
    '''
    def __init__(self, i2c, address=0x40, freq=50):
        # 创建PCA9685对象
        self.pca9685 = pca9685.PCA9685(i2c, address)
        # 设定PWM的频率
        self.pca9685.freq(freq)

        self.bottom_servo = Servo(
            self.pca9685,
            car_property['BOTTOM_SERVO_IDX'],
            min_duty=car_property['BOTTOM_SERVO_MIN_DUTY'],
            max_duty=car_property['BOTTOM_SERVO_MAX_DUTY'],
            angle_range=car_property['BOTTOM_SERVO_ANGLE_RANGE'],
            default_angle=car_property['BOTTOM_SERVO_DEFAULT_ANGLE'])
        
        self.top_servo = Servo(
            self.pca9685,
            car_property['TOP_SERVO_IDX'],
            min_duty=car_property['TOP_SERVO_MIN_DUTY'],
            max_duty=car_property['TOP_SERVO_MAX_DUTY'],
            angle_range=car_property['TOP_SERVO_ANGLE_RANGE'],
            default_angle=car_property['TOP_SERVO_DEFAULT_ANGLE'])
