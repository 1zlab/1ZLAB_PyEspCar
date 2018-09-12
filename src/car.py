'''
小车对象

功能描述：

API参考ROS的TurtleSim

目标： 同时控制前进距离与速度

1. 小车前进多少米 精确
2. 小车旋转多少度 （原地自旋）
3. 小车可以在地上绘制1ZLAB
4. 小车速度控制 + 角度控制

## 定速控制
已ok 当v > 0.5 以上的时候,小车可以正确的走直线

## 定距控制

'''
import math
import utime
from machine import Pin,Timer,I2C

from car_config import car_property, gpio_dict
from battery_voltage import BatteryVoltage
from user_button import UserButton
from motor import Motor
from encoder import Encoder
from pid_motor import MotorSpeedControl
from servo import CloudPlatform

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

    def __str__(self):
        return 'x: {}, y: {}, theta:{}, linear_v: {}, angular_v:{}'.format(
            self.x, 
            self.y, 
            self.theta,
            self.linear_velocity,
            self.angular_velocity)

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
        
        # 创建一个I2C对象
        i2c = I2C(
            scl=Pin(gpio_dict['I2C_SCL']),
            sda=Pin(gpio_dict['I2C_SDA']),
            freq=car_property['I2C_FREQUENCY'])

        # 创建舵机云台对象
        self.cloud_platform = CloudPlatform(i2c)

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
        
        # # 左侧电机的角度控制
        # self.left_mac = MotorAngleControl(
        #     self.left_motor,
        #     self.left_encoder,
        #     kp = car_property['LEFT_MOTOR_ANGLE_CTL_KP'],
        #     ki = car_property['LEFT_MOTOR_ANGLE_CTL_KI'],
        #     kd = car_property['LEFT_MOTOR_ANGLE_CTL_KD'],
        #     max_bias_sum = car_property['LEFT_MOTOR_ANGLE_CTL_MAX_BIAS_SUM'],
        #     is_debug = False)
        # # 右侧电机的角度控制
        # self.right_mac = MotorAngleControl(
        #     self.right_motor,
        #     self.right_encoder,
        #     kp = car_property['RIGHT_MOTOR_ANGLE_CTL_KP'],
        #     ki = car_property['RIGHT_MOTOR_ANGLE_CTL_KI'],
        #     kd = car_property['RIGHT_MOTOR_ANGLE_CTL_KD'],
        #     max_bias_sum = car_property['RIGHT_MOTOR_ANGLE_CTL_MAX_BIAS_SUM'],
        #     is_debug = False)
        
        # 小车控制模式 默认状态为角度控制
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['STOP']
        
        # 小车停止标志位
        self.stop_flag = False
        self.is_debug = is_debug # 是否开始调试模式
        
        # 执行单次的计时器
        # self.one_shot_timer = Timer(car_property['CAR__ID'])

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
    
    def update_pose(self):
        '''
        根据运动控制学 更新当前的位姿
        TODO v_left = v_right的情况
        TODO v_left = -v_right的情况?
        BUG 运动学模型仅仅适合两个轮子速度 同为正或者同为负的情况.
        '''
        # 将角度变化量变为左右两侧电机的直线速度
        v_left = self.motor_angle_to_velocity(self.left_msc._speed)
        v_right = self.motor_angle_to_velocity(self.right_msc._speed)

        # 旋转半径 默认为无穷大
        r = 1000000000000 # 旋转半径
        if v_left != v_right:
            # 计算旋转半径
            r = 0.5 * car_property['CAR_WIDTH'] * (v_left + v_right) / (v_right - v_left)
        
        # 计算得到小车的速度
        v_car = (r * v_right) / (r + car_property['CAR_WIDTH'] / 2)
        # 计算当前的偏转角度
        theta = math.atan(car_property['CAR_LENGTH'] / r)
        
        delta_t = car_property['PID_CTL_PERIOD']
        
        # 更新线速度
        self.pose.linear_velocity = v_car
        # 更新角速度
        self.pose.angular_velocity = v_car / r
        # 更新小车的偏转角度 (弧度值)
        self.pose.theta = delta_t * self.pose.angular_velocity
        # 更新小车的坐标
        move_dis = delta_t * self.pose.linear_velocity
        self.pose.x += move_dis * math.cos(self.pose.theta)
        self.pose.y += move_dis * math.sin(self.pose.theta)
    
    def callback(self, timer):
        '''
        小车PID控制回调函数
        '''
        # 电池ADC采样回调
        self.battery_adc.callback(timer)
        # 回调函数
        self.left_msc.callback(timer)
        self.right_msc.callback(timer)
        
        # BUG 更新当前的位姿
        # self.update_pose()
        
        # if not self.stop_flag:
        #     if self.car_ctl_mode == car_property['CAR_CTL_MODE']['GO_STRAIGHT']:
        #         # 小车走直线的控制模式
        #         diff = self.left_encoder.position - self.right_encoder.position

        #         # 添加两轮角度校准, 确保走直线
        #         self.left_msc.stop_flag = diff > 10
        #         self.right_msc.stop_flag = diff < -10 # abs(self.left_encoder.position) < abs(self.right_encoder.position)
        #         # 进入小车速度控制模式
        #         self.left_msc.callback(timer)
        #         self.right_msc.callback(timer)
        #     elif self.car_ctl_mode == car_property['CAR_CTL_MODE']['POINT_TURN']:
        #         # 原地旋转模式 
        #         # TODO ?
        #         # 添加两轮角度校准, 确保原地旋转
        #         self.left_msc.stop_flag = abs(self.left_encoder.position) > abs(self.right_encoder.position)
        #         self.right_msc.stop_flag = abs(self.left_encoder.position) < abs(self.right_encoder.position)
        #         # 进入小车速度控制模式
        #         self.left_msc.callback(timer)
        #         self.right_msc.callback(timer)
        #     elif self.car_ctl_mode == car_property['CAR_CTL_MODE']['SPEED']:
        #         # 速度控制模式
        #         self.left_msc.callback(timer)
        #         self.right_msc.callback(timer)
        #     elif self.car_ctl_mode == car_property['CAR_CTL_MODE']['STOP']:
        #         # 进入小车停止位控制模式
        #         self.left_mac.callback(timer)
        #         self.right_mac.callback(timer)
            
            
    def distance2angle(self, distance):
        '''
        将距离转换为电机旋转角度
        '''
        delta_angle = 360 * distance / (2 * math.pi * car_property['WHEEL_RADIUS'])
        return delta_angle

    def go_forward(self, distance=None, speed=0.5):
        '''
        小车前进
        '''
        if distance is None:
            # 设置为速度模式
            self.speed(speed)
        else:
            self.go(distance, speed=speed)
    
    def go_backward(self, distance=None, speed=0.5):
        '''
        小车后退
        '''
        if distance is None:
            self.speed(-1*speed)
        else:
            self.go(-1*distance,speed=-1*speed)
        

    def go(self, distance, speed=0.5):
        '''
        小车直线前进 Go Straight
        TODO 改为编码器角度控制
        @distance 小车前进距离单位m
        @speed 小车前进速度 m/s
        '''
        # 控制模式为走直线模式
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['GO_STRAIGHT']

        # 矫正速度        
        if distance < 0:
            # 向后移动的情况 速度必须为负值
            speed = -1*abs(speed)
        
        # 计算左侧编码器对应位置
        target_posi = self.distance2angle(distance)
        # 运动学控制
        self.kinematic_analysis(speed, 0, 
            left_target_posi=target_posi,
            right_target_posi=target_posi)

    
    def turn_left(self, speed=0.5):
        '''
        小车左转
        '''
        self.turn(turn_dir=-1, speed=speed)

    def turn_right(self, speed=0.5):
        '''
        小车右转
        '''
        self.turn(turn_dir=1, speed=speed)

    
    def turn(self, turn_dir=1, speed=0.5):
        '''
        小车原地旋转 point-turn
        默认旋转线速度是 0.3m/s

        @dir: 
            1  向左转
            -1 向右转
         
        '''
        # 控制模式为原地旋转模式
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['POINT_TURN']

        # # 将小车旋转角度转换为电机前进距离
        # distance = (angle / 360) *  math.pi * car_property['CAR_WIDTH'] 
        # # 计算时延
        # time_ms = int(abs(distance / speed) * 1000 * scalar)
        # 计算每个控制周期内电机的旋转角度
        motor_speed = self.velocity_to_motor_angle(speed)
        # 初始化
        self.left_msc.init()
        self.right_msc.init()
        
        # 电机反向旋转
        if turn_dir == 1:
            # 小车向右转
            self.left_msc.speed(1 * motor_speed)
            self.right_msc.speed(-1 * motor_speed)
        elif turn_dir == -1:
            self.right_msc.speed(1 * motor_speed)
            self.left_msc.speed(-1 * motor_speed)
        
        if self.is_debug:
            if turn_dir == 1:
                print('小车右转')
            # print('Rotate Angle: {}, motor_speed:{}, delay_ms: {}'.format(angle, motor_speed, time_ms))
        # # 等待ms
        # utime.sleep_ms(time_ms)
        # # 小车停止
        # self.stop()
    
    def stop(self):
        '''
        小车停止
        '''
        # # 自动切换为停止模式
        # self.car_ctl_mode = car_property['CAR_CTL_MODE']['STOP']
        self.speed(0)
        # self.left_mac.init()
        # self.right_mac.init()
        
        if self.is_debug:
            print('Car Stop')
    
    def speed(self, velocity, angle=0, delay_ms=None):
        '''
        小车速度控制模式
        @velocity: 小车直线速度
        @theta: 小车旋转角度
        @delay_ms: 延时时间
        '''
        # 设置控制模式为速度控制
        self.car_ctl_mode = car_property['CAR_CTL_MODE']['SPEED']
        # 设置延时时间
        self.kinematic_analysis(velocity, angle, delay_ms=delay_ms)
    
    def velocity_to_motor_angle(self, velocity):
        '''
        将速度(m/s)转换为控制周期内电机旋转角度(度)
        @velocity 速度, 单位m/s
        '''
        angle = 360 * (1 * velocity) / (2 * math.pi * car_property['WHEEL_RADIUS'])
        period = car_property['PID_CTL_PERIOD'] # PID控制周期 单位s
        # 1s内旋转的角度总和 / PID控制频率
        angle = angle / (1 / period)
        return angle
    def motor_angle_to_velocity(self, angle):
        '''
        将角度转换为直线速度
        '''
        period = car_property['PID_CTL_PERIOD'] # PID控制周期 单位s
        angle *= (1 / period) # 转换成每s电机旋转的角度
        # 计算得到直线速度 m / s
        velocity = (angle / 360) * (2 * math.pi * car_property['WHEEL_RADIUS'])
        return velocity


    def kinematic_analysis(self, velocity, angle, delay_ms=None, left_target_posi=None, right_target_posi=None):
        '''
        运动学分析与控制
        @velocity: 小车前进的直线速度, 单位m/s
        @angle： 小车的旋转角度, 单位 度
        @time: 小车的前进时间, 单位ms

        TODO 此运动学控制模型, 仅适合两个轮子速度同为正,或者同为负的时候
        '''
        # 初始化
        self.left_msc.init()
        self.right_msc.init()

        max_v = car_property['CAR_MAX_SPEED']
        # velocity 速度规约
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

              
        if delay_ms is not None:
            '''
            定时操作
            '''
            print('定时器 等待{} ms'.format(delay_ms))
            # 定时器只运行一次
            # TODO 定时器不好使
            # self.one_shot_timer.init(period=time_ms, mode=Timer.ONE_SHOT, callback=lambda t:self.stop())
            utime.sleep_ms(delay_ms)
            self.stop()

    def help(self):
        '''
        TODO 打印帮助信息
        1. 小车的API文档
        2. 小车的车身信息 宽高等
        '''
        pass

    def deinit(self):
        '''
        释放资源
        '''
        self.battery_adc.deinit()
        self.user_button.deinit()
        # mac 与 msc只需要销毁一次
        # self.left_mac.deinit()
        # self.right_mac.deinit()
        # self.tmp_timer.deinit()
