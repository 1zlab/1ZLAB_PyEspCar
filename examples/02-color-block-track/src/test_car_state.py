from car_state import *

class Car:

    def __init__(self):
        self.state = CarStop()
    
    def switch_state(self, state):
        '''切换小车的状态'''

        self.state.switch(state)
        if type(self.state) == state:
            print('[INFO] Change Status To {}'.format(self.state))
        else:
            print(self.state)
            print(self.state.allowed)
            # 状态切换失败
            print('[ERROR]  Change Status Fail')

if __name__ == "__main__":
    car = Car()
    car.switch_state(CarServoTrack)
    