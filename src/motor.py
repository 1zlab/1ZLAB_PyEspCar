'''
电机控制类
'''
from machine import Pin,PWM
from car_config import car_property,gpio_dict

class Motor:
    # MOTOR列表
    MOTOR_LIST = [
        (
            gpio_dict['LEFT_MOTOR_A'],
            gpio_dict['LEFT_MOTOR_B'],
            car_property['LEFT_MOTOR_INSTALL_DIR']
        ),
        (
            gpio_dict['RIGHT_MOTOR_A'],
            gpio_dict['RIGHT_MOTOR_B'],
            car_property['RIGHT_MOTOR_INSTALL_DIR']
        )
    ]

    # 电机的PWM频率还有PWM取值范围
    MOTOR_MAX_PWM = car_property['MOTOR_MAX_PWM']
    MOTOR_PWM_FREQUENCY = car_property['MOTOR_PWM_FREQUENCY']

    def __init__(self, idx, is_debug=False):
        
        gpio_a, gpio_b, self.motor_install_dir = Motor.MOTOR_LIST[idx]
        # A相PWM
        self.pwm_a = PWM(
            Pin(gpio_a, Pin.OUT),
            freq = Motor.MOTOR_PWM_FREQUENCY,
            duty = 0)
        
        # B相PWM
        self.pwm_b = PWM(
            Pin(gpio_b, Pin.OUT),
            freq = Motor.MOTOR_PWM_FREQUENCY,
            duty = 0)
        
        # 电机安装方向
        if not self.motor_install_dir:
            self.pwm_a, self.pwm_b = self.pwm_b, self.pwm_a
        
        # 电机速度信号 取值范围: -1023 - 1023 
        self._pwm = 0
        # 设置电机的PWM
        # self.pwm(self._pwm)
    
    def stop(self):
        '''
        电机停止转动
        '''
        self.speed = 0
    
    @property
    def speed(self):
        return self._pwm

    @speed.setter
    def speed(self, value):
        value = int(value)
        if abs(value) > Motor.MOTOR_MAX_PWM:
            # 判断pwm的绝对值是否越界
            value = Motor.MOTOR_MAX_PWM if value > 0 else -1*Motor.MOTOR_MAX_PWM
        
        # 设置当前的PWM信号
        self._pwm = value
        # 驱动电机驱动
        if self._pwm >= 0:
            self.pwm_a.duty(0)
            self.pwm_b.duty(abs(self._pwm))
        else:
            self.pwm_a.duty(abs(self._pwm))
            self.pwm_b.duty(0)

    @property
    def speed_percent(self):
        '''获得百分比标识的小车'''
        return (self.speed / 1023) * 100

    @speed_percent.setter
    def speed_percent(self, value):
        speed = int(value / 100 * 1023)
        self.speed = speed
        
    def deinit(self):
        '''
        资源释放
        '''
        # pwm资源释放
        self.pwm_a.deinit()
        self.pwm_b.deinit()
    


