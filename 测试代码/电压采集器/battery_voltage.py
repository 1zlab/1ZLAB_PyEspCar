from machine import Pin,Timer,ADC
import utime

class BatteryVoltage(object):

    def __init__(self, gpio_id):
        self.pin = Pin(gpio_id, Pin.IN)
        self.adc = ADC(self.pin)
        self.init_adc()


    def init_adc(self):
        '''
        初始化ADC
        '''
        # 设定满量程为 3.3v
        self.adc.atten(ADC.ATTN_11DB)
        # 设定取值范围在0-1023
        self.adc.width(ADC.WIDTH_10BIT)
    
    @staticmethod
    def adc2volt(value, scaler=11):
        '''
        将ADC采样值（0-1024）转换为实际的电压
        @scalar scalar为放缩因子，取决与电路电阻分压
        '''
        return value / 1024 * 3.3 * scaler
    