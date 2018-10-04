import pygame
from car_config import car_property

'''
NOTE：使用Python实现有限状态机FSM设计模式，用于管理小车的状态
'''
class CarState(object):
    '''小车的状态基类'''
    name = "state"
    allowed = []
    
    def switch(self, state):
        if state.name in self.allowed:
            print('[INFO] change state: {} to : {}'.format(self, state.name))
            self.__class__ = state
        else:
            print('[Error] could not change to state: {}'.format(state.name))
    def __str__(self):
        return self.name

class CarOff(CarState):
    '''小车关闭'''
    name = 'CAR_OFF'
    allowed = ['CAR_STOP']

class CarStop(CarState):
    '''小车停止'''
    name = 'CAR_STOP'
    allowed = ['CAR_SERVO_TRACK', 'CAR_SEARCH_AROUND', 'CAR_GO_FORWARD', 'CAR_GO_BACKWARD', 'CAR_OFF']

class CarServoTrack(CarState):
    '''舵机云台追踪'''
    name = 'CAR_SERVO_TRACK'
    allowed = ['CAR_STOP', 'CAR_POINT_TURN_LEFT', 'CAR_POINT_TURN_RIGHT', 'CAR_OFF']

class CarPointTurn(CarState):
    '''小车原地旋转'''
    name = 'CAR_POINT_TURN'
    allowed = ['CAR_STOP', 'CAR_OFF']

class CarPointTurnLeft(CarPointTurn):
    '''小车原地向左旋转'''
    name = 'CAR_POINT_TURN_LEFT'

class CarPointTurnRight(CarPointTurn):
    '''小车原地向右旋转'''
    name = 'CAR_POINT_TURN_RIGHT'

class CarGoStraight(CarState):
    '''小车走直线'''
    name = 'CAR_GO_STRAIGHT'
    allowed = ['CAR_STOP', 'CAR_OFF']

class CarGoForward(CarGoStraight):
    '''小车前进'''
    name = 'CAR_GO_FORWARD'
    
class CarGoBackward(CarGoStraight):
    '''小车后退'''
    name = 'CAR_GO_BACKWARD'


class CarSearchAround(CarState):
    '''小车搜寻模式'''
    name = 'CAR_SEARCH_AROUND'
    allowed = ['CAR_SERVO_TRACK', 'CAR_OFF']


