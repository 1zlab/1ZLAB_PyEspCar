'''
小车对象

功能描述：
* 设置两个电机的转速（速度采样） <-- 先写这个
* 设置两个电机的旋转角度/圈数

API参考ROS的TurtleSim

目标： 同时控制前进距离与速度

1. 小车前进多少米 精确
2. 小车旋转多少度 （原地自旋）
3. 小车可以在地上绘制1ZLAB
4. 小车速度控制 + 角度控制

[存在问题]
1. 小车有时候会莫名的开始自旋？（PID控制算法的问题，还是管脚的问题？）
2. 小车不走直线，两个电机速度不统一
3. move同样的幅度，前进与后退效果不一样，向前距离大一些
4. move 0.1 0.2 0.5 实际前进距离指数式增加
    TODO 测试PWM不同取值，对应电机速度
    ？有可能是速度快到一定程度，编码器的中断就处理不过来了
5. 电机在运行过程中抖动的厉害


'''
from car_config import car_property, gpio_dict
from battery_voltage import BatteryVoltage
from user_button import UserButton
from motor import Motor
from pid_motor import MotorAngleControl
import math
import utime


class Pose:

    def __init__(self, x, y, theta, linear_velocity, angular_velocity):
        self.x = x # x坐标
        self.y = y # y坐标
        self.theta = theta # 角度
        self.linear_velocity = linear_velocity# 小车线速度
        self.angular_velocity = angular_velocity # 小车角速度 

class Car(object):
    def __init__(self, left_mac, right_mac, is_debug=True):
        '''
        Car构造器函数
        '''
        # 电池ADC采样
        self.battery_adc = BatteryVoltage(gpio_dict['BATTERY_ADC'], is_debug=False)
        # 用户按键
        self.user_button = UserButton(gpio_dict['USER_BUTTON'], callback=self.user_button_callback)
        
        self.left_mac = left_mac # 左侧电机角度控制
        self.right_mac = right_mac # 右侧电机角度控制

        self.car_width = car_property['CAR_WIDTH'] # 后轮的轮距
        self.car_height = car_property['CAR_LENGTH'] # 前后轮的轮距
        
        self.pose = Pose(0, 0, 0, 0, 0) # 小车的位姿

        # 小车控制模式 默认状态为角度控制
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['POSITION'] 
        
        self.stop_flag = False # 小车停止标志位

        self.is_debug = is_debug
        
        # TODO 声明 定义定时器 100ms的回调函数

    def user_button_callback(self, pin):
        '''
        切换小车的停止位
        TODO 这里有BUG
        '''
        # 延时200ms 按键消抖
        utime.sleep_ms(200)

        self.stop_flag = not self.stop_flag
        if self.stop_flag:
            # 电机停止
            self.left_mac.motor.stop()
            self.right_mac.motor.stop()
        
        if self.is_debug:
            print('切换stopflag flag={}'.format())

    def callback(self, timer):
        self.battery_adc.callback(timer)
        
        if not self.stop_flag:
            self.left_mac.callback(timer, min_threshold=5)
            self.right_mac.callback(timer, min_threshold=5)

    def distance2angle(self, distance):
        '''
        将距离转换为电机旋转角度
        '''
        delta_angle = 360 * distance / (2 * math.pi * car_property['WHEEL_RADIUS'])
        return delta_angle

    def move(self, distance, max_speed=None):
        '''
        小车前进距离 distance单位m
        TODO 设置前进时候的最大速度
        '''
        # 将前进距离，修改为旋转角度增量
        delta_angle = self.distance2angle(distance)
        print('Move Distance: {}  Angle:{}'.format(distance, delta_angle))
        # 更新左侧电机的PID目标值
        self.left_mac.pid.target_value = self.left_mac.encoder.position + delta_angle
        # 更新右侧电机的PID目标值
        self.right_mac.pid.target_value = self.right_mac.encoder.position + delta_angle
        

    def rotate(self, angle, max_speed=None):
        '''
        小车旋转 角度
        TODO 设置旋转的最大角速度
        '''
        pass
    
    def stop(self):
        # 状态自动切换到角度控制
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['POSITION']
        self.kinematic_analysis(0, 0)

    def kinematic_analysis(self, velocity, angle):
        '''
        运动学控制
        '''
        pass
    
    def deinit(self):
        '''
        释放资源
        '''
        self.battery_adc.deinit()
        self.user_button.deinit()
        self.left_mac.deinit()
        self.right_mac.deinit()
    

    