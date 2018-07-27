'''
编码器类

TODO 采用概率学的手段来处理噪声。
TODO (小葱)修改底板电路 增加电容进行滤波 (实在不稳， 需要自己改)

备注： 目前软件滤波 比较稳定， 但是反向切换的时候有延迟（改用线性增，指数减？）

目前调的参数可以满足需求
主要是下面这两个参数
* MAX_LAZY_DIR_CNT
* MIN_EQUAL_CNT

TODO 计算编码器 相位差 AB
TODO Pin改为上拉模式 PULL_UP

A相 上升沿 -> B相 高电平  电机正转
A相 下降沿 -> B相 低电平  电机正转

TODO：如何区分是上升沿还是下降沿产生的事件？

'''
from machine import Pin 
import micropython
import utime
# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)

class Encoder:
    '''
    编码器 类
    '''
    def __init__(self, gpio_a, gpio_b, motor_install_dir=True, is_debug=False, name='RightEncoder'):
        self.name = name # 编码器的名字
        self.pin_a = Pin(gpio_a, Pin.IN, Pin.PULL_UP) # 编码器A相 输入模式 上拉电阻
        self.pin_b = Pin(gpio_b, Pin.IN, Pin.PULL_UP) # 编码器B相 输入模式 上拉电阻
        self.value_a = 0 # 最近一次a相位的电平
        self.value_b = 0 # 最近一次b相位的电平
        self.motor_install_dir = motor_install_dir # 电机的安装位置 (正向安装还是反向安装)
        self.encoder_cnt = 0  # 编码计数器 
        self.inter_cnt = 0 # 中断的总次数
        self.motor_dir = True # 电机转向
                              # True 正转 False 反转
        # 设置外部中断与回调函数
        self.pin_a.irq(trigger= Pin.IRQ_RISING, handler = self.irq_callback)
        # self.pin_a.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler = self.irq_callback)
        # self.pin_b.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler = self.irq_callback)

        self.is_debug = is_debug

    def get_motor_rotate_dir(self, irq_pin):
        '''
        判断电机的旋转方向
            - add_filter: 是否添加滤波
        '''
        ''''
        # 中断的引脚采样
        # 1 -> 上升沿触发
        # 0 -> 下降沿触发
        irq_pin_value = irq_pin.value()
        # 判定是否为irq 上升沿触发
        is_irq_rising = irq_pin_value == 1

        dir_pin = None # 代表方向的引脚
        # 查看引发中断的引脚是哪个，
        # 选择另外一个引脚作为方向判定引脚
        if irq_pin == self.pin_a:
            dir_pin = self.pin_b
        else:
            dir_pin = self.pin_a
        
        # 对方向引脚进行采样
        dir_pin_value = dir_pin.value()

        # 更新电平值
        if irq_pin == self.pin_a:
            self.value_a,self.value_b = irq_pin_value, dir_pin_value
        else:
            self.value_a,self.value_b = dir_pin_value, irq_pin_value
        


        # 电机方向判定
        motor_dir = None
        if is_irq_rising:
            # 上升沿触发
            if dir_pin_value == 1:
                motor_dir = True # 电机正转
            else:
                motor_dir = False # 电机反转
        else:
            # 下降沿触发
            if dir_pin_value == 0:
                motor_dir = True # 电机方向
            else:
                motor_dir = False
            
        # 判断两个电平是否相等
        if self.motor_install_dir == False:
            # 如果电机安装方向相反的话， 方向也相反
            motor_dir = not motor_dir

        self.motor_dir = motor_dir

        return motor_dir
        '''
        self.value_a = self.pin_a.value()
        # 添加软件消抖
        utime.sleep_ms(20)
        self.value_b = self.pin_b.value()
        if self.value_b == 1:
            self.motor_dir = True
        else:
            self.motor_dir = False
            
        return self.motor_dir
    def update_encoder_cnt(self):
        '''
        更新编码器的计数
        '''
        if self.motor_dir:
            # 如果是正向旋转
            self.encoder_cnt += 1
        else:
            self.encoder_cnt -= 1
        

    def irq_callback(self, irq_pin):
        '''
        电平发生跳变的时候 产生的中断回调函数
        '''
        # 获取编码器旋转方向
        self.get_motor_rotate_dir(irq_pin)
        # 更新编码器计数
        self.update_encoder_cnt()

        # 中断次数 +1
        self.inter_cnt += 1
        if self.is_debug:
            print("interupt pin: {}".format(irq_pin))
            # 打印编码器自身
            print(self)

    def __str__(self):
        '''
        打印编码器信息
        '''
        print('=====================Interupt ID: {}========================'.format(self.inter_cnt))
        print("Encoder: {}".format(self.name))
        print("PinA: {} Value： {}， PinB： {} Value： {}".format(self.pin_a, self.value_a, 
                self.pin_b, self.value_b))
        print("Motor Dir : {} ".format(self.motor_dir))
        print("Encoder Count: {}".format(self.encoder_cnt))
        print('=============================================\n\n')

