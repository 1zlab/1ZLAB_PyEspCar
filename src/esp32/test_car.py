import micropython
from machine import Timer
from car_config import car_property
from car import Car
import utime

# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)

# 创建一个小车
car = Car(is_debug=True)