# 中断测试

'''
单个的IRQ就有很多噪声

问题已解决

http://docs.micropython.org/en/v1.9.2/esp8266/library/machine.Pin.html?highlight=irq#machine.Pin.irq

测试效果： 正转 二者电平相同， 反转 相反

'''
from machine import Pin

print('test main')

# 右侧编码器
# pina = Pin(13) # uno底板 pin7
# pinb = Pin(12) # uno底板 pin2

# 左侧编码器
# pina = Pin(14) # uno底板 pin8
# pinb = Pin(27) # uno底板 pin4
pina = Pin(27) # uno底板 pin8
pinb = Pin(14) # uno底板 pin4

posi_cnt = 0 # 编码器累积计数
inter_cnt = 0 # 记录中断的次数

motor_dir = 1 # 电机的方向 1 / -1

lazy_dir = 0
def callback(pin):
    global posi_cnt
    global inter_cnt
    global motor_dir

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
    
    print("PinA: {} PinB: {}".format(a_value, last_b))

    if a_value == last_b:
        # 电机正转
        motor_dir = 1
    else:
        motor_dir = -1
    
    posi_cnt += motor_dir
    inter_cnt += 1
    print("posi: {} inter: {}".format(posi_cnt, inter_cnt))
    

pina.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler = callback)


