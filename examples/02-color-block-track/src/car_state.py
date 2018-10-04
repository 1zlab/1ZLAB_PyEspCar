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

# class CarOff(CarState):
#     '''小车关闭'''
#     name = 'CAR_OFF'
#     allowed = ['CAR_STOP']

class CarStop(CarState):
    '''小车停止'''
    name = 'CAR_STOP'
    allowed = ['CAR_SERVO_TRACK', 'CAR_SEARCH_AROUND']

class CarServoTrack(CarState):
    '''舵机云台追踪'''
    name = 'CAR_SERVO_TRACK'
    allowed = ['CAR_POINT_TURN', 'CAR_GO_STRAIGHT', 'CAR_SEARCH_AROUND']

class CarPointTurn(CarState):
    '''小车原地旋转'''
    name = 'CAR_POINT_TURN'
    allowed = ['CAR_POINT_TURN_LEFT', 'CAR_POINT_TURN_RIGHT', 'CAR_SEARCH_AROUND']

class CarPointTurnLeft(CarState):
    '''小车原地向左旋转'''
    name = 'CAR_POINT_TURN_LEFT'
    allowed = ['CAR_GO_STRAIGHT', 'CAR_SEARCH_AROUND']

class CarPointTurnRight(CarState):
    '''小车原地向右旋转'''
    name = 'CAR_POINT_TURN_RIGHT'
    allowed = ['CAR_GO_STRAIGHT', 'CAR_SEARCH_AROUND']

class CarGoStraight(CarState):
    '''小车走直线'''
    name = 'CAR_GO_STRAIGHT'
    allowed = ['CAR_SERVO_TRACK', 'CAR_STOP', 'CAR_GO_FORWARD', 'CAR_GO_BACKWARD', 'CAR_SEARCH_AROUND']

class CarGoForward(CarState):
    '''小车前进'''
    name = 'CAR_GO_FORWARD'
    allowed = ['CAR_GO_STRAIGHT', 'CAR_SEARCH_AROUND']

class CarGoBackward(CarState):
    '''小车后退'''
    name = 'CAR_GO_BACKWARD'
    allowed = ['CAR_GO_STRAIGHT', 'CAR_SEARCH_AROUND']

class CarSearchAround(CarState):
    '''小车搜寻模式'''
    name = 'CAR_SEARCH_AROUND'
    allowed = ['CAR_STOP']
