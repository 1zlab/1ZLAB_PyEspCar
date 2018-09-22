    # def kinematic_analysis(self, velocity, angle, delay_ms=None, left_target_posi=None, right_target_posi=None):
    #     '''
    #     运动学分析与控制
    #     @velocity: 小车前进的直线速度, 单位m/s
    #     @angle： 小车的旋转角度, 单位 度
    #     @time: 小车的前进时间, 单位ms

    #     TODO 此运动学控制模型, 仅适合两个轮子速度同为正,或者同为负的时候
    #     '''
    #     # 初始化
    #     self.left_msc.init()
    #     self.right_msc.init()

    #     max_v = car_property['CAR_MAX_SPEED']
    #     # velocity 速度规约
    #     if abs(velocity) > max_v:
    #         # 规约速度
    #         velocity = max_v if velocity > 0 else -1 * max_v
        
    #     # 角度转换为弧度
    #     theta = math.radians(angle)
    #     # 小车机械属性
    #     car_width = car_property['CAR_WIDTH'] # 小车宽度
    #     car_length = car_property['CAR_LENGTH'] # 小车长度
    #     # 根据速度与旋转角度，求解两个轮子差速
    #     left_velocity = velocity * (1 + car_width * math.tan(theta) / (2 * car_length))
    #     right_velocity = velocity * (1 - car_width * math.tan(theta) / (2 * car_length))
    #     # 将直线速度转换为小车电机角度旋转速度
    #     left_motor_angle_target = self.velocity_to_motor_angle(left_velocity)
    #     right_motor_angle_target = self.velocity_to_motor_angle(right_velocity)
        
    #     # 设定Target值
    #     self.left_msc.speed(left_motor_angle_target)
    #     self.right_msc.speed(right_motor_angle_target)

    #     if self.is_debug:
    #         print('Left Motor Speed Control : {}'.format(left_motor_angle_target))
    #         print('Right Motor Speed Control: {}'.format(right_motor_angle_target))

              
    #     if delay_ms is not None:
    #         '''
    #         定时操作
    #         '''
    #         print('定时器 等待{} ms'.format(delay_ms))
    #         # 定时器只运行一次
    #         # TODO 定时器不好使
    #         # self.one_shot_timer.init(period=time_ms, mode=Timer.ONE_SHOT, callback=lambda t:self.stop())
    #         utime.sleep_ms(delay_ms)
    #         self.stop()
    