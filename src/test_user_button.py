'''
测试用户按键
'''
from user_button import UserButton
from car_config import gpio_dict

# 小车停止标志位
stop_flag = False

def callback(pin):
    '''
    回调函数
    改变小车的标志位
    '''
    global stop_flag
    # 标志位取反
    stop_flag = not stop_flag
    print("小车是否停止: {}".format(stop_flag))

# 用户按键引脚编号
USER_BUTTON = gpio_dict['USER_BUTTON']
# 创建UserButton对象
btn = UserButton(USER_BUTTON, callback)

try:
    while True:
        pass
except:
    btn.deinit()