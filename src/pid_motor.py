'''

电机的PID控制(角度，速度)

TODO 增量式PID 速度减到0的时候， PWM可能处在电机的死区位置



'''
from machine import Timer
from pid import IncrementalPID
from car_config import car_property
import math


class MotorSpeedControl(object):
    '''电机速度PID控制'''
    def __init__(self, motor, encoder, kp, ki=0, kd=0, is_debug=False):
        self.motor = motor # 电机
        self.encoder = encoder # 编码器
        self.encoder.position = 0 # 编码器初始化

        self.pid = IncrementalPID(kp, ki, kd, min_result=-1023, max_result=1023) # 创建PID对象
        self._speed = 0 # 电机旋转速度

        self.stop_flag = False
        self.is_debug = is_debug
        self._iteration = 0 # PID迭代次数
        self.target_pwm = 0
        self.max_speed = 0
        self.set_max_speed()

    def set_max_speed(self):
        self.max_speed = car_property['CAR_MAX_SPEED'] / (2*math.pi*car_property['WHEEL_RADIUS'])
        self.max_speed *= car_property['WHEEL_TAKE_A_CIRCLE_PULSE']
        self.max_speed *= car_property['PID_CTL_PERIOD']

    def init(self):
        '''
        重新初始化
        '''
        self.encoder.position = 0        
        self._iteration = 0
        # 重新初始化PID
        self.pid.reset()

    def speed(self, value=None):
        '''
        设置速度
        '''
        if value is None:
            # 返回当前的速度
            return self._speed
        # 规约target ,计算控制周期内电机最大的target
        max_target = int(car_property['MOTOR_MAX_ANGLE']*car_property['PID_CTL_PERIOD'])

        if abs(value) > max_target:
            value = max_target if value > 0 else -1 * max_target 

        

        # 设置pid目标值
        self.pid.target(value)

    def is_legal_speed(self, encoder_value):
        '''
        判断编码器的速度是否合理
        '''
        if self.motor.pwm() > 0 and encoder_value > self.max_speed:
            return False
        elif self.motor.pwm() < 0 and encoder_value < -self.max_speed:
            return False
        
        return True
        

    def callback(self, timer, min_threshold=1):
        '''
        回调函数
        '''
        # 读取一段时间内， 真实的电机旋转角度
        if self.is_legal_speed(self.encoder.position):
            # 从编码器测得速度
            # 低通滤波器
            self._speed = self._speed * 0.8 + self.encoder.position * 0.2
        # 编码器清零
        self.encoder.position = 0
        # 更新PID 获取新的PWM控制信号
        pwm = self.pid.update(self._speed) 
        self.target_pwm = pwm
        if not self.stop_flag:
            # self.motor.pwm(int(pwm))
            pass
        else:
            # 电机停止旋转
            self.motor.pwm(0)

        if self.is_debug:
            self._iteration += 1
            if self._iteration > 40:
                # 1s 打印一次
                self._iteration = 0
                print("Target: {} RealValue: {} PID Result: {}".format(self.pid.target(), self._speed, pwm))
                print('PWM: {}'.format(pwm))

    def deinit(self):
        self.encoder.deinit()
        self.motor.deinit()

if __name__ == '__main__':
    '''
    测试电机速度控制
    '''
    import micropython
    from  machine import Pin,Timer
    import utime

    from car_config import gpio_dict, car_property
    from user_button import UserButton
    from motor import Motor
    from encoder import Encoder
    # from pid_motor import MotorSpeedControl
    # 设定紧急意外缓冲区的大小为100
    micropython.alloc_emergency_exception_buf(100)
    # 左侧电机
    left_motor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B'], 
            motor_install_dir=car_property['LEFT_MOTOR_INSTALL_DIR'])
    left_motor.stop()

    # 右侧电机
    right_motor = Motor(
        gpio_dict['RIGHT_MOTOR_A'], 
        gpio_dict['RIGHT_MOTOR_B'], 
        motor_install_dir=car_property['RIGHT_MOTOR_INSTALL_DIR'])
    right_motor.stop()

    # 左侧编码器
    left_pin_a = Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN)
    left_pin_b = Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN)
    left_encoder = Encoder(left_pin_a, left_pin_b,
        reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
        scale=car_property['LEFT_ENCODER_ANGLE_SCALE'])

    
    # 左侧电机速度控制PID

    # kp = car_property['LEFT_MOTOR_SPEED_CTL_KP']

    # ki = car_property['LEFT_MOTOR_SPEED_CTL_KI']

    # kd = car_property['LEFT_MOTOR_SPEED_CTL_KD']



    kp = car_property['LEFT_MOTOR_SPEED_CTL_KP']

    ki = car_property['LEFT_MOTOR_SPEED_CTL_KI']

    kd = car_property['LEFT_MOTOR_SPEED_CTL_KD']



    left_msc = MotorSpeedControl(left_motor, left_encoder, 

            kp = kp, ki = ki, kd = kd,is_debug=False)



    def btn_callback(pin):

        '''

        回调函数

        改变小车的标志位

        '''

        global left_msc

        print('User Button Pressed')

        utime.sleep_ms(500)

        left_msc.is_debug = not left_msc.is_debug



    # 用户按键引脚编号

    USER_BUTTON = gpio_dict['USER_BUTTON']

    # 创建UserButton对象

    btn = UserButton(USER_BUTTON, btn_callback)





    def callback(timer):

        # 速度控制回调函数

        left_msc.callback(timer)

        

    # 创建定时器 这里用的是定时器4

    timer = Timer(4)

    # 设置定时器回调 100ms执行一次

    period = int(car_property['PID_CTL_PERIOD']*1000)



    timer.init(period=period, mode=Timer.PERIODIC, callback=callback)

    

    # 设置左侧电机转速

    left_msc.speed(0)



    # 按下用户按键，可以查看PID控制的日志



    # try:

    #     while True:

    #         pass

    # except:

    #     timer.deinit()

    #     left_msc.deinit()




