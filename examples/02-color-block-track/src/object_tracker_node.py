import paho.mqtt.client as mqtt
from pyespcar_sdk import PyCarSDK
from object_tracker import ObjectTracker
import time

def update_object_tracker(message):
    global tracker

    timestamp, is_object_in_view, x_offset, y_offset, area_offset = message.split(',')
    now = int(round(time.time()*1000))

    if now - int(timestamp) > 50:
        # 时间间隔大于50ms，数据过期
        print('[INFO] data is out of date')
        return
    
    is_object_in_view = is_object_in_view == 'True'
    x_offset = float(x_offset)
    y_offset = float(y_offset)
    area_offset = float(area_offset)
    
    try:
        tracker.update(is_object_in_view, x_offset, y_offset, area_offset)
    except Exception as e:
        print('[ERROR]: ')
        print(e)
        time.sleep(5)

def on_message(client, userdata, msg):
    '''处理message回调'''
    global COLOR_BLOCK_TOPIC_ID

    # print('topic: {}'.format(msg.topic))
    # print('message: {}'.format(str(msg.payload)))

    if msg.topic == COLOR_BLOCK_TOPIC_ID:
        message = msg.payload.decode('utf-8')
        print('color_block_info: {}'.format(message))
        update_object_tracker(message)

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

# 阻塞式， 循环往复，一直处理网络数据，断开重连
client.loop_forever()