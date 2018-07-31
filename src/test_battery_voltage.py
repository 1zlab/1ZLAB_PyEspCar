from battery_voltage import BatteryVoltage
from car_config import gpio_dict


bv = BatteryVoltage(gpio_dict['BATTERY_ADC'], is_debug=True)