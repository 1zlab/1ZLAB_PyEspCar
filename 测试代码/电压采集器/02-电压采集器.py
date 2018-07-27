'''
电压采集器与电池过放检测
------------------------
读取电池电压
IO35 - 电压采集
定时器 -> 定时执行(更新)

航模电池 需要监控电池的电压
满电或者过放都不好
需要检测电压值是否低于某个特定的值, 如果低于的话, 电机停止工作.

锂电池型号: 2s 1900mah航模电池
淘宝链接: https://item.taobao.com/item.htm?id=555741665253
标准电压: 7.4v
过放: 6.4v

充电所需时间, 大概是1h
TODO 添加航模电池过放检测 好险!
TODO 尝试采样2000次, 电池采样 20s/次
TODO 充满电在6.8v左右 ?

'''
from machine import ADC,Pin,Timer
import utime


#define BATTERY_VOLTAGE_SAMPLE_PERIOD 200 // 采样周期
#define BATTERY_MIN_VOLTAGE 750 // 最小电量

battery_vol = None # 真实的航模电池的电压值 

'''
1. 初始化电压采集模块
'''
# 设置GPIO35号引脚作为ADC采样引脚
# 电池电压引脚 battery voltage pin
bv_pin = Pin(35,Pin.IN)
# 声明ADC对象 
bv_adc = ADC(bv_pin)
# 设定满量程为 3.3v
bv_adc.atten(ADC.ATTN_11DB)
# 取值范围 0-1023
bv_adc.width(ADC.WIDTH_10BIT)


'''
2. ADC采样数值还原为真实的电压

'''
def calculate_volatage(adc_val):
    # 根据精密电阻电池电压测量模块说明
    # adc_val的取值范围为 0-1024 (ADC.WIDTH_10BIT)
    return adc_val / 1024 * 3.3 * 11


'''
3. 采集电压信息
定时器周期采样, 最后取平均
这部分后面可以封装在 面向对象的静态方法里面
'''
BV_SAMPLE_PERIOD = 2000 # 采样次数为2000, 
bv_sample_num = 0
bv_sum = 0
def bv_sample(timer):
    global bv_adc
    global BV_SAMPLE_PERIOD
    global battery_vol
    global bv_sample_num
    global bv_sum
    bv_sum += bv_adc.read() # 读取采样值
    bv_sample_num += 1
    
    if bv_sample_num >= BV_SAMPLE_PERIOD:
        bv_value = bv_sum / BV_SAMPLE_PERIOD
        # 更新航模电池电压值
        print("bv: {}".format(bv_value))
        battery_vol = calculate_volatage(bv_value)
        print("电池电压: {}".format(battery_vol))
        # 清零
        bv_sample_num = 0 
        bv_sum = 0
        
# InitTimer use timer 1
timer=Timer(1)
timer.init(period=1, mode=Timer.PERIODIC, callback=bv_sample)

try:
    while True:
        # print("do something..., counter = %d"%(timer.value()))
        utime.sleep_ms(100)    
except:
    # 必须要有这个try except ,要不然 键盘中段不能让定时器停止
    # 禁用此定时器
    timer.deinit()
