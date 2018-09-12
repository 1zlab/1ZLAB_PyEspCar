# -*- coding:utf-8 -*-
from machine import I2C,Pin
from car_config import gpio_dict, car_property
from cloud_platform import CloudPlatform

# 创建一个I2C对象
i2c = I2C(
    scl=Pin(gpio_dict['I2C_SCL']),
    sda=Pin(gpio_dict['I2C_SDA']),
    freq=car_property['I2C_FREQUENCY'])

# 创建云台对象
cp = CloudPlatform(i2c)