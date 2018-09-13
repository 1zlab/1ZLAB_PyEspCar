'''
小车的GUI界面
'''
from uart_screen import UartScreen
import network

class CarGUI:

    def __init__(self):
        self.uscreen = UartScreen()
        self.wifi = network.WLAN(network.STA_IF)

        with open('wifi_config.json','r') as f:
            config = json.loads(f.read())
            self.essid = config['essid']

    def ip(self):
        
        if self.wifi.isconnected():
            # WIFI热点 (中文)
            self.uscreen.text(0, 0, b'WIFI\xc8\xc8\xb5\xe3', size='SMALL')
            self.uscreen.text(80, 0, self.essid, size='SMALL')
            # 显示IP还有端口号
            self.uscreen.text(0, 24, 'IP: {} , Port: {}'.format(self.wifi.ifconfig()[0], 8266),size='SMALL')
        else:
            self.uscreen.text(0, 0, 'WIFI NOT Connected...')
    
    
    def show(self, car):
        '''
        在串口液晶屏幕上打印相关的信息
        '''

        pass

    


from uart_screen import UartScreen

uscreen = UartScreen()

uscreen.clear('WHITE')

# 打印WIFI 热点信息
uscreen.text(0, 0, b'WIFI\xc8\xc8\xb5\xe3', size='SMALL', color='BLACK')
uscreen.text(80, 0, 'ChinaNet-Q5uk', size='SMALL', color='BLACK')
# 打印IP端口号
uscreen.text(0, 24, 'IP: {} Port: {}'.format('192.168.2.220', 8266),size='SMALL', color='BLACK')

# 显示小车的位姿
uscreen.text(0, 48, 'CAR: RUN', size='MIDDLE', color='GREEN')