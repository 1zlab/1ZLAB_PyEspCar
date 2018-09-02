'''
电机的PID控制(角度，速度)

TODO test PID Speed Control
'''
from machine import Timer
from pid import PID

class MotorAngleControl(object):
    '''
    电机旋转角度PID控制
    PID：  P比例 I 积分(惯性力) D微分(阻尼力)
    使用PID，结合编码器提供的反馈
    每隔100ms采样一次
    '''
    def __init__(self, motor, encoder, kp, ki=0, kd=0, is_debug=False):
        # 电机对象
        self.motor = motor
        # 编码器
        self.encoder = encoder
        # 初始化编码器的计数
        self.encoder._pos = 0
        # PID对象
        self.pid = PID(kp, ki, kd)
        # 是否开启调试模式
        self.is_debug = is_debug
        
        if is_debug:
            # 迭代次数计数
            self._iteration = 0
        
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
        # 设定目标计数
        target_count = angle

        if is_reset:
            # 电机角度重置，计数器清零
            self.encoder._pos = 0
            # 目标计数器加上之前编码器的值
            target_count += self.encoder.position
        
        # 设置PID的目标取值
        self.pid.set_target_value(target_count)

    def callback(self, timer, min_threshold=1):
        '''回调函数'''
        # 获取当前编码器的真实取值
        real_value = self.encoder.position   
        # 更新PID
        pwm = self.pid.update(real_value)
        if abs(real_value - self.pid.target_value) < min_threshold:
            pwm = 0
        # pwm的值放缩在 正负250-1023之间
        # 为了准确，这里需要限定一下速度
        if abs(pwm) > 350:
            pwm = 350 if pwm > 0 else -350
        
        self.motor.set_pwm(int(pwm))
        
        if self.is_debug:
            self._iteration += 1
            if self._iteration > 10:
                # 1s 打印一次
                self._iteration = 0
                print("Target: {} RealValue: {} PID Result: {}".format(self.pid.target_value, self.encoder.position, pwm))
                print('PWM: {}'.format(pwm))
    
    def deinit(self):
        '''销毁资源'''
        self.encoder.deinit()
        self.motor.deinit()
    
class MotorSpeedPID(object):
    '''电机速度PID控制'''
    def __init__(self, motor, encoder, kp, ki=0, kd=0, scale=1, is_debug=False):
        self.motor = motor # 电机
        self.encoder = encoder # 编码器
        self.encoder._pos = 0 # 编码器初始化
        self.pid = PID(kp, ki, kd) # 创建PID对象
        self._speed = 0 # 电机旋转速度

        self.is_debug = is_debug
        if self.is_debug:
            self._iteration = 0 # 迭代次数

    def speed(self, target_speed):
        '''
        设置速度
        '''
        if target_speed is None:
            # 返回当前的速度
            return self._speed
        
        # 设置pid目标值
        self.pid.target_value = target_speed
    
    def callback(self, timer, min_threshold=1):
        '''
        回调函数
        '''
        real_value = self.encoder.position # 读取一段时间内， 真实的电机旋转角度
        self._speed = real_value # 更新速度值
        pwm = self.pid.update(real_value) # 更新PID
        if abs(real_value - self.pid.target_value) < min_threshold:
            pwm = 0
        self.motor.set_pwm(int(pwm))
        
        # 编码器清零
        self.encoder._pos = 0
        if self.is_debug:
            self._iteration += 1
            if self._iteration > 10:
                # 1s 打印一次
                self._iteration = 0
                print("Target: {} RealValue: {} PID Result: {}".format(self.pid.target_value, self._speed, pwm))
                print('PWM: {}'.format(pwm))
        

