# main.py -- put your code here!
from pyb import ADC,Pin,Timer
import time

pin_a=Pin('A0',Pin.AF_PP,pull=Pin.PULL_NONE,af=Pin.AF1_TIM2)
pin_b=Pin('A1',Pin.AF_PP,pull=Pin.PULL_NONE,af=Pin.AF1_TIM2)

enc_timer = Timer(2,prescaler=0, period=60000)
enc_channel = enc_timer.channel(1,Timer.ENC_AB)


while True:
    counter = enc_timer.counter()
    print(counter)
    time.sleep(0.1)