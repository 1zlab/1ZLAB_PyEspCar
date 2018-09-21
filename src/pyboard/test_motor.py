from motor import Motor

left_motor = Motor(0, is_debug=True)
right_motor = Motor(1, is_debug=True)

left_motor.speed = 50
right_motor.speed = 50