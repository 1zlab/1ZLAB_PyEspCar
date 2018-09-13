'''
串口调试工具 Uart Debug Tools
'''

class UartPidParamAdjust():
    '''
    串口PID调参
    '''
    def __init__(self, pid, uart, is_debug):
        self.pid = pid
        self.uart = uart

        self.is_debug = is_debug

        self.cmd_list = {
            'SET_PID': self.update_pid_param,
            'SET_TARGET': self.update_target,
        }

    def callback(self, timer, new_real):
        '''
        回调函数
        '''
        # 发送真实值
        self.send_real(new_real)
        # 检测串口是否有数据读入
        if self.uart.any():
            data_byte = self.uart.readline()
            data_str = data_byte.decode('utf-8')
            self.command(data_str)
        
    def command(self, data_str):
        '''
        根据指令字符,执行特定的指令
        '''
        if self.is_debug:
            print('[INFO] Recieve： {}'.format(data_str))
        
        params = data_str.split(',')
        cmd_str = params[0]
        if cmd_str in self.cmd_list:
            self.cmd_list[cmd_str](*params[1:])
        else:
            print('[ERROR] Ukown Command : {}'.format(data_str))

    def update_pid_param(self, new_kp, new_ki, new_kd):
        '''
        更新PID参数
        '''
        self.pid.kp = float(new_kp)
        self.pid.ki = float(new_ki)
        self.pid.kd = float(new_kd)
        
        if self.is_debug:
            print('set param Kp = {}, Ki = {}, Kd = {}'.format(new_kp, new_ki, new_kd))
            print('new pid: {}'.format(self.pid))

    def update_target(self, new_target):
        '''
        更新目标值
        '''
        new_target = float(new_target)
        self.pid.set_target_value(new_target)
        
        if self.is_debug:
            print('new target: {}'.format(self.pid.target_value))

    def send_real(self, new_real):
        '''
        更新真实值
        '''
        data_str = ','.join(['REAL_VALUE', str(new_real)])
        data_str += '\n' # 添加换行符号
        data_byte = data_str.encode('utf-8')
        self.uart.write(data_byte)