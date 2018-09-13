'''
串口液晶屏

分辨率 240 * 360

WARNING 串口液晶屏 存在反常设计 RX为TX TX为RX

WARNING: 因为是使用串口通信 解析字符串, 
所以打印text的时候,不能出现诸如 
TODO text 筛选关键字

TODO 添加局部刷新
'''

from machine import UART
from car_config import gpio_dict

class UartScreen:
    '''
    串口液晶屏
    '''
    def __init__(self, uart=None, width=240, height=360, baundrate=9600):
        
        if uart is None:
            self.uart = UART(
                1, # UART
                baudrate=baundrate,
                rx=gpio_dict['UART_LCD_RX'],
                tx=gpio_dict['UART_LCD_TX'],
                timeout=10)
        else:
            self.uart = uart
        
        # 设置液晶屏的波特率
        self.baundrate(baundrate)
        # 串口液晶屏的宽度
        self.width = width
        # 串口液晶屏的高度
        self.height = height

        
        # 颜色字典W
        self.color_dict = {
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
        self.font_size_dict = {
            'LARGE': 48,
            'BIG': 32,
            'MIDDLE': 24,
            'SMALL': 16
        }

        # 亮度等级
        self.brightness_level_dict = {
            'HIGH': 0,
            'NORMAL': 64,
            'MIDDLE': 128,
            'DARK': 192,
            'ZERO': 255
        }

        # 显示方向
        self.direction_dict = {
            'HORIZONTAL': 1,
            'VERTITAL': 0
        }

        # 设置背光的亮度
        self.brightness(125)
        # 清屏
        self.clear()

    def send_cmd(self, cmd):
        '''
        串口屏发送指令
        '''
        repeat_time = 2

        for i in range(repeat_time):
            self.uart.write(cmd)
    def baundrate(self, boundrate):
        '''
        设置波特率
        '''
        self.send_cmd('BPS({});\r\n'.format(boundrate))


    def version(self):
        '''
        显示当前的版本号,分辨率等信息
        '''
        self.send_cmd('VER;\r\n')

    def clear(self, color='WHITE'):
        '''
        清屏
        '''
        color = self.color_dict[color] 
        self.send_cmd('CLR(%s);\r\n' % color)
    
    def background(self, color='WHITE'):
        color = self.color_dict[color] 
        self.send_cmd('SBC(%s);\r\n' % color)

    def brightness(self, level):
        '''
        调整画面亮度
        value 越大, 背光效果越强
        '''
        level = 255 - level       
        self.send_cmd('BL(%s);\r\n' % level)

    def direction(self, direction='HORIZONTAL'):
        '''
        设置显示方向
        '''
        direction = self.direction_dict[direction]
        self.send_cmd('dir(%s);\r\n' % direction)

    def point(self, x, y, color='BLACK'):
        '''
        绘制一个点
        '''
        color = self.color_dict[color]
        
        self.send_cmd('PS({0},{1},{2});\r\n'.format(x, y, color))

    def circle(self, x, y, r, color='BLACK', is_fill=False):
        '''
        绘制圆
        '''
        color = self.color_dict[color]
        if is_fill:
            # 绘制填充圆
            self.send_cmd('CIRF({0},{1},{2},{3});\r\n'.format(
                x, y, r, color))
        else:
            # 绘制空心圆
            self.send_cmd('CIR({0},{1},{2},{3});\r\n'.format(
                x, y, r, color))
        
    def line(self, x1, y1, x2, y2, color='BLACK'):
        '''
        绘制直线
        '''
        color = self.color_dict[color]

        self.send_cmd('PL({0},{1},{2},{3},{4});\r\n'.format(
            x1, y1, x2, y2, color))
    

    def rect(self, x, y, w, h, color='BLACK', is_fill=False):
        '''
        绘制矩形
        '''
        color = self.color_dict[color]

        if is_fill:
            self.send_cmd('BOXF({0},{1},{2},{3},{4})'.format(
                x, y, x + w, y + h, color))
        else:
            self.send_cmd('BOX({0},{1},{2},{3},{4})'.format(
                x, y, x + w, y + h, color))
        
        # 很奇怪, 我也不知道为什么绘制矩形这么奇怪
        self.clear()
    
    def text(self, x, y, text, size='MIDDLE', color='BLACK'):
        '''
        绘制文本
        '''

        size = self.font_size_dict[size] 
        color = self.color_dict[color]

        if type(text) == bytes:
            # 发送中文 比特 GB2312编码
            cmd = "DC{0}({1},{2},".format(size, x, y).encode()
            cmd += text
            cmd += ",{0});\r\n".format(color).encode()
            self.send_cmd(cmd)
        else:
            self.send_cmd("DC{4}({0},{1},{2},{3});\r\n".format(x,y,text,color, size))

if __name__ == '__main__':
    uscreen = UartScreen()
    # 显示中文1Z实验室
    # 注: 中文编码为GB2312
    uscreen.text(0, 0,  b'1Z\xca\xb5\xd1\xe9\xca\xd2', size='LARGE')
    # 显示PyESPCar
    uscreen.text(0, 200,  'PyESPCar', size='LARGE')