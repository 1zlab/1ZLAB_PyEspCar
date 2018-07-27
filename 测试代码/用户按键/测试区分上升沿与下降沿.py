from machine import Pin
import utime

USER_BUTTON = 22
# 引脚
button = Pin(USER_BUTTON, Pin.IN)

# 定义按键按下的值 （取决于按键模块的设计， 有可能相反）
# BTN_DOWN = 0 # 按键按下对应的取值 
# BTN_UP = 1 # 按键抬起对应的状态

counter = 0 # 计数器

def counter_callback(pin):
    '''
    计数器回调函数
    '''
    global counter
    print(pin)
    if pin.value() == 0:
        # 下降沿触发
        print("Falling")
    else:
        # 上升沿触发
        print("Rising")
        
    # 添加软件消抖
    # utime.sleep_ms(150)
    # if pin.value() == 0:
    counter += 1
    print("Counter += 1 ; Counter = %d"%(counter))
    

res = button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=counter_callback)
print(res)
print("按下按键， 会计数哦")

while True:
    # print("do something...")
    utime.sleep_ms(500)