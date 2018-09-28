# -*- coding: utf-8 -*- 
'''
测试图像二值化
'''
import cv2
from color_feature import *
import time
def init_video_capture(phone_ip):
    '''初始化手机WIFI摄像头'''
    global video_cap    
    # 摄像头的IP地址  
    # http://用户名：密码@IP地址：端口/
    ip_camera_url = 'http://admin:admin@{}:8081/'.format(phone_ip)
    # 创建一个VideoCapture
    video_cap = cv2.VideoCapture(ip_camera_url)
    # 设置缓存区的大小
    video_cap.set(cv2.CAP_PROP_BUFFERSIZE,1)

video_cap = None
phone_ip = '192.168.43.1'
init_video_capture(phone_ip)


cv2.namedWindow('result', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
cv2.namedWindow('binary', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)


ref_lowerb = (101, 111, 0)
ref_upperb = (140, 255, 255)

lowerb = (0, 0, 0)
upperb = (255, 255, 255)
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


while True:
    ret,img = video_cap.read()

    if not ret:
        print('WIFI Camera Not Detected')
        time.sleep(1)
        continue
    
    img_bin, rects = color_block_finder(img, lowerb=lowerb, upperb=upperb, min_h=5, min_w=5)

    cv2.imshow('result', img)
    cv2.imshow('binary', img_bin)
    cv2.imwrite('sreenshot.png', img)
    # 这里做一下适当的延迟，每帧延时0.05s钟
    if cv2.waitKey(10) & 0xFF == ord('q'):
        # 断开MQTT连接
        break