'''
用户按键
外部中断 切换小车的状态
'''
from machine import Pin
import utime

class UserButton(object):
    '''
    用户按键对象
    '''
    def __init__(self, gpio_id, callback=None):
        # 按键
        self.pin = Pin(gpio_id, Pin.IN)
        # 回调函数
        self.callback = callback
        # 设置外部中断
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler)
        # 标志位 是否处理完成中断
        self.flag = False

    def irq_handler(self, irq_pin):
        '''
        外部中断的相应函数
        '''
        # 添加软件滤波
        utime.sleep_ms(150)
        if self.pin.value() == 0:
            # 将标志位设定为真
            self.flag = True

            if self.callback is not None:
                # 执行回调函数
                self.callback(self.pin)

    def deinit(self):
        self.pin.irq(trigger=0, handler=None)
    

if __name__ == '__main__':
    # from user_button import UserButton
    from car_config import gpio_dict

    # 小车停止标志位
    stop_flag = False

    def callback(pin):
        '''
        回调函数
        改变小车的标志位
        '''
        global stop_flag
        # 标志位取反
        stop_flag = not stop_flag
        print("小车是否停止: {}".format(stop_flag))

    # 用户按键引脚编号
    USER_BUTTON = gpio_dict['USER_BUTTON']
    # 创建UserButton对象
    btn = UserButton(USER_BUTTON, callback)

    try:
        while True:
            pass
    except:
        btn.deinit()
