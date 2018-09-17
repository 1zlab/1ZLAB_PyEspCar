'''
电机的PID控制(角度，速度)
'''
from machine import Timer
from pid import IncrementalPID
from car_config import car_property

# class MotorAngleControl(object):
#     '''
#     电机旋转角度PID控制
#     PID：  P比例 I 积分(惯性力) D微分(阻尼力)
#     使用PID，结合编码器提供的反馈
#     每隔100ms采样一次
#     '''
#     def __init__(self, motor, encoder, kp, ki=0, kd=0, max_bias_sum=None, is_debug=False):
#         # 电机对象
#         self.motor = motor
#         # 编码器
#         self.encoder = encoder
#         self.old_encoder_pos = 0
#         # 初始化编码器的计数
#         self.encoder.position = 0
#         # PID对象
#         self.pid = PID(kp, ki, kd, max_bias_sum=max_bias_sum)
#         # 是否开启调试模式
#         self.is_debug = is_debug
#         self.max_pwm = 1023 # 测试角度控制的时候的最大PWM
#         # if is_debug:
#         # 迭代次数计数
#         self._iteration = 0

#     def init(self):
#         self.encoder.position = 0
#         self.pid.cur_bias = 0
#         self.pid.bias_sum = 0
#         self.pid.set_target_value(0)
#         self.old_encoder_pos = 0

#     def set_angle(self, angle, is_reset=False):
#         '''
#         设置电机的旋转角度
#         @angle:  电机旋转角度
#         @is_continue: 电机是否重新复位
#             * False: 不复位的话，计数器不清，
#                 0度在编码器最初始的位置 
#             * True: 如果连续旋转，旋转到特定角度的话，
#                 编码器计数清零， 目标角度设定为0度,同时is_reset=False
#         '''
#         # 设定目标计数
#         target_count = angle

#         if is_reset:
#             # 电机角度重置，计数器清零
#             self.encoder.position = 0
#             # 目标计数器加上之前编码器的值
#             target_count += self.encoder.position

#         # 设置PID的目标取值
#         self.pid.set_target_value(target_count)

#     def callback(self, timer, min_threshold=3, max_threshold=40):
#         '''回调函数'''
#         # 获取当前编码器的真实取值
#         real_value = self.encoder.position
#         # 对真实值进行修正 (简单滤波)
#         delta_posi =  real_value - self.old_encoder_pos 
#         if abs(delta_posi) > max_threshold:
#             self.encoder.position = self.old_encoder_pos 
#             real_value = self.old_encoder_pos
#         else:
#             self.old_encoder_pos = real_value

#         # 更新PID
#         pwm = self.pid.update(real_value)

#         # pwm的值放缩在 正负1023之间
#         # 为了准确，这里需要限定一下速度
#         # max_pwm = 1023
#         max_pwm = self.max_pwm
#         if abs(pwm) > max_pwm:
#             pwm = max_pwm if pwm > 0 else -1*max_pwm

#         if abs(real_value - self.pid.target_value) < min_threshold:
#             pwm = 0
    
#         self.motor.pwm(int(pwm))

#         if self.is_debug:
#             self._iteration += 1
#             if self._iteration > 10:
#                 # 1s 打印一次
#                 self._iteration = 0
#                 print("Target: {} RealValue: {} PID Result: {}".format(self.pid.target_value, self.encoder.position, pwm))
#                 print('PWM: {}'.format(pwm))

#     def deinit(self):
#         '''销毁资源'''
#         self.encoder.deinit()
#         self.motor.deinit()


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
        if abs(encoder_value) > 50:
            return False
        elif self.motor.pwm() > 0 and encoder_value < 0:
            return False
        elif self.motor.pwm() < 0 and encoder_value > 0:
            return False
        else:
            return True
        
    def callback(self, timer, min_threshold=1):
        '''
        回调函数
        '''
        # 读取一段时间内， 真实的电机旋转角度
        if self.is_legal_speed(self.encoder.position):
            # 从编码器测得速度
            self._speed = self.encoder.position
        
        # 编码器清零
        self.encoder.position = 0
        # 更新PID 获取新的PWM控制信号
        pwm = self.pid.update(self._speed) 
        
        if not self.stop_flag:
            self.motor.pwm(int(pwm))
        else:
            # 电机停止旋转
            self.motor.pwm(0)

        if self.is_debug:
            self._iteration += 1
            if self._iteration > 4:
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

    kp = 0
    ki = -10
    kd = 0

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

    timer.init(period=25, mode=Timer.PERIODIC, callback=callback)

    # 设置左侧电机转速
    left_msc.speed(0.5)

    # 按下用户按键，可以查看PID控制的日志

    # try:
    #     while True:
    #         pass
    # except:
    #     timer.deinit()
    #     left_msc.deinit()
