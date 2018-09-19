'''
驱动电机
------------------------------
备注2：pwm的范围是-1023 至 1023
备注2：电机死区 ：-250 - 250， pwm信号在这个范围是不转的
'''
from machine import Pin,PWM
from car_config import car_property

class Motor:
    def __init__(self, gpio_a, gpio_b, motor_install_dir=True, motor_dead_block=250, pwm=0):
        
        # A相PWM
        self.pwm_a = PWM(
            Pin(gpio_a, Pin.OUT),
            freq = car_property['PWM_FREQUENCY'],
            duty = 0)
        # B相PWM
        self.pwm_b = PWM(
            Pin(gpio_b, Pin.OUT),
            freq = car_property['PWM_FREQUENCY'],
            duty = 0)
        # 电机安装方向
        if not motor_install_dir:
            self.pwm_a, self.pwm_b = self.pwm_b, self.pwm_a
        # 电机速度信号 取值范围: -1023 - 1023 
        self._pwm = pwm
        # 设置电机的PWM
        self.pwm(self._pwm)
    
    def stop(self, is_lock=True):
        '''
        电机停止转动
        '''
        if is_lock:
            # 电机是否自锁
            self.pwm_a.duty(1023)
            self.pwm_b.duty(1023)
        else:
            self.pwm(0)
        
    def pwm(self, value=None, dead_block=100):
        '''
        获取设置小车的速度
        pwm的范围在 -1023到1023之间 自动放缩
        '''
        if value is None:
            return self._pwm
        
        value = int(value)

        # 添加电机死区保护
        if abs(value) < dead_block:
            value = 0
        
        if abs(value) > 1023:
            # 判断pwm的绝对值是否越界
            value = 1023 if value > 0 else -1023
        # 设置当前的PWM信号
        self._pwm = value
        # 电机正向安装  
        # pwm的取值范围 -1023 - 1023
        if self._pwm >= 0:
            self.pwm_a.duty(0)
            self.pwm_b.duty(abs(self._pwm))
        else:
            self.pwm_a.duty(abs(self._pwm))
            self.pwm_b.duty(0)

    def deinit(self):
        '''
        资源释放
        '''
        # pwm资源释放
        self.pwm_a.deinit()
        self.pwm_b.deinit()


if __name__ == '__main__':
    from car_config import gpio_dict, car_property
    # from motor import Motor
    import time

    # 左侧电机
    lmotor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B'], 
            motor_install_dir=car_property['LEFT_MOTOR_INSTALL_DIR'])
    lmotor.pwm(300)

    # 右侧电机
    rmotor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'], 
            motor_install_dir=car_property['RIGHT_MOTOR_INSTALL_DIR'])
    rmotor.pwm(300)

    try:
        while True:
            pass
    except:
        lmotor.deinit()
        rmotor.deinit()
