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
