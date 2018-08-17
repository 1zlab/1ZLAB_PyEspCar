'''
驱动电机

pwm的范围是-1023 至 1023

备注：电机死区 ：-250 - 250， pwm信号在这个范围是不转的
'''
from machine import Pin,PWM

class Motor:
    def __init__(self, gpio_a, gpio_b, motor_install_dir=True, motor_dead_block=250, pwm=0):

        # 电机安装方向
        self.motor_install_dir = motor_install_dir
        # A相引脚
        self.pin_a = Pin(gpio_a, Pin.OUT)
        # B相引脚
        self.pin_b = Pin(gpio_b, Pin.OUT)
        
        # pwm引脚用户控制电机转速
        if motor_install_dir:
            # 电机正向安装
            self.enable_pin = self.pin_a      
            self.pwm_pin = PWM(self.pin_b, freq=1000)
        else:
            # 电机反向安装
            self.enable_pin = self.pin_b    
            self.pwm_pin = PWM(self.pin_a, freq=1000)
            

        self.motor_dead_block =  motor_dead_block
        self.pwm = pwm
        self.set_pwm(self.pwm)

    def stop(self):
        '''
        电机停止转动
        '''
        self.enable_pin.value(0) # 高电平
        # 设置占空比
        self.pwm_pin.duty(0)

    def set_pwm(self, pwm):
        '''
        设置小车的速度
        '''
        # print('set pwm: {}'.format(pwm))
        if abs(pwm) < self.motor_dead_block:
            # print("Motor Dead Block: {}".format(pwm))
            # pwm为电机死区
            # self.pwm = 0
            # self.stop()
            
            # pwm为电机死区
            if pwm <  0:
                pwm = -1*self.motor_dead_block
            else:
                pwm = self.motor_dead_block
            
        if abs(pwm) > 1023:
            # 判断pwm的绝对值是否
            if pwm <  0:
                pwm = -1023
            else:
                pwm = 1023
        self.pwm = pwm
        # 电机正向安装  
        # pwm的取值范围 -1023 - 1023
        if pwm >= 0:
            self.enable_pin.value(0)
            self.pwm_pin.duty(pwm)
        else:
            self.enable_pin.value(1)
            self.pwm_pin.duty(1023 + pwm)

