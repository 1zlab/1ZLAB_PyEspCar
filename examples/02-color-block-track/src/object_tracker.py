'''
色块追踪
'''
from pyespcar_sdk import PyCarSDK
from car_state import *
from pid import IncrementalPID
import time

class ObjectTracker:
    '''物体追踪小车'''
    OBJECT_CENTER_OFFSET_THRESHOLD = 0.1
    OBJECT_AREA_THRESHOLD = 0.1
    POINT_TURN_SPEED_PERCENT = 100
    GO_STRAIGHT_SPEED_PERCENT = 50
    def __init__(self, sdk):
        # PyESPCar的SDK
        self.sdk = sdk
        # 上一次的状态
        self.last_state = CarStop()
        # 当前的状态
        self.state = CarStop()
        # 物体在X轴方向上的偏移量
        self.x_offset = 0
        # 物体在Y轴方向上的偏移量
        self.y_offset = 0
        # 物块目标面积的偏移量
        self.area_offset = 0
        # 物体是否在视野里面
        self.is_object_in_view = False
        # 底部舵机的PID
        self.bottom_servo_pid = IncrementalPID(kp=-1, ki=-3, max_result=1, min_result=-1)
        # 顶部舵机的PID
        self.top_servo_pid = IncrementalPID(kp=-1, ki=-3, max_result=1, min_result=-1)

        # 状态与函数之间的映射
        self.on_state_func_dict = {
            # CarOff: self.on_car_off,
            CarStop: self.on_car_stop,
            CarSearchAround: self.on_search_around,
            CarServoTrack: self.on_servo_track,
            CarPointTurn: self.on_point_turn,
            CarPointTurnLeft: self.on_point_turn_left,
            CarPointTurnRight: self.on_point_turn_right,
            CarGoStraight: self.on_go_straight,
            CarGoBackward: self.on_go_backward,
            CarGoForward: self.on_go_forward,
        }
    

    @property
    def angle_offset(self):
        '''获取偏航角'''
        return self.sdk.bottom_servo_angle - self.sdk.BOTTOM_SERVO_DEFAULT_ANGLE


    def update(self, is_object_in_view, x_offset, y_offset, area_offset):
        print('[INFO] update data')
        print('{},{},{},{}'.format(is_object_in_view, x_offset, y_offset, area_offset))
        
        self.is_object_in_view = is_object_in_view
        self.x_offset = self.x_offset * 0.2  + x_offset * 0.8
        self.y_offset = self.y_offset * 0.2 + y_offset * 0.8
        self.area_offset = area_offset

        if abs(self.x_offset) < self.OBJECT_CENTER_OFFSET_THRESHOLD:
                self.x_offset = 0
        if abs(self.y_offset) < self.OBJECT_CENTER_OFFSET_THRESHOLD:
            self.y_offset = 0
        if abs(self.area_offset) < self.OBJECT_AREA_THRESHOLD:
            self.area_offset = 0

        if not self.is_object_in_view:
            print('[INFO] color block not in view')
            # 目标跟丢，进入搜寻模式
            if type(self.state) != CarSearchAround:
                self.switch_state(CarSearchAround)
            
        else:
            print('[INFO] color block in view')
            print('[INFO] cur state: {}'.format(self.state))
            # 执行当前状态的回调函数
            self.on_state_func_dict[self.state.__class__]()
    
    # def on_car_off(self):
    #     '''响应关闭小车'''
    #     self.sdk.stop()
    #     self.sdk.cp_reset()

    def on_car_stop(self):
        '''响应小车停止'''
        print('[INFO] on car stop')
        
        # BUG 下面的执行不到 on_message 中断了？
        print('{}'.format(self.is_object_in_middle()))
        if type(self.last_state) != CarStop:
            # 小车停车
            self.sdk.stop()
        if not self.is_object_in_middle():
            self.switch_state(CarServoTrack)
            

    def is_object_in_middle(self):
        '''判断物体是否在画面中心'''
        
        is_cx = abs(self.x_offset) < self.OBJECT_CENTER_OFFSET_THRESHOLD
        is_cy = abs(self.y_offset) < self.OBJECT_CENTER_OFFSET_THRESHOLD
        
        return is_cx and is_cy

    def on_servo_track(self):
        '''相应舵机追踪'''
        print('[INFO] on servo track')
        
        # 舵机云台物体追踪是否完成
        is_in_middle = self.is_object_in_middle()
        
        if is_in_middle:
            # 舵机云台已经使物体处在画面中心
            if abs(self.angle_offset) > 30:
                # 偏移角度比较大，需要旋转身体
                self.switch_state(CarPointTurn)
            else:
                self.switch_state(CarGoStraight)
        else:
            
            # 下臂舵机PID控制
            # self.bottom_servo_pid.result = self.sdk.bottom_servo_angle
            delta_angle = self.bottom_servo_pid.update(self.x_offset)
            self.sdk.set_bottom_servo_angle(self.sdk.bottom_servo_angle + delta_angle)

            # 上臂舵机PID控制
            # self.top_servo_pid.result = self.sdk.top_servo_angle
            delta_angle = self.top_servo_pid.update(self.y_offset)
            self.sdk.set_top_servo_angle(self.sdk.top_servo_angle + delta_angle)
    
    def get_point_turn_delay_ms(self):
        '''获取小车原地旋转的延时'''
        kp = 2
        return abs(self.angle_offset) * kp

    def on_point_turn(self):
        '''原地旋转'''
        print('[INFO] on point turn')
        if self.angle_offset > 0:
            self.switch_state(CarPointTurnLeft)
        else:
            self.switch_state(CarPointTurnRight)

    def on_point_turn_left(self):
        '''向左原地旋转'''
        print('[INFO] on point turn left')

        delay_ms = self.get_point_turn_delay_ms()
        # 底部舵机复位
        self.sdk.set_bottom_servo_angle(self.sdk.BOTTOM_SERVO_DEFAULT_ANGLE)
        time.sleep(100/1000)

        speed_percent = self.POINT_TURN_SPEED_PERCENT
        self.sdk.turn_left(speed_percent=speed_percent, delay_ms=delay_ms)
        time.sleep(delay_ms/1000)
        
        self.switch_state(CarGoStraight)

    def on_point_turn_right(self):
        '''向右原地旋转'''
        print('[INFO] on point turn right')
        delay_ms = self.get_point_turn_delay_ms()
        # 底部舵机复位
        self.sdk.set_bottom_servo_angle(self.sdk.BOTTOM_SERVO_DEFAULT_ANGLE)
        time.sleep(100/1000)
        
        speed_percent = self.POINT_TURN_SPEED_PERCENT
        self.sdk.turn_right(speed_percent=speed_percent, delay_ms=delay_ms)
        time.sleep(delay_ms/1000)
        
        self.switch_state(CarGoStraight)

    def on_go_straight(self):
        '''小车走直线'''
        print('[INFO] on go straight')
        is_x_offset = abs(self.x_offset) > 2 * self.OBJECT_CENTER_OFFSET_THRESHOLD
        is_y_offset = abs(self.y_offset) > 2 * self.OBJECT_CENTER_OFFSET_THRESHOLD

        if is_x_offset or is_y_offset:
            self.sdk.stop()
            # 偏移过大，舵机云台校准，避免丢失对象
            self.switch_state(CarServoTrack)

        elif self.area_offset > 0.05:
            # 根据物体面积判断需要前进还是后退
            # 面积太大，小车需要后退
            self.switch_state(CarGoBackward)
        elif self.area_offset < -0.05:
            # 面积太小，小车需要前进
            self.switch_state(CarGoForward)
        else:
            # 小车停止前进
            self.switch_state(CarStop)
        
    def on_go_forward(self):
        '''小车向前走'''
        print('[INFO] on go forward')
        speed_percent = self.GO_STRAIGHT_SPEED_PERCENT
        self.sdk.go_forward(speed_percent=speed_percent)
        self.switch_state(CarGoStraight)

    def on_go_backward(self):
        '''小车向后走'''
        print('[INFO] on go backward')
        speed_percent = self.GO_STRAIGHT_SPEED_PERCENT
        self.sdk.go_backward(speed_percent=speed_percent)
        self.switch_state(CarGoStraight)
    
    def on_search_around(self):
        '''四周找寻'''
        # TODO 添加寻找模式
        print('[INFO] on search around')
        if self.is_object_in_view:
            print('[INFO] change to car stop')
            self.switch_state(CarStop)
        else:
            self.sdk.stop()
            print('[INFO] no object in view!!!!!')

            if type(self.last_state) == CarGoForward:
                self.sdk.cp_down(20)
            elif type(self.last_state) == CarGoBackward:
                self.sdk.cp_up(20)
            elif type(self.last_state) == CarPointTurnLeft:
                self.sdk.cp_right(20)
            elif type(self.last_state) == CarPointTurnRight:
                self.sdk.cp_left(20)
            

    def switch_state(self, state):
        '''切换小车的状态'''
        tmp_state_cls = self.state.__class__
        print('[INFO] change stat')
        self.state.switch(state)
        if type(self.state) == state:
            print('[INFO] Change Status To {}'.format(self.state))
            # 更新上一次的状态
            self.last_state.__class__ = tmp_state_cls
            # 执行当前状态的回调函数
            # self.on_state_func_dict[self.state.__class__]()
        else:
            # 状态切换失败
            print('[ERROR]  Change Status Fail')