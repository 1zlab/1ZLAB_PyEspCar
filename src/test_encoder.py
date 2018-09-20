'''
编码器测试
'''
from machine import Timer
from encoder import Encoder
from button import Button

left_encoder = Encoder(0, is_quad_freq=False)
right_encoder = Encoder(1, is_quad_freq=False)
    
print('Test Encoder')


def encoder_clear(pin):
    '''
    编码器计数清零
    '''
    left_encoder.distance = 0
    right_encoder.distance = 0 
# 创建Button对象
btn = Button(0, encoder_clear)

def print_encoder_info(timer):
    print('Left Distance: {}'.format(left_encoder.distance))
    print('Right Distance: {}'.format(right_encoder.distance))
timer = Timer(4)

# 3s 打印一次数据
timer.init(period=3000, mode=Timer.PERIODIC, callback=print_encoder_info)

def quit():
    # 释放资源
    timer.deinit()
    left_encoder.deinit()
    right_encoder.deinit()
