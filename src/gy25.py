'''
GY-25 module contains MPU-6050 and STM 32F030F4P6 (ARM CPU).
GY-25模块集成了MPU6050还有STM32的一款芯片

解析GY-25模块串口发送回来的数据
    * 0xAA 帧头
    * yaw 偏航角 ： 绕Z轴旋转
    * pitch 俯仰角： 绕Y轴旋转
    * roll 横滚角： 绕X轴旋转
    * 0x55 帧尾
'''
from machine import UART,Pin
from car_config import gpio_dict
import utime
import ustruct


class EulerAngle:
    '''
    欧拉角
    '''
    def __init__(self, yaw, pitch, roll):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def update(self, yaw, pitch, roll):
        self.yaw, self.pitch, self.roll = yaw, pitch, roll
    
    def __str__(self):
        return 'Yaw: {}, pitch: {}, roll: {}'.format(self.yaw, self.pitch, self.roll)

class GY25:

    FRAME_PROTOCAL = '>BhhhB'
    FRAME_LENGTH = 8
    FRAME_BEGIN = 0xAA
    FRAME_END = 0x55
    
    def __init__(self, uart, is_debug=False):
        self.uart = uart
        self.angle = EulerAngle(0, 0, 0) # init euler angle
        self.is_debug = is_debug
    
    def is_legal_frame(self, frame_bytes):
        # verify frame length
        if len(frame_bytes) != GY25.FRAME_LENGTH:
            return False
        
        # verify frame begin and end
        frame_begin, yaw,pitch, roll, frame_end= ustruct.unpack(GY25.FRAME_PROTOCAL, frame_bytes)
        if frame_begin == GY25.FRAME_BEGIN and frame_end == GY25.FRAME_END:
            return True
        
        return False
    
    def parse_frame(self, frame_bytes):

        if not self.is_legal_frame(frame_bytes):
            return (None, None, None)
        # parase frame data
        begin, yaw,pitch, roll, end= ustruct.unpack(GY25.FRAME_PROTOCAL, frame_bytes)
        yaw /= 100
        pitch /= 100
        roll /= 100

        self.angle.update(yaw, pitch, roll)
        return (yaw, pitch, roll)

    def update(self):
        # frame not ready
        if self.uart.any() < GY25.FRAME_LENGTH:
            return False
        # read data
        frame_bytes = uart.read(GY25.FRAME_LENGTH)
        # fix the current frame
        while not self.is_legal_frame(frame_bytes) and uart.any():
            frame_bytes = frame_bytes + uart.read(1)
            frame_bytes = frame_bytes[1:]

        if self.is_legal_frame(frame_bytes):
            # frame data is legal
            self.angle.update(*self.parse_frame(frame_bytes))

            if self.is_debug:
                print(self.angle)
            return True
        return False


if __name__ == '__main__':

    uart = UART(2, baudrate=115200, rx=gpio_dict['UART1_RX'], tx=gpio_dict['UART1_TX'],timeout=10)
    # uart = UART(2, baudrate=115200, rx=12, tx=13,timeout=10)
    gy25 = GY25(uart, is_debug=True)

    while True:
        ret = gy25.update()
        utime.sleep_ms(5)