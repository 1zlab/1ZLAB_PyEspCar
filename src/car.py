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

3. [BUG] move同样的幅度，前进与后退效果不一样，向后距离大一些
    且后向的前进举例更接近真实值
4. [BUG] move 0.1 0.2 0.5 实际前进距离指数式增加
    TODO 测试PWM不同取值，对应电机速度
    ?电机有一个启动时间
8. [BUG] 累积误差问题, 前进时间长了,角度偏移就越来越大
   [TODO] Move或者旋转之后,添加一个位姿修正
[TODO] 电机存在一个启动时间,而且可能是一个轮子先动,在旋转较小角度的时候,这个问题比较明显.
? 小车旋转角度的反馈信号
[TODO] PID速度控制 编码器改成增量式

[TODO] 前进距离与实际尺寸不符合
'''
import math
import utime
from machine import Pin,Timer

from car_config import car_property, gpio_dict
from battery_voltage import BatteryVoltage
from user_button import UserButton
from motor import Motor
from encoder import Encoder
from pid_motor import MotorSpeedControl,MotorAngleControl


class Pose:
    '''
    小车的位姿描述
    '''
    def __init__(self, x, y, theta, linear_velocity, angular_velocity):
        self.x = x # x坐标
        self.y = y # y坐标
        self.theta = theta # 角度
        self.linear_velocity = linear_velocity# 小车线速度
        self.angular_velocity = angular_velocity # 小车角速度 

class Car(object):
    def __init__(self, is_debug=False):
        '''
        Car构造器函数
        '''
        # 小车的位姿
        self.pose = Pose(0, 0, 0, 0, 0)

        # 电池ADC采样
        self.battery_adc = BatteryVoltage(
            gpio_dict['BATTERY_ADC'],
            is_debug=False)
        
        # 用户按键
        self.user_button = UserButton(
            gpio_dict['USER_BUTTON'], 
            callback=lambda timer: self.user_button_callback(timer))
        
        # 左侧电机
        self.left_motor = Motor(
            gpio_dict['LEFT_MOTOR_A'],
            gpio_dict['LEFT_MOTOR_B'], 
            motor_install_dir=car_property['LEFT_MOTOR_INSTALL_DIR'])
        self.left_motor.stop() # 左侧电机停止
        
        # 右侧电机
        self.right_motor = Motor(
            gpio_dict['RIGHT_MOTOR_A'], 
            gpio_dict['RIGHT_MOTOR_B'], 
            motor_install_dir=car_property['RIGHT_MOTOR_INSTALL_DIR'])
        self.right_motor.stop() # 右侧电机停止

        # 左侧编码器
        self.left_encoder = Encoder(
            Pin(gpio_dict['LEFT_ENCODER_A'], Pin.IN),
            Pin(gpio_dict['LEFT_ENCODER_B'], Pin.IN),
            reverse=car_property['LEFT_ENCODER_IS_REVERSE'], 
            scale=car_property['LEFT_ENCODER_ANGLE_SCALE'])
        # 右侧编码器
        self.right_encoder = Encoder(
            Pin(gpio_dict['RIGHT_ENCODER_A'], Pin.IN),
            Pin(gpio_dict['RIGHT_ENCODER_B'], Pin.IN),
            reverse=car_property['RIGHT_ENCODER_IS_REVERSE'], 
            scale=car_property['RIGHT_ENCODER_ANGLE_SCALE'])
        
        # 左侧电机速度控制
        self.left_msc = MotorSpeedControl(
            self.left_motor,
            self.left_encoder,
            kp = car_property['LEFT_MOTOR_SPEED_CTL_KP'],
            ki = car_property['LEFT_MOTOR_SPEED_CTL_KI'],
            kd = car_property['LEFT_MOTOR_SPEED_CTL_KD'],
            max_bias_sum = car_property['LEFT_MOTOR_SPEED_CTL_MAX_BIAS_SUM'], 
            is_debug=False)
        
        # 右侧电机速度控制
        self.right_msc = MotorSpeedControl(
            self.right_motor,
            self.right_encoder,
            kp = car_property['RIGHT_MOTOR_SPEED_CTL_KP'],
            ki = car_property['RIGHT_MOTOR_SPEED_CTL_KI'],
            kd = car_property['RIGHT_MOTOR_SPEED_CTL_KD'],
            max_bias_sum = car_property['RIGHT_MOTOR_SPEED_CTL_MAX_BIAS_SUM'],
            is_debug=False)
        
        # 左侧电机的角度控制
        self.left_mac = MotorAngleControl(
            self.left_motor,
            self.left_encoder,
            kp = car_property['LEFT_MOTOR_ANGLE_CTL_KP'],
            ki = car_property['LEFT_MOTOR_ANGLE_CTL_KI'],
            kd = car_property['LEFT_MOTOR_ANGLE_CTL_KD'],
            max_bias_sum = car_property['LEFT_MOTOR_ANGLE_CTL_MAX_BIAS_SUM'],
            is_debug = False)
        # 右侧电机的角度控制
        self.right_mac = MotorAngleControl(
            self.right_motor,
            self.right_encoder,
            kp = car_property['RIGHT_MOTOR_ANGLE_CTL_KP'],
            ki = car_property['RIGHT_MOTOR_ANGLE_CTL_KI'],
            kd = car_property['RIGHT_MOTOR_ANGLE_CTL_KD'],
            max_bias_sum = car_property['RIGHT_MOTOR_ANGLE_CTL_MAX_BIAS_SUM'],
            is_debug = False)
        
        # 小车控制模式 默认状态为角度控制
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['POSITION']
        
        # 小车停止标志位
        self.stop_flag = False
        self.is_debug = is_debug # 是否开始调试模式
        
        # 执行单次的计时器
        self.one_shot_timer = Timer(car_property['CAR_ONE_SHOT_TIMER_ID'])

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
            self.left_motor.stop()
            self.right_motor.stop()
        
        if self.is_debug:
            print('切换stopflag flag={}'.format(self.stop_flag))

    def callback(self, timer):
        '''
        小车PID控制回调函数
        '''
        # 电池ADC采样回调
        self.battery_adc.callback(timer)
        
        if not self.stop_flag:
            if self.car_ctl_mode == car_property['CAR_CTL_MODE']['SPEED']:
                # 添加两轮角度校准, 确保走直线
                self.left_msc.stop_flag = abs(self.left_encoder.position) > abs(self.right_encoder.position)
                self.right_msc.stop_flag = abs(self.left_encoder.position) < abs(self.right_encoder.position)

                # 进入小车速度控制模式
                self.left_msc.callback(timer)
                self.right_msc.callback(timer)
            elif self.car_ctl_mode == car_property['CAR_CTL_MODE']['POSITION']:
                # 进入小车位置控制模式
                self.left_mac.callback(timer)
                self.right_mac.callback(timer)
        
    def distance2angle(self, distance):
        '''
        将距离转换为电机旋转角度
        '''
        delta_angle = 360 * distance / (2 * math.pi * car_property['WHEEL_RADIUS'])
        return delta_angle

    def move(self, distance, speed=0.2):
        '''
        小车前进
        @distance 小车前进距离单位m
        @speed 小车前进速度 m/s

        '''
        
        # 计算前进时间
        time_ms = int(abs((distance / speed) * 1000))
        
        if distance < 0:
            speed = -1*speed
        # 运动学控制
        self.kinematic_analysis(speed, 0, time_ms)

    def rotate(self, angle, speed=0.3, scalar=2):
        '''
        小车旋转 角度
        默认旋转线速度是 0.3m/s
        
        旋转的时候,有损耗,需要添加一个比例系数(不准确)
        TODO
        45 2.2
        90 2
        180 1.8
        360 1.5
        720 1.32
        '''
        # 将小车旋转角度转换为电机前进距离
        distance = (angle / 360) *  math.pi * car_property['CAR_WIDTH'] 
        # 计算时延
        time_ms = int(abs(distance / speed) * 1000 * scalar)
        # 计算每个控制周期内电机的旋转角度
        motor_speed = self.velocity_to_motor_angle(speed)
        # 自动切换为速度控制
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['SPEED']
        # 初始化
        self.left_msc.init()
        self.right_msc.init()
        
        # 电机反向旋转
        if angle > 0:
            # 小车向右转
            self.left_msc.speed(1 * motor_speed)
            self.right_msc.speed(-1 * motor_speed)
        elif angle < 0:
            self.right_msc.speed(1 * motor_speed)
            self.left_msc.speed(-1 * motor_speed)
        
        if self.is_debug:
            print('Rotate Angle: {}, motor_speed:{}, delay_ms: {}'.format(angle, motor_speed, time_ms))
        # 等待ms
        utime.sleep_ms(time_ms)
        # 小车停止
        self.stop()
    
    def stop(self):
        '''
        小车停止
        '''
        # 运动学控制,速度设定为0
        self.kinematic_analysis(0, 0)
        utime.sleep_ms(100)

        # 自动切换为角度控制
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['POSITION']
        self.left_mac.init()
        self.right_mac.init()
        
        if self.is_debug:
            print('Car Stop')

    def velocity_to_motor_angle(self, velocity):
        '''
        将速度(m/s)转换为控制周期内电机旋转角度(度)
        '''
        angle = 360 * (1 * velocity) / (2 * math.pi * car_property['WHEEL_RADIUS'])
        period = car_property['PID_CTL_PERIOD'] # PID控制周期 单位s
        # 1s内旋转的角度总和 / PID控制频率
        angle = angle / (1 / period)
        return angle
    
    def kinematic_analysis(self, velocity, angle, time_ms=None, left_target_posi=None, right_target_posi=None):
        '''
        运动学控制
        @velocity: 小车前进的直线速度, 单位m/s
        @angle： 小车的旋转角度, 单位 度
        @time: 小车的前进时间, 单位ms
        '''
        
        # 自动切换为速度控制
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['SPEED']
        # 初始化
        self.left_msc.init()
        self.right_msc.init()

        max_v = car_property['CAR_MAX_SPEED'] # 小车最大线速度
        if abs(velocity) > max_v:
            # 规约速度
            velocity = max_v if velocity > 0 else -1 * max_v
        
        # 角度转换为弧度
        theta = math.radians(angle)
        # 小车机械属性
        car_width = car_property['CAR_WIDTH'] # 小车宽度
        car_length = car_property['CAR_LENGTH'] # 小车长度
        # 根据速度与旋转角度，求解两个轮子差速
        left_velocity = velocity * (1 + car_width * math.tan(theta) / (2 * car_length))
        right_velocity = velocity * (1 - car_width * math.tan(theta) / (2 * car_length))
        # 将直线速度转换为小车电机角度旋转速度
        left_motor_angle_target = self.velocity_to_motor_angle(left_velocity)
        right_motor_angle_target = self.velocity_to_motor_angle(right_velocity)
        
        # 设定Target值
        self.left_msc.speed(left_motor_angle_target, target_posi = left_target_posi)
        self.right_msc.speed(right_motor_angle_target, target_posi = right_target_posi)

        if self.is_debug:
            print('Left Motor Speed Control : {}'.format(left_motor_angle_target))
            print('Right Motor Speed Control: {}'.format(right_motor_angle_target))

              
        if time_ms is not None:
            '''
            定时操作
            '''
            print('定时器 等待{} ms'.format(time_ms))
            # 定时器只运行一次
            # TODO 定时器不好使
            # self.one_shot_timer.init(period=time_ms, mode=Timer.ONE_SHOT, callback=lambda t:self.stop())
            utime.sleep_ms(time_ms)
            self.stop()
            
    def deinit(self):
        '''
        释放资源
        '''
        self.battery_adc.deinit()
        self.user_button.deinit()
        # mac 与 msc只需要销毁一次
        self.left_mac.deinit()
        self.right_mac.deinit()
        # self.tmp_timer.deinit()
