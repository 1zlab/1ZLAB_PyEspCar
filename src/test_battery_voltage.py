'''
测量电池电压
'''
from car_config import gpio_dict
from battery_voltage import BatteryVoltage
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
    timer.deinit()
