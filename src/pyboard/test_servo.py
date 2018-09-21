'''
舵机测试
舵机云台旋转到中间位置
'''
from servo import Servo

btm_servo = Servo(0, is_debug=True)
top_servo = Servo(1, is_debug=True)