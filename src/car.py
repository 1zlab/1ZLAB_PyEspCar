'''
小车对象
'''
import math
import utime
from machine import Pin,Timer,I2C

from car_config import car_property, gpio_dict
from battery_voltage import BatteryVoltage
from button import Button
from motor import Motor
from cloud_platform import CloudPlatform
import gc

class Car(object):
    def __init__(self, is_debug=False):
        '''
        Car构造器函数
        '''
        # 小车的位姿
        self = Pose(0, 0, 0, 0, 0)

        # 电池ADC采样
        self.battery_adc = BatteryVoltage(
            gpio_dict['BATTERY_ADC'],
            is_debug=False)
        
        # 用户按键
        self.user_button = Button(
            0, 
            callback=lambda pin: self.stop_trigger(pin))
        
        try:
            # 创建一个I2C对象
            i2c = I2C(
                scl=Pin(gpio_dict['I2C_SCL']),
                sda=Pin(gpio_dict['I2C_SDA']),
                freq=car_property['I2C_FREQUENCY'])
            # 创建舵机云台对象
            self.cloud_platform = CloudPlatform(i2c)
        except:
            print('[ERROR]: pca9885舵机驱动模块初始化失败')
            print('[Hint]: 请检查接线')
        
        self.speed_percent = 50 # 小车默认速度

        # 左侧电机
        self.left_motor = Motor(0)
        self.left_motor.stop() # 左侧电机停止

        # 右侧电机
        self.right_motor = Motor(1)
        self.right_motor.stop() # 右侧电机停止

        # 小车停止标志位
        self.stop_flag = False
        self.is_debug = is_debug # 是否开始调试模式
    

    def stop(self):
        '''停车'''
        self.left_motor.speed_percent = 0
        self.right_motor.speed_percent = 0

    def stop_trigger(self, pin):
        '''
        切换小车的停止位
        '''
        self.stop_flag = not self.stop_flag
        if self.stop_flag:
            self.stop()

        if self.is_debug:
            print('切换stopflag flag={}'.format(self.stop_flag))
    

    def go_forward(self, speed_percent=None, delay_ms=None):
        '''
        小车前进
        '''
        if speed_percent is None:
            speed_percent = self.speed_percent
        self.left_motor.speed_percent = speed_percent
        self.right_motor.speed_percent = speed_percent

        if delay_ms is not None:
            utime.sleep_ms(int(delay_ms))
            self.stop()

    def go_backward(self, speed_percent=None, delay_ms=None):
        '''
        小车后退
        '''
        if speed_percent is None:
            speed_percent = self.speed_percent

        self.left_motor.speed_percent = -speed_percent
        self.right_motor.speed_percent = -speed_percent

        if delay_ms is not None:
            utime.sleep_ms(int(delay_ms))
            self.stop()
        
    def turn_left(self, speed_percent=None, elay_ms=None):
        '''
        小车左转
        '''
        if speed_percent is None:
            speed_percent = self.speed_percent

        self.left_motor.speed_percent = -speed_percent
        self.right_motor.speed_percent = speed_percent

        if delay_ms is not None:
            utime.sleep_ms(int(delay_ms))
            self.stop()

    def turn_right(self, speed_percent=None, elay_ms=None):
        '''
        小车右转
        '''
        if speed_percent is None:
            speed_percent = self.speed_percent

        self.left_motor.speed_percent = speed_percent
        self.right_motor.speed_percent = -speed_percent

        if delay_ms is not None:
            utime.sleep_ms(int(delay_ms))
            self.stop()


    def deinit(self):
        '''
        释放资源
        '''
        self.battery_adc.deinit()
        self.user_button.deinit()
        self.left_motor.deinit()
        self.right_motor.deinit()
    
    def log(self):
        # 打印日志 TODO
        print('[INFO] battery voltage: {}'.format(self.battery_adc.battery_voltage))
        print('[INFO] default velocity (percent): {}'.format(self.speed_percent))
