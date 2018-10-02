'''
小车MQTT控制模式
'''
from umqtt.simple import MQTTClient
import time
import micropython
from machine import Timer
from car import Car
import gc

# 设定紧急意外缓冲区的大小为100
micropython.alloc_emergency_exception_buf(100)

# 创建一个小车
car = Car(is_debug=True)

cmd_dict = {
    'TURN_LEFT': car.turn_left,
    'TURN_RIGHT': car.turn_right,
    'GO_FORWARD': car.go_forward,
    'GO_BACKWARD': car.go_backward,
    'CP_UP': car.cloud_platform.up,
    'CP_DOWN': car.cloud_platform.down,
    'CP_LEFT': car.cloud_platform.left,
    'CP_RIGHT': car.cloud_platform.right,
    'CP_RESET': car.cloud_platform.reset,
    'STOP': car.stop,
    'MOVE': car.move,
    'SET_BOTTOM_SERVO_ANGLE':car.cloud_platform.bottom_servo.angle,
    'SET_TOP_SERVO_ANGLE': car.cloud_platform.top_servo.angle,
}


def command_process(cmd_str):
    global car
    params = cmd_str.split(',')
    cmd_name = params[0]
    if len(params) > 1:
        cmd_dict[cmd_name](*params[1:])
    else:
        cmd_dict[cmd_name]()


def mqtt_callback(topic, msg):
    global MQTT_TOPIC_ID
    print('topic: {}'.format(topic))
    print('msg: {}'.format(msg))
    if topic == MQTT_TOPIC_ID:
        command_process(msg.decode())
	

SERVER = '192.168.43.16'
CLIENT_ID = 'PYESPCAR_A0'
MQTT_TOPIC_ID = b'PYESPCAR_CTL_MSG'

client = MQTTClient(CLIENT_ID, SERVER)
client.set_callback(mqtt_callback)
print('[INFO] Connect to the MQTT Broker')
result = client.connect()
print('result code : {}'.format(result))
if result == 0:
    print('[INFO] Sucess!! Connect to the MQTT Broker')
else:
    print('[INFO] Fail to connect to mqtt broker')
    exit(-1)

print('[INFO] Subscribe Topic: {}'.format(MQTT_TOPIC_ID))
client.subscribe(MQTT_TOPIC_ID)


while True:
    try:
        # 查看是否有数据传入
	    # 有的话就执行 mqtt_callback
	    client.check_msg()
	    # utime.sleep_ms(5)
    except KeyboardInterrupt as e:
        print(e)
        print('[INFO] Quit MQTT check_msg mode')
        break
    except Exception as e:
        print('[ERROR] MQTT')
        print(e)
        gc.collect()
        client.connect()