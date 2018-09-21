import utime
from pyb import Timer
from config import config
from pid_motor import MotorSpeedControl
from motor import Motor
from encoder import Encoder

left_motor = Motor(0)
left_encoder = Encoder(0)

Kp = config['LEFT_MOTOR_SPEED_CTL_KP']
Ki = config['LEFT_MOTOR_SPEED_CTL_KI']
Kd = config['LEFT_MOTOR_SPEED_CTL_KD']

msc = MotorSpeedControl(left_motor, left_encoder, kp=Kp, ki=Ki, kd=Kd, is_debug=True)



timer = Timer(4, freq=int(1/config['MOTOR_SPEED_PID_CTL_PERIOD']))

update_flag = False
def callback(tim):
    global update_flag
    if not update_flag:
        update_flag = True

timer.callback(callback)

msc.speed = 0.1
while True:
    if update_flag:
        msc.update()
        update_flag = False
    
    utime.sleep_ms(1)
