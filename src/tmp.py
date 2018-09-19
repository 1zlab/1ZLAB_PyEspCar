def update_gy25_frame(uart):
    global yaw
    global pitch
    global roll

    if uart.any() < 8:
        return False
    
    raw_data = uart.read(8)
    if is_legal_data(raw_data):
        (yaw, pitch, roll) = parse_gy25(data)
        print('Yaw: {} Pitch: {} Roll: {}'.format(yaw, pitch, roll))
        return True
    else:
        while uart.any() and not is_legal_data(raw_data):
            raw_data = list(raw_data)
            raw_data.pop(0)
            raw_data.append(list(uart.read(1))[0])
            raw_data = bytes(raw_data)

            if is_legal_data(raw_data):
                print('raw_data2: {}'.format(raw_data))
                (yaw, pitch, roll) = parse_gy25(data)
                print('Yaw: {} Pitch: {} Roll: {}'.format(yaw, pitch, roll))
                return True
        return False
while True:
    ret = update_gy25_frame(uart)
    utime.sleep_ms(5)