'''
每隔100ms测量一下小车的速度

在预设速度 0-1024 与 100ms内采样数的计数进行映射

问题

电压不变的条件下， 编码器采集的数据不稳定

'''
from Encoder import *
from machine import Timer

# 编码器管脚编号
LEFT_ENCODER_A = 5
LEFT_ENCODER_B = 18
RIGHT_ENCODER_A = 21
RIGHT_ENCODER_B = 19

# 初始化右侧编码器
print('init right encoder')
rm_encoder = Encoder(RIGHT_ENCODER_A, RIGHT_ENCODER_B, is_debug=False)
# 初始或左侧的编码器
print('init left encoder')
lm_encoder = Encoder(LEFT_ENCODER_A, LEFT_ENCODER_B, is_debug=False, name="LeftEncoder", motor_install_dir=False)


def counter2speed(encoder_cnt):
    '''
    编码器计数与速度之间的映射关系
    基于直流电机 转速与电压呈正比的基础假设。
    '''
    pass

def speed_sample(timer):
    '''
    对电机的转度进行采样
    '''
    global lm_encoder
    global rm_encoder
    
    print('LM INTER: {} RM INTER:{}'.format(lm_encoder.inter_cnt, rm_encoder.inter_cnt))
    # 采集左侧电机的编码器数据
    lm_speed = lm_encoder.encoder_cnt
    # 数据清零
    lm_encoder.encoder_cnt = 0
    lm_encoder.inter_cnt = 0 # 中断的总次数

    # 采集右侧电机的编码器数据
    rm_speed = rm_encoder.encoder_cnt
    # 数据清零
    rm_encoder.encoder_cnt = 0
    rm_encoder.inter_cnt = 0

    print('LM Speed: {} RM Speed:{}'.format(lm_speed, rm_speed))
    return lm_speed, rm_speed


# 初始化定时器
timer=Timer(2)
# 这里的周期是每隔多少毫秒执行一次
timer.init(period=1000, mode=Timer.PERIODIC, callback=speed_sample)