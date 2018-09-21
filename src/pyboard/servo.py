from machine import Pin
from pyb import Timer
from config import config

class Servo:
    timer = None
    SERVO_PWM_FREQUENCY = config['SERVO_PWM_FREQUENCY']
    SERVO_PWM_PERIOD = config['SERVO_PWM_PERIOD']
    SERVO_TIMER_ID = config['SERVO_TIMER_ID']

    SERVO_LIST = [
        (
            config['SERVO_BOTTOM_GPIO'],
            config['SERVO_BOTTOM_CHANNEL_ID'],
            config['SERVO_BOTTOM_PWM_DUTY_PERCENT_MIN'],
            config['SERVO_BOTTOM_PWM_DUTY_PERCENT_MAX'],
            config['SERVO_BOTTOM_ANGLE_RANGE'],
            config['SERVO_BOTTOM_DEFAULT_ANGLE']
        ),
        (
            config['SERVO_TOP_GPIO'],
            config['SERVO_TOP_CHANNEL_ID'],
            config['SERVO_TOP_PWM_DUTY_PERCENT_MIN'],
            config['SERVO_TOP_PWM_DUTY_PERCENT_MAX'],
            config['SERVO_TOP_ANGLE_RANGE'],
            config['SERVO_TOP_DEFAULT_ANGLE']
        )
    ]

    def __init__(self, idx, is_debug=False):
        self.is_debug = is_debug
        
        gpio, ch, min_duty, max_duty, angle_range, default = Servo.SERVO_LIST[idx]

        if Servo.timer is None:
            Servo.timer = Timer(Servo.SERVO_TIMER_ID, freq=Servo.SERVO_PWM_FREQUENCY)
        
        self.pin = Pin(gpio,Pin.OUT)
        self.pwm = Servo.timer.channel(ch, Timer.PWM, pin=self.pin, pulse_width=0)
        self.angle_range = angle_range
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.default = default
        self._angle = default
        self.angle = default
       

    def reset(self):
        self.angle = self.default
        
        if self.is_debug:
            print('[INFO] Servo Reset')
            print(self)

    def angle2duty(self, value):
        return self.min_duty + (self.max_duty - self.min_duty) * ( value / self.angle_range) 

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value):
        value = 0 if value < 0 else value
        value = self.angle_range if value > self.angle_range else value
        self._angle = value

        duty = self.angle2duty(value)
        self.pwm.pulse_width_percent(duty)

        if self.is_debug:
            print(self)
    
    def deinit(self):
        if Servo.timer is not None:
            Servo.timer.deinit() # 释放Timer资源
            Servo.timer = None
        del(self)
    
    def __str__(self):
        print('[INFO] servo angle: {}'.format(self.angle))
        print('[INFO] servo pwm duty percent: {}'.format(self.pwm.pulse_width_percent()))
        print('[INFO] servo pwm duty: {}'.format(self.pwm.pulse_width()))