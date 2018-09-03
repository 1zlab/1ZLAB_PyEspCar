
'''
舵机控制的代码

云台下臂舵机： 
    270度舵机  duty范围 24 - 130 中间duty：77
云台上臂舵机: 
    180度舵机  duty范围 30 - 130 中间duty：80
'''
from machine import Pin,PWM
from car_config import car_property

class Servo:
    def __init__(self, pin, angle_range=180, min_duty=30, max_duty=130, default_angle=90):
        '''
        构造器函数
        '''
        self.pin = pin # 舵机管脚
        self.pwm = PWM(pin, freq=car_property['PWM_FREQUENCY']) # 创建一个PWM的对象
        self.angle_range = angle_range # 舵机旋转角度范围
        self.default_angle = default_angle # 默认的角度
        self.min_duty = min_duty # 最小占空比
        self.max_duty = max_duty # 最大占空比
        self._angle =  default_angle
        self.angle(default_angle)

    def angle(self, target_angle):
        if target_angle is None:
            # 返回当前的角度值
            return self._angle
        
        # 角度范围判断
        target_angle = target_angle if target_angle > 0 else 0
        target_angle = target_angle if target_angle < self.angle_range else self.angle_range 
        
        # 计算PWM
        target_duty = int(self.min_duty + (self.max_duty - self.min_duty) * ( target_angle / self.angle_range)) 
        # 打印占空比
        print('Target Duty: {}'.format(target_duty))
        self.pwm.duty(target_duty)
        self._angle = target_angle

    def deinit(self):
        '''
        资源释放
        '''
        self.pwm.deinit()

