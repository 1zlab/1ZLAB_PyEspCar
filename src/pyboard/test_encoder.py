from encoder import Encoder
import utime

left_encoder = Encoder(0, is_quad_freq=True, reverse=False)
right_encoder = Encoder(1, is_quad_freq=True, reverse=False)


while True:
    print('Left Encoder')
    print(left_encoder)
    print('Right Encoder')
    print(right_encoder)

    utime.sleep_ms(100)