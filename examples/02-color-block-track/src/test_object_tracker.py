from object_tracker import ObjectTracker
import paho.mqtt.client as mqtt
from car_state import *
from pyespcar_sdk import PyCarSDK
import time

def on_message(client, userdata, msg):
    '''处理message回调'''
    global COLOR_BLOCK_TOPIC_ID

    # print('topic: {}'.format(msg.topic))
    # print('message: {}'.format(str(msg.payload)))

    if msg.topic == COLOR_BLOCK_TOPIC_ID:
        message = msg.payload.decode('utf-8')
        print('color_block_info: {}'.format(message))
        # update_object_tracker(message)


# 建立一个MQTT的客户端
client = mqtt.Client()
# 绑定数据接收回调函数
client.on_message = on_message

HOST_IP = 'localhost' # Server的IP地址
HOST_PORT = 1883 # mosquitto 默认打开端口
COLOR_BLOCK_TOPIC_ID = 'color_block_info' # TOPIC的ID

# 连接MQTT服务器
client.connect(HOST_IP, HOST_PORT, 60)
# 订阅主题
client.subscribe(COLOR_BLOCK_TOPIC_ID)


sdk = PyCarSDK(client, is_debug=True)
tracker = ObjectTracker(sdk)

tracker.switch_state(CarSearchAround)
time.sleep(5)
tracker.switch_state(CarStop)