class PyCarSDK:
    # MQTT小车控制的Topic
    MQTT_TOPIC_ID = 'PYESPCAR_CTL_MSG'
    # 默认小车移动速度
    DEFAULT_CAR_SPEED = 60
    # 舵机云台的单位移动角度
    DEFAULT_CP_DELTA_ANGLE = 5
    
    # 底部舵机角度范围
    BOTTOM_SERVO_ANGLE_RANGE = car_property['BOTTOM_SERVO_ANGLE_RANGE']
    # 底部舵机默认角度
    BOTTOM_SERVO_DEFAULT_ANGLE = car_property['BOTTOM_SERVO_DEFAULT_ANGLE']
    # 顶部舵机角度范围
    TOP_SERVO_ANGLE_RANGE = car_property['TOP_SERVO_ANGLE_RANGE']
    # 顶部舵机默认角度
    TOP_SERVO_DEFAULT_ANGLE = car_property['TOP_SERVO_DEFAULT_ANGLE']
    
    
    def __init__(self, mqtt_client, is_debug=False):
        # 是否开启调试模式
        self.is_debug = is_debug
        # MQTT的客户端
        self.mqtt_client = mqtt_client
        # 设置小车的默认速度
        self.speed = PyCarSDK.DEFAULT_CAR_SPEED
        # 设置默认的舵机云台角度变换值
        self.cp_delta_angle = PyCarSDK.DEFAULT_CP_DELTA_ANGLE
        # 记录当前底部舵机的角度
        self.bottom_servo_angle = PyCarSDK.DEFAULT_BOTTOM_SERVO_ANGLE
        # 记录顶部舵机的角度
        self.top_servo_angle = PyCarSDK.DEFAULT_TOP_SERVO_ANGLE    
        # 键盘事件映射字典
        self.KEY_FUNC_MAP = {
            pygame.K_LEFT: self.turn_left,
            pygame.K_RIGHT: self.turn_right,
            pygame.K_UP: self.go_forward,
            pygame.K_DOWN: self.go_backward,
            pygame.K_a: self.cp_left,
            pygame.K_d: self.cp_right,
            pygame.K_w: self.cp_up,
            pygame.K_s: self.cp_down,
            pygame.K_r: self.cp_reset
        }
        
        # 小车停止
        self.stop()
        # 舵机复位
        self.cp_reset()

    def response_keys_event(self, events):
        '''
        相应键盘事件
        '''
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.KEY_FUNC_MAP:
                    self.KEY_FUNC_MAP[event.key]()
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    self.stop()

    def send_command(self, cmd_str):
        '''
        通过MQTT发送指令
        '''
        if self.is_debug:
            print('Topic: {}'.format(PyCarSDK.MQTT_TOPIC_ID))
            print('SEND:  {}'.format(cmd_str))
        
        self.mqtt_client.publish(self.MQTT_TOPIC_ID, cmd_str)

    def stop(self, delta_angle=None):
        '''
        小车停止
        '''
        self.send_command('STOP')
        if self.is_debug:
            print('[INFO] Car Stop')
        

    def turn_left(self, speed_percent=None, delay_ms=None):
        '''
        小车左转
        '''
        if speed_percent is None:
            speed_percent = self.speed

        if delay_ms is not None:
            self.send_command('TURN_LEFT,{},{}'.format(speed_percent, delay_ms))
        else:
            self.send_command('TURN_LEFT,{}'.format(speed_percent))
        
        if self.is_debug:
            print('[INFO] car turn left, speed: {}, delay_ms: {}'.format(speed_percent, delay_ms))
        
    def turn_right(self, speed_percent=None, delay_ms=None):
        '''
        小车右转
        '''
        if speed_percent is None:
            speed_percent = self.speed

        if delay_ms is not None:
            self.send_command('TURN_RIGHT,{},{}'.format(speed_percent, delay_ms))
        else:
            self.send_command('TURN_RIGHT,{}'.format(speed_percent))

        if self.is_debug:
            print('[INFO] car turn right, speed: {}, delay_ms: {}'.format(speed_percent, delay_ms))

    def go_forward(self, speed_percent=None, delay_ms=None):
        '''
        小车前进
        '''
        if speed_percent is None:
            speed_percent = self.speed

        if delay_ms is not None:
            self.send_command('GO_FORWARD,{},{}'.format(speed_percent, delay_ms))
        else:
            self.send_command('GO_FORWARD,{}'.format(speed_percent))

        if self.is_debug:
            print('[INFO] car go forward, speed: {}, delay_ms: {}'.format(speed_percent, delay_ms))

    def go_backward(self, speed_percent=None, delay_ms=None):
        '''
        小车后退
        '''
        if speed_percent is None:
            speed_percent = self.speed

        if delay_ms is not None:
            self.send_command('GO_BACKWARD,{},{}'.format(speed_percent, delay_ms))
        else:
            self.send_command('GO_BACKWARD,{}'.format(speed_percent))

        if self.is_debug:
            print('[INFO] car go backward, speed: {}, delay_ms: {}'.format(speed_percent, delay_ms))

    def move(self, left_motor_speed, right_motor_speed, delay_ms=None):
        '''
        小车运动 两轮差速前进
        '''
        if delay_ms is not None:
            self.send_command('MOVE,{},{},{}'.format(left_motor_speed, right_motor_speed, delay_ms))
        else:
            self.send_command('MOVE,{},{}'.format(left_motor_speed, right_motor_speed))

        if self.is_debug:
            print('[INFO] car move, left_speed: {}, right_speed: {} delay_ms: {}'.format(\
                left_motor_speed,right_motor_speed, delay_ms))

    def set_bottom_servo_angle(self, angle):
        '''
        设置底部舵机的角度
        '''
        if angle > PyCarSDK.BOTTOM_SERVO_ANGLE_RANGE:
            angle = PyCarSDK.BOTTOM_SERVO_ANGLE_RANGE
        elif angle < 0:
            angle = 0
        
        self.send_command('SET_BOTTOM_SERVO_ANGLE,{}'.format(angle))
        self.bottom_servo_angle = angle
        if self.is_debug:
            print('[INFO] bottom servo angle: {}'.format(self.bottom_servo_angle))
    
    def set_top_servo_angle(self, angle):
        '''
        设置顶部的舵机角度
        '''
        if angle > PyCarSDK.TOP_SERVO_ANGLE_RANGE:
            angle = PyCarSDK.TOP_SERVO_ANGLE_RANGE
        elif angle < 0:
            angle = 0

        self.send_command('SET_TOP_SERVO_ANGLE,{}'.format(angle))
        self.top_servo_angle = angle
        if self.is_debug:
            print('[INFO] top servo angle: {}'.format(self.top_servo_angle))
        
    def cp_up(self, delta_angle=None):
        '''
        舵机云台向上
        '''
        if delta_angle is None:
            delta_angle = self.cp_delta_angle
        angle = self.top_servo_angle + delta_angle
        self.set_top_servo_angle(angle)

    def cp_down(self, delta_angle=None):
        '''
        舵机云台向下
        '''
        if delta_angle is None:
            delta_angle = self.cp_delta_angle
        angle = self.top_servo_angle - delta_angle
        self.set_top_servo_angle(angle)

    def cp_left(self, delta_angle=None):
        '''
        云台向左转
        '''
        if delta_angle is None:
            delta_angle = self.cp_delta_angle
        
        angle = self.bottom_servo_angle + delta_angle
        self.set_bottom_servo_angle(angle)

    def cp_right(self, delta_angle=None):
        '''
        云台向右转
        '''
        if delta_angle is None:
            delta_angle = self.cp_delta_angle
        
        angle = self.bottom_servo_angle - delta_angle
        self.set_bottom_servo_angle(angle)

    def cp_reset(self):
        '''
        舵机复位
        '''
        self.set_bottom_servo_angle(PyCarSDK.BOTTOM_SERVO_DEFAULT_ANGLE)
        self.set_top_servo_angle(PyCarSDK.TOP_SERVO_DEFAULT_ANGLE)

        if self.is_debug:
            print('[INFO] cloud platform reset')