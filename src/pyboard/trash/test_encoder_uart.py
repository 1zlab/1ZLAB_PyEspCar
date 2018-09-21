from machine import UART
from encoder import Encoder
import utime

left_encoder = Encoder(0, is_quad_freq=True)
right_encoder = Encoder(1, is_quad_freq=True)

uart = UART(1, 114200)
uart.init(114200, bits=8, parity=None, stop=1) # init with given parameters


while True:
    data = '{},{}\n'.format(left_encoder.distance, 0)
    # right_encoder.distance
    print('SEND: {}'.format(data))
    uart.write(data)
    utime.sleep_ms(100)