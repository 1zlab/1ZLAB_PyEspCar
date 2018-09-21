import utime
from machine import UART
from car_config import gpio_dict

uart = UART(1, baudrate=115200, rx=gpio_dict['UART2_RX'], tx=gpio_dict['UART2_TX'], timeout=10)

while True:
    if uart.any():
        data = uart.readline()
        print(data)
    utime.sleep_ms(50)
