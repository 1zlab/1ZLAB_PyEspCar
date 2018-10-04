import time
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from cvutils import *
from wifi_camera import IPCameraAPP

# 创建一个IP摄像头对象
phone_ip = '192.168.43.1'
ip_cam = IPCameraAPP(phone_ip)

# 获取第一张图像
first_img = ip_cam.read()
# 选择ROI区域
rect, roi = select_roi(first_img)
roi_hist = calculate_roi_hist(roi)

cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
cv2.namedWindow('bk_proj', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
cv2.namedWindow('binary', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)


def get_posi_offset(img, rect):
    '''获取色块距离画面中心的偏移量'''

    img_height, img_width, _ = img.shape
    (x, y, w, h) = rect
    x_offset = (x + w/2) / img_width - 0.5
    y_offset = (y + h/2) / img_height - 0.5


    return (x_offset, y_offset)

def get_area_offset(img, rect, ref_area=0.2):
    '''获取色块面积的偏移量'''
    img_height, img_width, _ = img.shape
    x,y,w,h = rect

    area_offset = (w * h) / (img_height * img_width) - ref_area

    return area_offset

mqtt_broker_ip = 'localhost'
mqtt_broker_port = 1883
mqtt_client = mqtt.Client()
TOPIC_ID = 'color_block_info'
# mqtt_client.on_message = on_message
result = mqtt_client.connect(mqtt_broker_ip, mqtt_broker_port, 60)
if result != 0:
    print('[ERROR] could not connect to MQTT Broker,please check ip and port')
    exit(-1)
else:
    print('[INFO] connect to the MQTT Broker')


while True:
    img = ip_cam.read()
    binary, bk_proj = backprojection(img, roi_hist)
    
    # 毫秒级时间戳
    timestamp = int(round(time.time()*1000))
    rects = color_block_finder(binary, min_h=20, min_w=20)
    
    canvas = None
    if len(rects) > 0:    
        rect = max(rects, key=lambda rect: rect[2]*rect[3])
        canvas = draw_color_block_rect(img, [rect])
        x_offset, y_offset = get_posi_offset(img, rect)
        area_offset = get_area_offset(img, rect)
        message = '{0},{1},{2:.2f},{3:.2f},{4:.2f}'.format(timestamp, True, x_offset, y_offset, area_offset)
        mqtt_client.publish(TOPIC_ID, message)
        print('[INFO] send message: \n{}'.format(message))
    else:
        canvas = img
        message = '{0},{1},{2},{3},{4}'.format(timestamp,False, 0, 0, 0)
        mqtt_client.publish(TOPIC_ID, message)
        print('[INFO] send message: \n{}'.format(message))

    cv2.imshow('image', canvas)
    cv2.imshow('bk_proj', bk_proj)
    cv2.imshow('binary', binary)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Quit')
        break