'''
小车MQTT控制模式
'''
from umqtt.simple import MQTTClient
import time
import micropython
from machine import Timer
from car import Car

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
    'MOVE': car.move
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
client.connect()

client.subscribe(MQTT_TOPIC_ID)


while True:
    # 查看是否有数据传入
	# 有的话就执行 mqtt_callback
	client.check_msg()
	time.sleep(0.1)