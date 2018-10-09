from lamp_state import LampOff, LampLightMiddle, LampLightBright

class Lamp:
    '''台灯'''
    def __init__(self):
        # 当前的台灯亮度
        self.brightness = 0
        # 创建一个台灯实例
        self.state = LampOff()
        # 状态与台灯相应函数映射
        self.state_map = {
            LampOff: self.on_lamp_off,
            LampLightMiddle: self.on_lamp_light_middle,
            LampLightBright: self.on_lamp_light_bright
        }

    def set_brightness(self, value):
        '''设置台灯亮度'''
        self.brightness = value
        print('[INFO]set brightness to {}'.format(value))

    def on_lamp_off(self):
        '''响应关灯状态'''
        print('[INFO] on lamp off')
        self.set_brightness(0)

    def on_lamp_light_middle(self):
        '''响应台灯护眼模式'''
        print('[INFO] on lamp light middle')
        self.set_brightness(125)
    
    def on_lamp_light_bright(self):
        '''响应台灯明亮模式'''
        print('[INFO] on lamp light bright')
        self.set_brightness(255)
    
    def switch(self, state):
        '''切换状态'''
        result = self.state.switch(state)
        if result:
            # 成功进行状态转换
            # 执行状态转换的函数
            self.state_map[state]()
        else:
            print('[ERROR] Fail to change  state to {}'.format(state))
