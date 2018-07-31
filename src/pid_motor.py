from motor import Motor
from encoder import Encoder

class PIDMotor(Motor):
    '''
    PID Motor继承自 Motor类，可以设置转速
    '''
    def __init__(motor, encoder)):
