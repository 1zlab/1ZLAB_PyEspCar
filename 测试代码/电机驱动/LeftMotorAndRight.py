'''
左电机跟右电机

AIN1 UNO D3 -> GPIO 25
AIN2 UNO D6 -> GPIO 27
BIN1 UNO D11 -> GPIO 23
BIN2 UNO D5 -> GPIO 16


使能端口不好用
初步判定 IO无效。
'''
from machine import Pin,PWM

# 控制右侧电机(正向)
A4950T_AIN1 = 25 # 对应UNO底板 D3
A4950T_AIN2 = 27 # 对应UNO底板 D6

# A4950T 电机驱动引脚 GPIO编号
# 控制左侧电机(反向)
A4950T_BIN1 = 23 # 对应UNO底板 D11
A4950T_BIN2 = 15 # 对应UNO底板 D5

# PS之前的Arduino代码，管脚映射写错了
# A4950T_AIN1  = 23 # uno 11
# A4950T_AIN2  = 16 # uno 5
# A4950T_BIN1  = 27 # uno 6
# A4950T_BIN2  = 25 # uno 3

lm_pin_1 = Pin(A4950T_BIN1,Pin.OUT)
lm_pin_2 = Pin(A4950T_BIN2,Pin.OUT)
lm_pwm_1 = PWM(lm_pin_1)
lm_pwm_2 = PWM(lm_pin_2)

rm_pin_1 = Pin(A4950T_AIN2, Pin.OUT)
rm_pin_2 = Pin(A4950T_AIN1, Pin.OUT)
rm_pwm = PWM(rm_pin_1)

def set_lm_pwm(speed):
    '''
    设置左侧电机的PWM
    '''
    global lm_pin_1
    global lm_pin_2
    global lm_pwm

    if speed >= 0:
        lm_pin_1.value(0)
        lm_pwm.duty(speed)
    else:
        lm_pin_1.value(1)
        lm_pwm.duty(1023+speed)


def set_rm_pwm(speed):
    '''
    设置右侧电机的PWM
    '''
    global rm_pin_1
    global rm_pin_2
    global rm_pwm

    if speed >= 0:
        rm_pin_1.value(0)
        rm_pwm.duty(speed)
    else:
        rm_pin_1.value(1)
        rm_pwm.duty(1023+speed)
