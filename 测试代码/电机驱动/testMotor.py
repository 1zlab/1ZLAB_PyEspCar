from Motor import *

# 右侧电机
rmotor = Motor(A4950T_AIN1, A4950T_AIN2)
rmotor.set_speed(-250)

# 左侧电机
lmotor = Motor(A4950T_BIN1, A4950T_BIN2) #,motor_install_dir=False)
lmotor.set_speed(-250)