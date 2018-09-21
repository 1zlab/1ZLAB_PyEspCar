'''

电机的PID控制(角度，速度)

TODO 增量式PID 速度减到0的时候， PWM可能处在电机的死区位置



'''
from pyb import Timer
from pid import IncrementalPID
from config import config
import math


class MotorSpeedControl(object):
    '''电机速度PID控制'''
    MOTOR_SPEED_PID_CTL_PERIOD = config['MOTOR_SPEED_PID_CTL_PERIOD']
    MOTOR_MAX_SPEED = config['CAR_MAX_SPEED']

    def __init__(self, motor, encoder, kp, ki=0, kd=0, is_debug=False):
        self.is_debug = is_debug # 是否开启调试模式
        self.stop_flag = False # 停止标志位

        self.motor = motor # 电机
        self.encoder = encoder # 编码器
        self.encoder.reset() # 重置编码器
        self.pid = IncrementalPID(kp, ki, kd, min_result=-100, max_result=100) # 创建PID对象 最大输出是百分比
        self._mvdis = 0 # 电机旋转速度(控制周期内的电机前进距离)
        
        self._iteration = 0 # PID迭代次数
        self.target_pwm = 0
        self.max_speed = 0
    
    def reset(self):
        '''电机速度控制类重置'''
        self.motor.stop()
        self.encoder.reset()
        self.pid.reset()
        self.speed = 0
        self._iteration = 0

    def is_legal_speed(self, value):
        '''判断speed是否合法'''

        if abs(value) > MotorSpeedControl.MOTOR_MAX_SPEED:
            return False
        return True
    
    def distance2speed(self, value):
        return value / MotorSpeedControl.MOTOR_SPEED_PID_CTL_PERIOD

    @property
    def speed(self):
        return self.distance2speed(self._mvdis)

    @speed.setter
    def speed(self, value):
        
        if not self.is_legal_speed(value):
            # 判断速度value是否合法
            print('[ERROR] Invalid Motor Speed (m/s) Max Speed: {}'.format(MotorSpeedControl.MOTOR_MAX_SPEED))
            return
        
        # 计算出speed相对控制周期内的前进距离
        value = value * MotorSpeedControl.MOTOR_SPEED_PID_CTL_PERIOD 
        # 设置目标值
        self.pid.target = value
    
    def update(self):
        '''
        回调函数
        '''        
        cur_speed = self.encoder.distance / MotorSpeedControl.MOTOR_SPEED_PID_CTL_PERIOD 

        # 读取一段时间内， 真实的电机旋转角度
        if self.is_legal_speed(cur_speed):
            # 从编码器测得速度
            # 低通滤波器
            self._mvdis = self._mvdis * 0.8 + self.encoder.distance * 0.2

        self.encoder.reset()  # 重置编码器计数

        # 更新PID 获取新的PWM控制信号
        motor_pwm = self.pid.update(self._mvdis) 
        
        if not self.stop_flag:
            self.motor.speed = motor_pwm
        else:
            # 电机停止旋转
            self.motor.pwm(0)

        if self.is_debug:
            self._iteration += 1
            if self._iteration > 40:
                # 1s 打印一次
                self._iteration = 0
                print('Target Speed: {} , Real Speed: {}'.format(self.distance2speed(self.pid.target), self.speed))
                print('Motor PWM: {}'.format(motor_pwm))

    def deinit(self):
        self.encoder.deinit()
        self.motor.deinit()
        del(self)

