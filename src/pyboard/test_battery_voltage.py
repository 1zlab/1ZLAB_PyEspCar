from battery_voltage import BatteryVoltage
from pyb import Timer
import utime

timer = Timer(4, freq=100)

bv = BatteryVoltage(is_debug=True)


sample_flag = False

def bv_callback(tim):
    global sample_flag

    if not sample_flag:
        sample_flag = True

timer.callback(bv_callback)

while True:
    if sample_flag:
        bv.sample()
        print('volatage: {}'.format(bv.battery_voltage))

        sample_flag = False
    

    utime.sleep_ms(200)