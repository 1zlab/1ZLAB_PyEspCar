import micropython
from machine import Timer
from car_config import car_property
from car import Car
import utime

# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)

# 创建一个小车
car = Car(is_debug=True)

# 停止 只测速不驱动电机
# car.stop_flag = True
# car.left_msc.stop_flag = True
# car.right_msc.stop_flag = True

# 创建定时器 这里用的是定时器4
timer = Timer(5)
# 设置定时器回调 100ms执行一次
ctl_period = int(car_property['PID_CTL_PERIOD']*1000) # 控制周期，转换为ms
timer.init(period=ctl_period, mode=Timer.PERIODIC, callback=lambda t: car.callback(t))


def quit():
    import gc
    global timer
    global car
    timer.deinit()
    car.deinit()
    gc.collect()


car.speed(0.5)

print('Run')
while True:
    if car.pose.y >= 100:
        print('Move 1m')
        car.stop()
        break
    utime.sleep_ms(50)

print('Stop')
print('Pose: {}'.format(car.pose))