from machine import Timer
from pid import PID

class MotorAngleControl(object):
    '''
    电机旋转角度PID控制
    使用PID，结合编码器提供的反馈
    每隔100ms采样一次
    '''
    def __init__(self, motor, encoder, kp, ki=0, kd=0, is_debug=False):
        # 电机对象
        self.motor = motor
        # 编码器
        self.encoder = encoder
        self.encoder.count = 0
        # 角度与编码器计数之间的缩放因子
        self.scalar = 1
        # PID对象
        self.pid = PID(kp, ki, kd)
        # 创建定时器 
        # TODO 这里用的是定时器4
        self.timer = Timer(4)
        # 设置定时器回调 100ms执行一次
        # TODO 测试10ms更新一次
        self.timer.init(period=10, mode=Timer.PERIODIC, callback=self.callback)
        # 是否重置计数器
        self.is_reset = False
        # 是否开启调试模式
        self.is_debug = is_debug

    def count2angle(self, count):
        '''
        将编码器计数转换为角度
        '''
        return count * self.scalar

    def angle2count(self, angle):
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
        
        # 将result转换为电机转速
        pwm = self.scalar*result
        # pwm的值放缩在 正负250-1023之间
        # TODO ? pwm 也可以是0啊
        if abs(pwm) > 300:
            if pwm > 0:
                pwm = 300
            elif pwm < 0:
                pwm = -300
        '''
        elif abs(pwm) > 10 and abs(pwm) < 250:
            if pwm > 0:
                pwm = 250
            elif pwm < 0:
                pwm = -250
        '''
        
        self.motor.set_pwm(int(pwm))
        if self.is_debug:
            print("Target: {} RealValue: {} PID Result: {}".format(self.pid.target_value, self.encoder.count, result))
            print('PWM: {}'.format(pwm))

        
        
class MotorSpeedPID(object):
    '''
    电机速度PID控制
    '''
    def __init__(self, motor, encoder):
        pass
        