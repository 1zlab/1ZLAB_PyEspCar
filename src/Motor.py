'''
驱动电机

speed的范围是-1023 至 1023

电机死区 ：-250 - 250
pwm信号在这个范围是不转的

'''
from machine import Pin,PWM

# 控制右侧电机(正向)
A4950T_AIN1 = 25 # 对应UNO底板 D3
A4950T_AIN2 = 27 # 对应UNO底板 D6

# A4950T 电机驱动引脚 GPIO编号
# 控制左侧电机(反向)
A4950T_BIN1 = 23 # 对应UNO底板 D11
A4950T_BIN2 = 15 # 对应UNO底板 D5

class Motor:
    def __init__(self, gpio_a, gpio_b, motor_install_dir=True, motor_dead_block=250, speed=0):

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
            self.pwm = PWM(self.pin_b, freq=1000)
        else:
            # 电机反向安装
            self.enable_pin = self.pin_b    
            self.pwm = PWM(self.pin_a, freq=1000)
            

        self.motor_dead_block =  motor_dead_block
        self.speed = speed
        self.set_speed(self.speed)

    def stop(self):
        '''
        电机停止转动
        '''
        self.enable_pin.value(0) # 高电平
        # 设置占空比
        self.pwm.duty(0)

    def set_speed(self, speed):
        '''
        设置小车的速度
        '''
        print('set speed: {}'.format(speed))
        if abs(speed) < self.motor_dead_block:
            print("Motor Dead Block: {}".format(speed))
            # speed为电机死区
            self.speed = 0
            self.stop()

        else:
            # 电机正向安装  
            # speed的取值范围 -1000 - 1000
            if speed >= 0:
                self.enable_pin.value(0)
                self.pwm.duty(speed)
            else:
                self.enable_pin.value(1)
                self.pwm.duty(1023 + speed)

