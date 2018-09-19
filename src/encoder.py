'''
AB相正交编码器类
'''
from machine import Pin

class Encoder(object):
    def __init__(self, pin_x, pin_y, reverse, scale, motor=None, is_four_freq=False):
        self.reverse = reverse
        self.scale = scale
        self.forward = True
        self.pin_x = pin_x
        self.pin_y = pin_y
        self._pos = 0

        if is_four_freq:
            self.x_interrupt = pin_x.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.x_callback)
            self.y_interrupt = pin_y.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.y_callback)
        else:
            self.x_interrupt = pin_x.irq(trigger=Pin.IRQ_RISING, handler=self.x_callback)
        self.motor = motor
    def x_callback(self, line):
        if self.motor is not None:
            if self.motor.pwm() > 0:
                self._pos += 1
            else:
                self._pos -= 1
        else:
            self.forward = self.pin_x.value() ^ self.pin_y.value() ^ self.reverse
            self._pos += 1 if self.forward else -1

    def y_callback(self, line):
        if self.motor is not None:
            if self.motor.pwm() > 0:
                self._pos += 1
            else:
                self._pos -= 1
        else:
            self.forward = self.pin_x.value() ^ self.pin_y.value() ^ self.reverse ^ 1
            self._pos += 1 if self.forward else -1

    @property
    def position(self):
        return self._pos * self.scale

    @position.setter
    def position(self, value):
        self._pos = value // self.scale
        
    
    def deinit(self):
        '''
        资源释放
        '''
        # 注销引脚的IRQ
        self.pin_x.irq(trigger=0, handler=None)
        self.pin_y.irq(trigger=0, handler=None)

if __name__ == '__main__':

    '''
    编码器测试
    -------------------------
    注意： print频次不能高，会影响计数

    电机旋转一圈 A B相各 11个脉冲
    减速比为1:30, 同时因为采用了四倍频技术,
    所以轮子旋转一圈对应 11 * 4 * 30 = 1320个脉冲

    电机旋转一周的计数是1320， 折算成360度角度，
    对应的scale = 360/1320 = 3 / 11

    '''
    from machine import Pin,Timer
    import time
    # from encoder import Encoder
    from user_button import UserButton
    from car_config import gpio_dict, car_property


    left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
    left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
    left_encoder = Encoder(left_pin_a, left_pin_b,
        reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
        scale=1)

    right_pin_a = Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN)
    right_pin_b = Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN)
    right_encoder = Encoder(right_pin_a, right_pin_b,
        reverse=car_property['RIGHT_ENCODER_IS_REVERSE'],
        scale=1)
        
    print('Test Encoder')

    def callback(timer):
        print('Left Angle: {}'.format(left_encoder.position))
        print('Right Angle: {}'.format(right_encoder.position))


    def encoder_clear(pin):
        '''
        编码器计数清零
        '''
        left_encoder.position = 0
        right_encoder.position = 0 

    # 用户按键引脚编号
    USER_BUTTON = gpio_dict['USER_BUTTON']
    # 创建UserButton对象
    btn = UserButton(USER_BUTTON, encoder_clear)

    timer = Timer(4)
    # 3s 打印一次数据
    timer.init(period=1000, mode=Timer.PERIODIC, callback=callback)


    def quit():
        # 释放资源
        timer.deinit()
        left_encoder.deinit()
        right_encoder.deinit()

    # TODO 添加另外一个退出按键， 执行quit函数