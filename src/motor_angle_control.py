from machine import Timer
from pid import PID

class MotorAngleControl(object):
    '''
    电机的角度控制PID
    使用PID，结合编码器提供的反馈
    每隔100ms采样一次
    '''
    def __init__(self, motor, encoder, kp, ki=0, kd=0, is_debug=False):
        # 电机对象
        self.motor = motor
        # 编码器
        self.encoder = encoder
        # 角度与编码器计数之间的缩放因子
        self.scalar = 1
        # PID对象
        self.pid = PID(kp, ki, kd)
        # 创建定时器
        self.timer = Timer(4)
        # 设置定时器回调 100ms执行一次
        self.timer.init(period=100, mode=Timer.PERIODIC, callback=self.callback)
        # 是否重置计数器
        self.is_reset = False
        
    def count2angle(self, count):
        '''
        将编码器计数转换为角度
        '''
        return count * self.scalar

    def angle2count(angle):
        '''
        将角度转换为编码器计数
        '''
        return angle / self.scalar

    def set_angle(self, angle, is_reset=False):
        '''
        设置电机的旋转角度
        @angle:  电机旋转角度
        @is_continue: 电机是否重新复位
            * False: 不复位的话，计数器不清，
                0度在编码器最初始的位置 
            * True: 如果连续旋转，旋转到特定角度的话，
                编码器计数清零， 目标角度设定为0度,同时is_reset=False
        '''
        self.is_reset = is_reset
        # 设定目标计数
        target_count = self.angle2count(angle)
        if is_reset:
            # 计数器清零
            self.encoder.count = 0
        else:
            # 目标计数器加上之前编码器的值
            target_count += self.encoder.count
        
        # 设置PID的目标取值
        self.pid.set_target_value(target_count)

    def callback(self, timer):
        '''
        回调函数
        '''
        # 获取当前编码器的真实取值
        real_value = self.encoder.count
        # 更新PID
        result = self.pid.update(real_value)
        if self.is_debug:
            print("Target: {} RealValue: {} PID Result: {}".format(self.pid.target_value, self.motor.count, result))
        # 将result转换为电机转速
        pwm = 1*result
        # pwm的值放缩在 正负250-1023之间
        self.motor.set_pwm(pwm)
        
class MotorSpeedPID(object):
    def __init__(self, motor, encoder):
        pass
        