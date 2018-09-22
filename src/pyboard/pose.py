'''
位姿
TODO Test
'''
from config import config

class Pose:
    '''
    小车的位姿描述
    '''
    CAR_WIDTH = config['CAR_WIDTH']

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
            math.degrees(self.theta),
            self.linear_velocity,
            self.angular_velocity)

    def reset(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.linear_velocity = 0
        self.angular_velocity = 0


    def update(self, v_left, v_right, delta_t):
        '''
        根据运动控制学 更新当前的位姿
        涉及到刚体运动学的知识
        参考文章
        https://blog.csdn.net/qq_16149777/article/details/73224070
        https://blog.csdn.net/u010422438/article/details/82256280
        '''
        # 旋转半径 默认为无穷大
        r = None # 旋转半径
        v_car = None # 小车速度
        if v_left == v_right:
            # 小车做直线运动
            r = 1e100 # 旋转半径为无穷大, 但是math没有 inf
            self.linear_velocity = v_left

        elif v_left == -v_right:
            # 小车做自旋运动
            r = 0
            self.linear_velocity = 0
        else:
            # 小车做曲弧运动
            # 计算旋转半径
            r = (Pose.CAR_WIDTH / 2) * ((v_left + v_right) / (v_left-v_right))
            self.linear_velocity = (v_left + v_right) / 2
        
        # 小车角度增量
        delta_theta =  (v_right - v_left) * delta_t / Pose.CAR_WIDTH
        # 更新角速度
        self.angular_velocity = delta_theta / delta_t

        # 更新小车的偏转角度 (弧度值)
        self.theta += delta_theta
        # 约束theta
        if self.theta > math.pi:
            self.theta -= math.pi
        
        elif self.theta < -math.pi:
            self.theta += math.pi
        
        # 更新小车的坐标(M点的轨迹方程)
        self.x += -1*(v_left + v_right) * math.sin(self.theta)
        self.y += (v_left + v_right) * math.cos(self.theta)