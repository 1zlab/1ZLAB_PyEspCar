import pygame

class PyCarSDK:
    MQTT_TOPIC_ID = 'PYESPCAR_CTL_MSG'
    DEFAULT_CAR_SPEED = 60 # 默认小车移动速度
    DEFAULT_CP_DELTA_ANGLE = 5 # 舵机云台的单位移动角度
    
    
    def __init__(self, mqtt_client, is_debug=False):
        self.is_debug = is_debug

        self.mqtt_client = mqtt_client
        self.speed = PyCarSDK.DEFAULT_CAR_SPEED
        self.cp_delta_angle = PyCarSDK.DEFAULT_CP_DELTA_ANGLE
        
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
        '''通过MQTT发送指令'''
        
        if self.is_debug:
            print('Topic: {}'.format(PyCarSDK.MQTT_TOPIC_ID))
            print('SEND:  {}'.format(cmd_str))
        
        self.mqtt_client.publish(self.MQTT_TOPIC_ID, cmd_str)

    def stop(self, delta_angle=None):
        self.send_command('STOP')

    def turn_left(self, speed_percent=None, delay_ms=None):
        if speed_percent is None:
            speed_percent = self.speed

        if delay_ms is not None:
            self.send_command('TURN_LEFT,{},{}'.format(speed_percent, delay_ms))
        else:
            self.send_command('TURN_LEFT,{}'.format(speed_percent))
    def turn_right(self, speed_percent=None, delay_ms=None):
        if speed_percent is None:
            speed_percent = self.speed

        if delay_ms is not None:
            self.send_command('TURN_RIGHT,{},{}'.format(speed_percent, delay_ms))
        else:
            self.send_command('TURN_RIGHT,{}'.format(speed_percent))

    def go_forward(self, speed_percent=None, delay_ms=None):
        if speed_percent is None:
            speed_percent = self.speed

        if delay_ms is not None:
            self.send_command('GO_FORWARD,{},{}'.format(speed_percent, delay_ms))
        else:
            self.send_command('GO_FORWARD,{}'.format(speed_percent))

    def go_backward(self, speed_percent=None, delay_ms=None):
        if speed_percent is None:
            speed_percent = self.speed

        if delay_ms is not None:
            self.send_command('GO_BACKWARD,{},{}'.format(speed_percent, delay_ms))
        else:
            self.send_command('GO_BACKWARD,{}'.format(speed_percent))

    def move(self, left_motor_speed, right_motor_speed, delay_ms=None):
        if delay_ms is not None:
            self.send_command('MOVE,{},{},{}'.format(left_motor_speed, right_motor_speed, delay_ms))
        else:
            self.send_command('MOVE,{},{}'.format(left_motor_speed, right_motor_speed))
    
    def cp_up(self, delta_angle=None):
        if delta_angle is None:
            delta_angle = self.cp_delta_angle
        self.send_command('CP_UP,{}'.format(delta_angle))
    
    def cp_down(self, delta_angle=None):
        if delta_angle is None:
            delta_angle = self.cp_delta_angle
        self.send_command('CP_DOWN,{}'.format(delta_angle))

    def cp_left(self, delta_angle=None):
        if delta_angle is None:
            delta_angle = self.cp_delta_angle
        self.send_command('CP_LEFT,{}'.format(delta_angle))

    def cp_right(self, delta_angle=None):
        if delta_angle is None:
            delta_angle = self.cp_delta_angle
        self.send_command('CP_RIGHT,{}'.format(delta_angle))
    
    def cp_reset(self):
        self.send_command('CP_RESET')