from machine import Pin


# 控制右侧电机(正向)
A4950T_AIN1 = 25 # 对应UNO底板 D3
A4950T_AIN2 = 27 # 对应UNO底板 D6

# A4950T 电机驱动引脚 GPIO编号
# 控制左侧电机(反向)
A4950T_BIN1 = 23 # 对应UNO底板 D11
A4950T_BIN2 = 16 # 对应UNO底板 D5

# Pin(A4950T_AIN1).value(1)
# Pin(A4950T_AIN2).value(0)

Pin(A4950T_BIN1,Pin.OUT).value(1)
Pin(A4950T_BIN2,Pin.OUT).value(0)

Pin(A4950T_BIN1,Pin.OUT).value(0)
Pin(A4950T_BIN2,Pin.OUT).value(1)