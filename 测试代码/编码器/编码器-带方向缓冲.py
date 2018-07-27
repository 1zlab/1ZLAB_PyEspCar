from machine import Pin

'''
这个算法最后实际测试效果比较好

AB相位 随意接线

左右侧电机刚好相反
'''
print('test main')

# 右侧编码器
pina = Pin(13) # uno底板 pin7
pinb = Pin(12) # uno底板 pin2

# 左侧编码器
# pina = Pin(14) # uno底板 pin8
# pinb = Pin(27) # uno底板 pin4
# pina = Pin(27) # uno底板 pin8
# pinb = Pin(14) # uno底板 pin4

posi_cnt = 0 # 编码器累积计数
inter_cnt = 0 # 记录中断的次数

motor_dir = 1 # 电机的方向 1 / -1
lazy_motor_dir_cnt = 0


def callback(pin):
    global posi_cnt
    global inter_cnt
    global motor_dir
    global lazy_motor_dir_cnt

    a_value = pina.value()
    
    last_b = pinb.value()
    b_count = 0

    while True:
        new_b = pinb.value()
        if new_b == last_b:
            b_count += 1
        else:
            last_b = new_b
            b_count = 0 
        if b_count >= 5:
            break
    print('-------------------------------------------------')
    print('interupt pin: {}'.format(pin))
    print("PinA: {} PinB: {}".format(a_value, last_b))

    if a_value == last_b:
        # 电机正转
        motor_dir = 1
    else:
        motor_dir = -1
    
    print("raw motor dir: {}".format(motor_dir))

    # 约束lazy motor dir 的边界
    lazy_motor_dir_cnt += motor_dir
    if lazy_motor_dir_cnt > 10:
        lazy_motor_dir_cnt = 10
    elif lazy_motor_dir_cnt < -10:
        lazy_motor_dir_cnt = -10

    # 对motor_dir 重新赋值
    if lazy_motor_dir_cnt > 0:
        motor_dir = 1
    elif lazy_motor_dir_cnt < 0:
        motor_dir = -1
    
    print("motor_dir : {} lazy_dir: {}".format(motor_dir, lazy_motor_dir_cnt))
    posi_cnt += motor_dir
    inter_cnt += 1
    print("posi: {} inter: {}".format(posi_cnt, inter_cnt))
    
    print('-------------------------------------------------')

pina.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler = callback)
pinb.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler = callback)


