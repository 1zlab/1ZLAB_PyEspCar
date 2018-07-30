from machine import Timer, Pin
import utime
LEFT_ENCODER_A = 5
LEFT_ENCODER_B = 18
lencode_pin_a = Pin(LEFT_ENCODER_A)
lencode_pin_b = Pin(LEFT_ENCODER_B)

value_a = 0
value_b = 0
posi_cnt = 0
negi_cnt = 0

def encoder_sample(timer):
    '''
    TODO: 改用真值表，改写，简化逻辑判断
    '''
    global lencode_pin_a
    global lencode_pin_b
    global value_a
    global value_b
    global posi_cnt
    global negi_cnt

    new_value_a = lencode_pin_a.value()
    new_value_b = lencode_pin_b.value()
    
    if value_a == 0 and new_value_a == 1:
        # 检测A相上升沿
        print("RISING A,   B:{}".format(new_value_b))
        if new_value_b == 1:
            # 电机正转
            posi_cnt += 1
        else:
            negi_cnt += 1
    elif value_a == 1 and new_value_a == 0:
        # 检测到A相下降沿
        print("FALLING A,   B:{}".format(new_value_b))
        if new_value_b == 0:
            posi_cnt += 1
        else:
            negi_cnt += 1
    elif value_b == 0 and new_value_b == 1:
        # 检测到B相上升沿
        print("RISING B,   A:{}".format(new_value_a))
        if new_value_a == 0:
            # 电机正转
            posi_cnt += 1
        else:
            negi_cnt += 1
        
    elif value_b == 1 and new_value_b == 0:
        # 检测到B相下降沿
        print("FALLING B,   A:{}".format(new_value_a))
        if new_value_a == 1:
            # 电机反转
            posi_cnt += 1
        else:
            negi_cnt += 1

    print('posi_cnt: {}  negi_cnt:{}'.format(posi_cnt, negi_cnt))
    value_a = new_value_a
    value_b = new_value_b    
    # print("value_a: {} value_b: {}".format(value_a, value_b))


# 初始化定时器
timer=Timer(2)
# 定时器 每1ms执行一次
timer.init(period=1, mode=Timer.PERIODIC, callback=encoder_sample)


try:
    while True:
        # print("do something..., counter = %d"%(timer.value()))
        utime.sleep_ms(100)    
except:
    # 必须要有这个try except ,要不然 键盘中段不能让定时器停止
    # 禁用此定时器
    timer.deinit()
