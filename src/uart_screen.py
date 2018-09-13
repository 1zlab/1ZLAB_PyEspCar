'''
串口液晶屏

分辨率 240 * 360

WARNING 串口液晶屏 存在反常设计 RX为TX TX为RX
'''

from machine import UART
from car_config import gpio_dict

class UartScreen:
    '''
    串口液晶屏
    '''
    def __init__(self, uart=None):
        
        if uart is None:
            self.uart = UART(
                1, # UART
                baudrate=115200,
                rx=gpio_dict['UART_LCD_RX'],
                tx=gpio_dict['UART_LCD_TX'],
                timeout=10)
        else:
            self.uart = uart
        
        # 清屏
        self.clear()
        # 颜色字典W
        self.color = {
            'BLACK' : 0,
            'WHITE' : 15,
            'RED' : 1,
            'GREEN' : 2,
            'BLUE' : 3,
            'YELLOW' : 4,
            'PURPLE' : 6,
            'GRAY': 8,
            'LIGHT_RED' : 9,
            'LIGHT_GREEN' : 10,
            'LIGHT_BULE' : 11,
            'LIGHT_YELLOW' : 12,
            'LIGHT_PURPLE' : 14,
            'LIGHT_GREY' : 7
        }

        # 字体大小
        self.font_size = {
            'LARGE': 48,
            'BIG': 32,
            'MIDDLE': 24,
            'SMALL': 16
        }

        # 亮度等级
        self.brightness = {
            'HIGH': 0,
            'NORMAL': 64,
            'MIDDLE': 128,
            'DARK': 192,
            'ZERO': 255
        }

        # 显示方向
        self.direction = {
            'HORIZONTAL': 1,
            'VERTITAL': 0
        }
    
    def version(self):
        '''
        显示当前的版本号
        '''
        self.uart.write('VER;\r\n')

    def clear(self, color='BLACK'):
        '''
        清屏
        '''
        color = self.color[color] 
        self.uart.write('CLR(%s);\r\n' % color)

    def show(self):
        '''
        显示画面
        '''
        # self.uart.write(self.frame)
        pass
        
    def brightness(self, level='NORMAL'):
        '''
        调整画面亮度
        '''
        level = self.brightness[level]
        
        self.uart.write('BL(%s);\r\n' % level)

    def direction(self, direction='HORIZONTAL'):
        '''
        设置显示方向
        '''
        direction = self.direction[direction]
        self.uart.write('dir(%s);\r\n' % direction)

    def point(self, x, y, color='WHITE'):
        '''
        绘制一个点
        '''
        color = self.color[color]
        
        self.uart.write('PS({0},{1},{2});\r\n'.format(x, y, color))

    def circle(self, x, y, r, color='WHITE', is_fill=False):
        '''
        绘制圆
        '''
        color = self.color[color]
        if is_fill:
            # 绘制填充圆
            self.uart.write('CIRF({0},{1},{2},{3});\r\n'.format(
                x, y, r, color))
        else:
            # 绘制空心圆
            self.uart.write('CIR({0},{1},{2},{3});\r\n'.format(
                x, y, r, color))
        
    def line(self, x1, y1, x2, y2, color='WHITE'):
        '''
        绘制直线
        '''
        color = self.color[color]

        self.uart.write('PL({0},{1},{2},{3},{4});\r\n'.format(
            x1, y1, x2, y2, color))
    

    def rect(self, x, y, w, h, color='WHITE', is_fill=False):
        '''
        绘制矩形
        '''
        color = self.color[color]

        if is_fill:
            self.uart.write('BOXF({0},{1},{2},{3},{4})'.format(
                x, y, x + w, y + h, color))
        else:
            self.uart.write('BOX({0},{1},{2},{3},{4})'.format(
                x, y, x + w, y + h, color))
        
    def text(self, x, y, text, size='MIDDLE', color='WHITE'):
        '''
        绘制文本
        '''

        size = self.font_size[size] 
        color = self.color[color]

        if type(text) == bytes:
            # 发送中文 比特 GB2312编码
            cmd = "DC{0}({1},{2},".format(size, x, y).encode()
            cmd += text
            cmd += ",{0});\r\n".format(color).encode()
            self.uart.write(cmd)
        else:
            self.uart.write("DC{4}({0},{1},{2},{3});\r\n".format(x,y,text,color, size))

if __name__ == '__main__':
    uscreen = UartScreen()
    # 显示中文1Z实验室
    # 注: 中文编码为GB2312
    uscreen.text(0, 0,  b'1Z\xca\xb5\xd1\xe9\xca\xd2', size='LARGE')
    # 显示PyESPCar
    uscreen.text(0, 200,  'PyESPCar', size='LARGE')