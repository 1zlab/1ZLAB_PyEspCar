'''
PID工具类
'''
class PID:
    '''
    PID的基类
    '''
    def __init__(self, kp, ki=0, kd=0, target=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self._target = target # 设置目标值
        self.cur_bias = 0  # 最近一次的误差 err_k 
        self.pre_bias = 0  # 上一次的误差 err_k-1
        self.result = 0 # 被控制量
        
    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, value):
        self._target = value
        
    def reset(self):
        '''重新初始化PID'''
        pass
    
    def update(self, value):
        '''更新PID'''
        pass
    
    def __str__(self):
        return 'Kp={}, Ki={}, Kd={} Target={}'.format(self.kp, self.ki, self.kd, self._target)

class PositionPID(PID):

    def __init__(self, kp, ki=0, kd=0, target=0, max_bias_sum=None, max_bias_win=None):
        
        super().__init__(kp=kp, ki=ki, kd=kd, target=target)

        self.error_list = [] # 误差列表
        self.max_bias_sum = max_bias_sum # 积分上限
        self.max_bias_win = max_bias_win # 积分窗口
        self.bias_sum = 0   # 累积误差

    def reset(self):
        '''
        重新初始化
        '''
        self.error_list = []
        self.bias_sum = 0
        self.cur_bias = 0
        self.pre_bias = 0
        self.target = 0

    def update(self, value):
        ''' 
        位置式PID更新公式
            Result =Kp*e(k)+Ki*∑e(k)+Kd[e(k)-e(k-1)]
        '''

        # 更新当前的误差
        self.cur_bias = value - self._target

        if self.max_bias_win is not None:
            self.error_list.append(self.cur_bias)
            if len(self.error_list) > self.max_bias_win:
                old_err = self.error_list.pop(0) # 弹出队尾元素
                self.bias_sum -= old_err # 减去旧的error
        
        # 更新积分项
        self.bias_sum += self.cur_bias
        
        # 限制累积误差的范围
        if self.max_bias_sum is not None:
            if self.bias_sum < -1 * self.max_bias_sum:
                self.bias_sum = -1 * self.max_bias_sum
            elif self.bias_sum > self.max_bias_sum:
                self.bias_sum = self.max_bias_sum
        
        # 更新控制量的值
        self.result = self.kp * self.cur_bias + \
            self.ki * self.bias_sum + \
            self.kd * (self.cur_bias - self.pre_bias)
        # 更新上一次误差
        self.pre_bias = self.cur_bias

        return self.result

class IncrementalPID(PID):
    '''
    增量式PID
    '''
    def __init__(self, kp, ki=0, kd=0, target=0, max_result=None, min_result=None):
        # 调用父类的构造器
        super().__init__(kp=kp, ki=ki, kd=kd, target=target)
        # 控制量
        self.old_bias = 0  # 前一次的误差 err_k-2
        self.max_result = max_result
        self.min_result = min_result

    def reset(self):
        self.old_bias = 0
        self.pre_bias = 0
        self.cur_bias = 0
        self._target = 0
    
    def update(self, value):
        '''
        增量式PID更新公式
            Result +=Kp[e(k)-e(k-1)]+Ki*e(k)+Kd[e(k)-2e(k-1)+e(k-2)]
        增量式PID只与当前的误差还有上两次的误差有关
        '''
        # 计算当前的err
        self.cur_bias = value - self._target
        
        # 更新控制量的值
        self.result += self.kp*(self.cur_bias - self.pre_bias) + \
            self.ki*self.cur_bias + \
            self.kd*(self.cur_bias -2*self.pre_bias + self.old_bias)
        
        if self.min_result is not None and self.result < self.min_result:
            self.result = self.min_result
        if self.max_result is not None and self.result > self.max_result:
            self.result = self.max_result
        
        # 更新误差历史
        self.pre_bias, self.old_bias = self.cur_bias, self.pre_bias
    
        return self.result
