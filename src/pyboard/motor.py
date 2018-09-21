'''
电机控制类
'''
from machine import Pin
from pyb import Timer
from config import config
class Motor:

    MOTOR_PWM_FREQUENCY = config['MOTOR_PWM_FREQUENCY']
    MOTOR_PWM_MAX_DUTY = config['MOTOR_PWM_MAX_DUTY']
    MOTOR_PWM_MAX_DUTY_PERCENT = config['MOTOR_PWM_MAX_DUTY_PERCENT']

    # MOTOR资源列表
    MOTOR_LIST = [
        (
            config['LEFT_MOTOR_A_GPIO'],
            config['LEFT_MOTOR_B_GPIO'],
            config['LEFT_MOTOR_IS_REVERSE'],
            config['LEFT_MOTOR_TIMER_ID'],
            config['LEFT_MOTOR_A_CHANNEL'],
            config['LEFT_MOTOR_B_CHANNEL'],
        ),
        (
            config['RIGHT_MOTOR_A_GPIO'],
            config['RIGHT_MOTOR_B_GPIO'],
            config['RIGHT_MOTOR_IS_REVERSE'],
            config['RIGHT_MOTOR_TIMER_ID'],
            config['RIGHT_MOTOR_A_CHANNEL'],
            config['RIGHT_MOTOR_B_CHANNEL'],
        )
    ]

   

    def __init__(self, idx, is_debug=False):
        
        gpio_a, gpio_b, reverse, timer_id, ch_a, ch_b = Motor.MOTOR_LIST[idx]

        # 电机是否反方向安装
        self.reverse = reverse
        
        # PWM定时器
        self.timer = Timer(timer_id, freq=Motor.MOTOR_PWM_FREQUENCY)

        # 电机A相PWM
        self.pin_a = Pin(gpio_a, Pin.OUT)
        self.pwm_a = self.timer.channel(ch_a, Timer.PWM, pin=self.pin_a, pulse_width=0)
        
        # 电机B相PWM
        self.pin_b = Pin(gpio_b, Pin.OUT)
        self.pwm_b = self.timer.channel(ch_b, Timer.PWM, pin=self.pin_b, pulse_width=0)
        
        # 电机速度信号 取值范围: -100 - 100 
        self._speed = 0

        self.is_debug = is_debug
        # 设置电机的PWM
        # self.pwm(self._pwm)

    def stop(self):
        '''
        电机停止转动
        '''
        self.speed = 0

        if self.is_debug:
            print('[INFO] motor stop')

    @property
    def speed(self):
        if self.reverse:
            return self._speed * -1
        else:
            return self._speed

    @speed.setter
    def speed(self, value):
        value = float(value)
        if self.reverse:
            value *= -1

        # 边界判断
        if abs(value) > Motor.MOTOR_PWM_MAX_DUTY_PERCENT:
            if value > 0:
                value = Motor.MOTOR_PWM_MAX_DUTY_PERCENT
            else:
                value = -Motor.MOTOR_PWM_MAX_DUTY_PERCENT

        self._speed = value

        if value >= 0:
            self.pwm_a.pulse_width_percent(0)
            self.pwm_b.pulse_width_percent(abs(value))
        else:
            self.pwm_a.pulse_width_percent(abs(value))
            self.pwm_b.pulse_width_percent(0)

        if self.is_debug:
            print('[INFO] pina duty: {} pinb duty: {}'.format(self.pwm_a.pulse_width(), self.pwm_b.pulse_width()))
            print('[INFO] pina duty percent: {} , pinb duty percent: {}'.format(
                self.pwm_a.pulse_width_percent(),
                self.pwm_b.pulse_width()))
        
    def deinit(self):

        self.timer.deinit()
        if self.is_debug:
            print('[INFO] deinit motor')
        del(self)


