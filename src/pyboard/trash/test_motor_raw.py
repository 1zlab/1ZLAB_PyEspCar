from pyb import Timer

timer = Timer(5, freq=1000)

motor_a = timer.channel(3, Timer.PWM, pin=pyb.Pin.board.X3, pulse_width=0)
motor_b = timer.channel(4, Timer.PWM, pin=pyb.Pin.board.X4, pulse_width=0)

