'''
文档
http://docs.micropython.org/en/latest/pyboard/library/pyb.Timer.html?highlight=encoder


可用与Timer的ID为： 2, 4
Timer.ENC 只能配置在Timer的CH1还有CH2上面


'''
from machine import Pin
from pyb import Timer


# gpio_x = 'X1'
# gpio_y = 'X2'
# timer_id = 2

gpio_x = 'X9'
gpio_y = 'X10'
timer_id = 4


# X1： TIM2 CH1
pin_x = Pin(gpio_x, Pin.AF_PP, pull=Pin.PULL_NONE, af = Pin.AF1_TIM2)  # 编码器A相
# X2： TIM2 CH2
pin_y = Pin(gpio_y, Pin.AF_PP, pull=Pin.PULL_NONE, af = Pin.AF1_TIM2 ) # 编码器B相
encoder_timer = Timer(timer_id, prescaler=0, period=13439)

'''
channel num 会被忽略
mode: 
    1. Timer.ENC_A: Channel1 变换 -> 计数器变化 
    2. Timer.ENC_B: Channel2 变换 -> 计数器变化
    3. Timer.ENC_AB: channel1或channel2变换 -> 计数器变化
'''
encoder_timer.channel(1, Timer.ENC_A)

# channel2 = encoder_timer.cha
