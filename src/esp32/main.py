'''
程序入口
'''
from machine import Pin
import utime

if __name__ == '__main__':
    # MQTT小车控制模式
    exec(open('mqtt_control_mode.py').read(), globals())