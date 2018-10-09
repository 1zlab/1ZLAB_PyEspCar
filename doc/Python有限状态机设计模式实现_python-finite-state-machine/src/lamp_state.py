class LampState:
    name = 'state'
    allowed = []
    
    def switch(self, state):

        if state.name in self.allowed:
            print('[INFO] change state: {} to : {}'.format(self, state.name))
            self.__class__ = state
            return True
        else:
            print('[Error] could not change to state: {}'.format(state.name))
            return False            
    def __str__(self):
        return self.name

class LampOff(LampState):
    name = 'LampOff'
    allowed = ['LampLightMiddle']

class LampLightMiddle(LampState):
    name = 'LampLightMiddle'
    allowed = ['LampLightBright']

class LampLightBright(LampState):
    name = 'LampLightBright'
    allowed = ['LampOff']