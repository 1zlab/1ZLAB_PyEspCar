from servo import Servo
import utime

class CloudPlatform:
    DAFAULT_DELTA_ANGLE = 10 # 舵机每次的运动幅度
    
    DIRECTION = {
        'UP': 1,
        'DOWN': -1,
        'LEFT': 1,
        'RIGHT': -1
    }

    def __init__(self, is_debug=False):
        self.bottom_servo = Servo(0, is_debug=is_debug)
        self.top_servo = Servo(1, is_debug=is_debug)
        self.is_debug = is_debug

    def down(self, delta_angle=None):
        '''
        云台上臂向下
        '''
        if delta_angle is None:
            delta_angle = CloudPlatform.DAFAULT_DELTA_ANGLE
        target = CloudPlatform.DIRECTION['DOWN'] * delta_angle + self.top_servo.angle
        if self.is_debug:
            print('[INFO] Turn Down, Target Angle = {}'.format(target))
        
        self.top_servo.angle = target
    
    def up(self, delta_angle=None):
        '''
        云台上臂向上
        '''
        if delta_angle is None:
            delta_angle = CloudPlatform.DAFAULT_DELTA_ANGLE
        target = CloudPlatform.DIRECTION['UP'] * delta_angle + self.top_servo.angle
        if self.is_debug:
            print('[INFO] Turn UP, Target Angle = {}'.format(target))
        
        self.top_servo.angle = target
    
    def left(self, delta_angle=None):
        '''
        云台下臂向左
        '''
        if delta_angle is None:
            delta_angle = CloudPlatform.DAFAULT_DELTA_ANGLE
        target = CloudPlatform.DIRECTION['LEFT']*delta_angle + self.bottom_servo.angle
        
        if self.is_debug:
            print('[INFO] Turn Left, Target Angle = {}'.format(target))
        
        self.bottom_servo.angle = target 
            
    def right(self, delta_angle=None):
        '''
        云台下臂向右
        '''
        if delta_angle is None:
            delta_angle = CloudPlatform.DAFAULT_DELTA_ANGLE
        target =  CloudPlatform.DIRECTION['RIGHT']*delta_angle + self.bottom_servo.angle
        if self.is_debug:
            print('[INFO] Turn Right, Target Angle = {}'.format(target))
        self.bottom_servo.angle = target

    def reset(self):
        self.top_servo.reset()
        utime.sleep_ms(200) # 延时防止卡在死区
        self.bottom_servo.reset()
    
    def deinit(self):
        self.top_servo.deinit()
        self.bottom_servo.deinit()
        