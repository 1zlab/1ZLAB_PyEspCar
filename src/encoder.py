from machine import Timer, Pin
import utime

class Encoder(object):
    '''
    编码器对象
    '''
    def __init__(self, gpio_a, gpio_b, timer_id, name='RightEncoder', 
                motor_install_dir=True, is_debug=False):
        
        # 设置编码器的名称
        self.name = name
        # 根据电机安装方向，设置AB相Pin
        if motor_install_dir:
            self.pin_a = Pin(gpio_a)
            self.pin_b = Pin(gpio_b)
        else:
            self.pin_a = Pin(gpio_b)
            self.pin_b = Pin(gpio_a)
        
        # 最近一次A相的电平
        self.last_a = 0
        # 最近一次B相的电平
        self.last_b = 0
        # 新的A相电平
        self.new_a = 0
        # 新的B相电平 
        self.new_b = 0
        # 定时器计数
        self.count = 0
        # 定时器
        self.timer = Timer(timer_id)
        # 定时器 每1ms执行一次
        self.timer.init(period=1, mode=Timer.PERIODIC, callback=self.callback)
        
        # 是否开启Debug模式
        self.is_debug = is_debug
        
    def callback(self,timer):
        '''
        回调函数
        '''
        # 更新A相电平
        self.new_a = self.pin_a.value()    
        # 更新B相电平
        self.new_b = self.pin_b.value()
        
        if not self.last_a and self.new_a:
            # 检测到编码器A相上升沿 RISING
            if self.new_b:
                self.count -= 1
            else:
                self.count += 1
        elif self.last_a and not self.new_a:
            # 检测到编码器A相下降沿 FALLING
            if self.new_b:
                self.count += 1
            else:
                self.count -= 1 
        elif not self.last_b and self.new_b:
            # 检测到编码器B相上升沿 RASING
            if self.new_a:
                self.count += 1
            else:
                self.count -= 1
        elif self.last_b and not self.new_b:
            # 检测到编码器B相下降沿 FALLING
            if self.new_a:
                self.count -= 1
            else:
                self.count += 1
        if self.is_debug:
            # 打印计数器信息
            if self.last_a != self.new_a or self.last_b != self.new_b:
                # 计数器变换再打印
                print('{} Counter: {}'.format(self.name, self.count))
                print('last_a:{} new_a:{} last_b:{} new_b: {}'.format(self.last_a, self.new_a, self.last_b, self.new_b))
        # 更新电平历史
        self.last_a = self.new_a
        self.last_b = self.new_b