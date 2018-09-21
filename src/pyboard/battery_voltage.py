'''
对电池电压进行采样
-------------------
航模电池需要监控电池的电压
满电或者过放都不好,需要检测电压值是否低于某个特定的值, 
如果低于的话, 电机停止工作.

注：锂电池18650电池组自带过放保护，所以不需要做过放检测。
'''
import utime
from machine import Pin
from pyb import ADC
from config import config 

class BatteryVoltage(object):

    BATTERY_ADC_GPIO = config['BATTERY_ADC_GPIO'] # 电池采样ADC管脚编号
    BATTERY_ADC_RESOLUTION = config['BATTERY_ADC_RESOLUTION'] # ADC满量程读数
    BATTERY_ADC_SAMPLE_PERIOD = config['BATTERY_ADC_SAMPLE_PERIOD'] # 电池ADC采样周期
    BATTERY_OVER_DISCHARGE_VOLT = config['BATTERY_OVER_DISCHARGE_VOLT'] # 电池过放参考电压
    BATTERY_ADC_SCALAR = config['BATTERY_ADC_SCALAR'] # 电池电压缩放因子

    def __init__(self, is_debug=False):
        # 是否开启调试模式
        self.is_debug = is_debug

        self.pin = Pin(BatteryVoltage.BATTERY_ADC_GPIO, Pin.IN) # 电压采样引脚
        self.adc = ADC(self.pin) # 创建引脚对应的ADC对象

        self.bv_sample_cnt = 0 # 统计次数
        self.bv_sample_sum = 0 # 采样电压总和
        self.battery_voltage = 0 # 电池电压 
        # 初始化电池电压
        self.init_battery_voltage()
        # 电池是否过放
        self.is_over_discharge = False # 电池是否过放
    
    def init_battery_voltage(self):
        '''
        初始化，电池电压
        '''
        # 采样BV_SAMPLE_PERIOD次
        for i in range(BatteryVoltage.BATTERY_ADC_SAMPLE_PERIOD):
            self.bv_sample_sum += self.adc.read()
        # 更新电池电压
        self.battery_voltage = self.adc2volt(self.bv_sample_sum/ BatteryVoltage.BATTERY_ADC_SAMPLE_PERIOD)
        # 累加值清零
        self.bv_sample_sum = 0

    def sample(self):
        '''
        定时器回调函数
        '''
        self.bv_sample_cnt += 1 # 计数器自增
        # 采样电池，并累加
        self.bv_sample_sum += self.adc.read()

        if self.bv_sample_cnt >= BatteryVoltage.BATTERY_ADC_SAMPLE_PERIOD:
            # 判断是否满足周期
            self.battery_voltage = self.adc2volt(self.bv_sample_sum/BatteryVoltage.BATTERY_ADC_SAMPLE_PERIOD)
            if self.battery_voltage < BatteryVoltage.BATTERY_OVER_DISCHARGE_VOLT:
                # 电压低于过放电压
                self.is_over_discharge = True
            else:
                self.is_over_discharge = False
            
            # 清零
            self.bv_sample_cnt = 0
            self.bv_sample_sum = 0
            # 打印电池电压Debug信息
            if self.is_debug:
                print("Battery Voltage: {}".format(self.battery_voltage))
                
    @staticmethod
    def adc2volt(value):
        '''
        将ADC采样值（0-BATTERY_ADC_RESOLUTION）转换为实际的电压
        @scalar scalar为放缩因子，取决与电路电阻分压
        '''
        return value / BatteryVoltage.BATTERY_ADC_RESOLUTION * 3.3 * BatteryVoltage.BATTERY_ADC_SCALAR

    def deinit(self):
        '''
        释放资源
        备注 ADC没有deinit方法
        '''
        # 释放ADC资源
        del(self)