from machine import Pin

pina = Pin('X1', Pin.IN)
pinb = Pin('X2', Pin.IN)



old_a = 0
old_b = 0

count = 0
while True:
    new_a = pina.value()
    new_b = pinb.value()

    if new_a != old_a or new_b != old_b:
        count+=1
        print('CNT: {} A: {} B: {}'.format(count, new_a, new_b))
        old_a = new_a
        old_b = new_b
