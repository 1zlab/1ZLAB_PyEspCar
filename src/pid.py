import micropython
# 分配报错缓存区
micropython.alloc_emergency_exception_buf(100)


class PID(object):
    '''
    PID控制类
    '''
    def __init__(self, kp, ki=0, kd=0, target_value=0):
        self.kp = kp # 比例系数
        self.ki = ki # 积分系数
        self.kd = kd # 微分系数
        self.target_value = target_value # 目标值
        self.cur_bias = 0  # 最近一次的误差 err_k 
        self.last_bias = 0  # 上一次的误差 err_k-1
        self.bias_sum = 0   # 累积误差
    
    def set_target_value(self, target_value):
        '''
        设置目标值
        '''
        self.target_value = target_value

    def update(self, real_value):
        '''
        更新偏差
        '''
        # 计算偏差
        self.cur_bias = real_value - self.target_value
        # 更新偏差的积分
        self.bias_sum += self.cur_bias
        # 获取PID的控制结果
        result = self.kp*self.cur_bias + self.ki*self.bias_sum + self.kd*(self.cur_bias-self.last_bias)
        # 更新上次的误差
        self.last_bias = self.cur_bias
        return result