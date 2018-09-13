'''
对电池电压进行采样
-------------------
航模电池需要监控电池的电压
满电或者过放都不好,需要检测电压值是否低于某个特定的值, 
如果低于的话, 电机停止工作.
'''
from machine import Pin,Timer,ADC
import utime

class BatteryVoltage(object):
    
    def __init__(self, gpio_id, is_debug=False):
        self.BV_SAMPLE_PERIOD = 100 # 采样周期(次数)为2000次
        self.OVER_DISCHARGE_VOLTAGE = 6.4 # 过放电压参考值
        self.pin = Pin(gpio_id, Pin.IN) # 电压采样引脚
        self.adc = ADC(self.pin) # 创建引脚对应的ADC对象
        self.init_adc() # 初始化ADC
        
        self.bv_sample_cnt = 0 # 统计次数
        self.bv_sample_sum = 0 # 采样电压总和
        self.battery_voltage = 0 # 电池电压 
        # 初始化电池电压
        self.init_battery_voltage()
        # 创建一个定时器
        # self.timer = Timer(timer_id) 
        # 每隔1ms执行一次
        # self.timer.init(period=1, mode=Timer.PERIODIC, callback=self.callback)
        # 电池是否过放
        self.is_over_discharge = False # 电池是否过放
        # 是否开启调试模式
        self.is_debug = is_debug
    def init_adc(self):
        '''
        初始化ADC
        '''
        # 设定满量程为 3.3v
        self.adc.atten(ADC.ATTN_11DB)
        # 设定取值范围在0-1023
        self.adc.width(ADC.WIDTH_10BIT)
    
    def init_battery_voltage(self):
        '''
        初始化，电池电压
        '''
        # 采样BV_SAMPLE_PERIOD次
        for i in range(self.BV_SAMPLE_PERIOD):
            self.bv_sample_sum += self.adc.read()
        # 更新电池电压
        self.battery_voltage = self.adc2volt(self.bv_sample_sum/self.BV_SAMPLE_PERIOD)
        # 累加值清零
        self.bv_sample_sum = 0

    def callback(self, timer):
        '''
        定时器回调函数
        '''
        self.bv_sample_cnt += 1 # 计数器自增
        # 采样电池，并累加
        self.bv_sample_sum += self.adc.read()

        if self.bv_sample_cnt >= self.BV_SAMPLE_PERIOD:
            # 判断是否满足周期
            self.battery_voltage = self.adc2volt(self.bv_sample_sum/self.BV_SAMPLE_PERIOD)
            if self.battery_voltage < self.OVER_DISCHARGE_VOLTAGE:
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
    def adc2volt(value, scaler=11):
        '''
        将ADC采样值（0-1024）转换为实际的电压
        @scalar scalar为放缩因子，取决与电路电阻分压
        '''
        return value / 1024 * 3.3 * scaler

    def deinit(self):
        '''
        释放资源
        备注 ADC没有deinit方法
        '''
        # 释放ADC资源
        # self.adc.deinit()
        pass


if __name__ == '__main__':
    '''
    测量电池电压
    '''
    from car_config import gpio_dict
    # from battery_voltage import BatteryVoltage
    from machine import Timer

    bv = BatteryVoltage(gpio_dict['BATTERY_ADC'], is_debug=True)
    # 创建一个定时器
    timer = Timer(1) 
    # 每隔100ms执行一次 10s 判断一次电池电压是否过放
    timer.init(period=100, mode=Timer.PERIODIC, callback=bv.callback)

    try:
        while True:
            pass
    except:
        # 释放定时器资源
        timer.deinit()
        # 释放ADC资源
        bv.deinit()
