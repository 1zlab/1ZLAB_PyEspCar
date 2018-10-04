'''
获取图像并广播当前色块的位置
'''
import cv2
import time
import numpy as np
import paho.mqtt.client as mqtt
from color_feature import *

# 更新阈值
def updateThreshold(x):

    global lowerb
    global upperb

    minH = cv2.getTrackbarPos('minH','binary')
    maxH = cv2.getTrackbarPos('maxH','binary')
    minS = cv2.getTrackbarPos('minS','binary')
    maxS = cv2.getTrackbarPos('maxS', 'binary')
    minV = cv2.getTrackbarPos('minV', 'binary')
    maxV = cv2.getTrackbarPos('maxV', 'binary')
    
    lowerb = np.int32([minH, minS, minV])
    upperb = np.int32([maxH, maxS, maxV])
    
    print('更新阈值')
    print(lowerb)
    print(upperb)

def init_video_capture(phone_ip):
    '''初始化手机WIFI摄像头'''
    global video_cap    
    # 摄像头的IP地址  
    # http://用户名：密码@IP地址：端口/
    ip_camera_url = 'http://admin:admin@{}:8081/'.format(phone_ip)
    print('[INFO] initialization wifi camera:\n{}'.format(ip_camera_url))
    # 创建一个VideoCapture
    video_cap = cv2.VideoCapture(ip_camera_url)
    # 设置缓存区的大小
    video_cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
    
    print('[INFO] jump some frame of wifi camera,please wait')
    # 清空wifi摄像头的缓存
    # 跳过的帧数
    ignore_cnt = 100
    # 过滤帧
    for i in range(ignore_cnt):
        ret, img = video_cap.read()



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

video_cap = None
phone_ip = '192.168.43.1'
init_video_capture(phone_ip)

cv2.namedWindow('result', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
cv2.namedWindow('binary', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)


# 参考颜色阈值 红色
ref_lowerb = (144, 109, 27)
ref_upperb = (184, 211, 206)
# ref_lowerb = (0, 98, 76)
# ref_upperb = (6, 213, 255)

# 参考颜色阈值 淡青色
# ref_lowerb = (44, 0, 36)
# ref_upperb = (110, 79, 190)
# 参考颜色阈值 嫩绿色
# ref_lowerb = (30, 170, 131)
# ref_upperb = (144, 200, 194)

# # 参考颜色阈值 黑色
# ref_lowerb = (100, 0, 0)
# ref_upperb = (110, 255, 255)



lowerb = (0, 0, 0)
upperb = (255, 255, 255)


cv2.createTrackbar('minH','binary',0,255,updateThreshold)
cv2.createTrackbar('maxH','binary',0,255,updateThreshold)
cv2.createTrackbar('minS','binary',0,255,updateThreshold)
cv2.createTrackbar('maxS','binary',0,255,updateThreshold)
cv2.createTrackbar('minV','binary',0,255,updateThreshold)
cv2.createTrackbar('maxV','binary',0,255,updateThreshold)

time.sleep(0.5)

cv2.setTrackbarPos('maxH', 'binary', ref_upperb[0])
cv2.setTrackbarPos('minH', 'binary', ref_lowerb[0])
cv2.setTrackbarPos('maxS', 'binary', ref_upperb[1])
cv2.setTrackbarPos('minS', 'binary', ref_lowerb[1])
cv2.setTrackbarPos('maxV', 'binary', ref_upperb[2])
cv2.setTrackbarPos('minV', 'binary', ref_lowerb[2])

updateThreshold(None)


while True:
    ret,img = video_cap.read()
    if ret:
        img_bin, rects = color_block_finder(img, lowerb=lowerb, upperb=upperb, min_h=20, min_w=20)
        
        # 毫秒级时间戳
        timestamp = int(round(time.time()*1000))

        if len(rects) > 0:    
            rect = max(rects, key=lambda rect: rect[2]*rect[3])
            canvas = draw_color_block_rect(img, [rect])
            x_offset, y_offset = get_posi_offset(img, rect)
            area_offset = get_area_offset(img, rect)
            message = '{0},{1},{2:.2f},{3:.2f},{4:.2f}'.format(timestamp, True, x_offset, y_offset, area_offset)
            mqtt_client.publish(TOPIC_ID, message)
        else:
            canvas = img
            message = '{0},{1},{2},{3},{4}'.format(timestamp,False, 0, 0, 0)
            mqtt_client.publish(TOPIC_ID, message)
            
        
        cv2.imshow('result', canvas)
        cv2.imshow('binary', img_bin)
    else:
        print('[ERROR] failed to get image')
        exit(-1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Quit')
        break

cv2.destroyAllWindows()
