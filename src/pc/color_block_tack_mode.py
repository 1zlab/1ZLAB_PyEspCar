'''

状态机
1 -> 2 -> 3 -> 4

* 1 舵机比例控制
* 2 电机底盘旋转 + 舵机比例控制（电机旋转是干扰）， 直到底部舵机的角度是135度正方向
* 3 电机走直线，前进/后退， 此时
* 4 停止， 如果offset大于开启阈值，则进入步骤1

TODO 改成动态的 差速运动
TODO 有条件的复位，阻止往复舵机摆动
'''
import cv2
import time
import paho.mqtt.client as mqtt
from color_feature import *
from pyespcar_sdk import PyCarSDK
from pid import PositionPID
import threading

cur_status = 0


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

    # 清空wifi摄像头的缓存
    for i in range(100):
        ret, frame = video_cap.read()


def get_posi_offset(img, rect):
    '''获取色块距离画面中心的偏移量'''
    global posi_min_threshold

    img_height, img_width, _ = img.shape
    (x, y, w, h) = rect
    x_offset = (x + w/2) / img_width - 0.5
    y_offset = (y + h/2) / img_height - 0.5

    if abs(x_offset) <= posi_min_threshold:
        x_offset = 0
    if abs(y_offset) <= posi_min_threshold:
        y_offset = 0

    return (x_offset, y_offset)

def get_area_offset(img, rect, ref_area=0.2):
    '''获取色块面积的偏移量'''
    global area_min_threshold
    img_height, img_width, _ = img.shape
    x,y,w,h = rect

    area_offset = (w * h) / (img_height * img_width) - ref_area

    if abs(area_offset) < area_min_threshold:
        area_offset = 0
    return area_offset


cur_top_servo_angle = 90
cur_bottom_servo_angle = 135

def cp_bottom_servo_control(x_offset, kp=-5, max_delta_angle=2):
    '''底部舵机的PID控制'''
    global sdk
    global cur_bottom_servo_angle

    # 获得底部舵机角度增量
    delta_btm_angle = x_offset * kp
    # 判断增幅有没有越界
    if abs(delta_btm_angle) > max_delta_angle:
        delta_btm_angle = max_delta_angle if delta_btm_angle > 0 else -max_delta_angle
    # 计算下一个时刻的角度
    next_bottom_servo_angle =  delta_btm_angle + cur_bottom_servo_angle
    # 判断范围是否合法
    if next_bottom_servo_angle < 0:
        next_bottom_servo_angle = 0
    elif next_bottom_servo_angle > 270:
        next_bottom_servo_angle = 270
    
    # 重新矫正增量
    delta_btm_angle = next_bottom_servo_angle - cur_bottom_servo_angle
    
    # 舵机动作
    sdk.set_bottom_servo_angle(next_bottom_servo_angle)
    # 更新当前底部舵机的角度
    cur_bottom_servo_angle = next_bottom_servo_angle

def cp_top_servo_control(y_offset, kp=-5, max_delta_angle=2):
    '''顶部舵机的PID控制'''
    global sdk
    global cur_top_servo_angle

    # 获得顶部舵机角度增量
    delta_top_angle = y_offset * kp
    # 判断增幅有没有越界
    if abs(delta_top_angle) > max_delta_angle:
        delta_top_angle = max_delta_angle if delta_top_angle > 0 else -max_delta_angle
    # 计算下一个时刻的角度
    next_top_servo_angle =  delta_top_angle + cur_top_servo_angle
    # 判断范围是否合法 
    # 0-180 约束为 30-150
    if next_top_servo_angle < 30:
        next_top_servo_angle = 30
    elif next_top_servo_angle > 150:
        next_top_servo_angle = 150
        
    # 舵机动作
    sdk.set_top_servo_angle(next_top_servo_angle)
    # 更新当前顶部部舵机的角度
    cur_top_servo_angle = next_top_servo_angle


def stat0_stop(x_offset, y_offset, area_offset):
    '''小车停止状态'''
    global cur_status
    global sdk
    global posi_min_threshold

    # 小车停止
    sdk.stop()
    print('STEP1-------<<<<<<<<<<<<')
    # time.sleep(2)

    if abs(x_offset) > posi_min_threshold or abs(y_offset) > posi_min_threshold:
        print('STEP2-------<<<<<<<<<<<<')
        # time.sleep(2)
        # 如果色块中心在画面存在偏移
        cur_status = 1

def stat1_cp_ctl(x_offset, y_offset, area_offset):
    '''舵机角度控制'''
    global cur_status
    global sdk
    global posi_min_threshold
    

    if abs(x_offset) < posi_min_threshold and abs(y_offset) < posi_min_threshold:
        # 目前色块在画面正中心, 接下来电机转动，旋转小车
        cur_status = 2
    else:
        # 舵机云台PID控制
        cp_bottom_servo_control(x_offset, kp=-5, max_delta_angle=5)
        cp_top_servo_control(y_offset, kp=-5, max_delta_angle=5)



# car_turn_pid = PositionPID(kp=-100, ki=-10, kd=0, target=0, max_bias_sum=None, max_bias_win=10)
# def car_turn_pid_control(angle_offset, kp=-30, max_speed_percent=60):
#     # 舵机转向的PID控制
#     global car_turn_pid

#     if angle_offset < 0:
#         speed_percent = kp * angle_offset/135 + 35
#     else:
#         speed_percent = kp * angle_offset/135 - 35
    
#     if abs(speed_percent) > max_speed_percent:
#         speed_percent = max_speed_percent if speed_percent > 0 else -max_speed_percent
    
#     if speed_percent > 0:
#         sdk.turn_right(speed_percent=abs(speed_percent))
#     else:
#         sdk.turn_left(speed_percent=abs(speed_percent))

state = False

def toggle_state():
    global state
    state = not state

def stat2_car_turn(x_offset, y_offset, area_offset):
    '''
    小车转向, 舵机反向转动
    '''
    global cur_status
    global sdk
    global cur_bottom_servo_angle
    global video_cap
    global posi_min_threshold
    global state
    # 计算角度偏移量
    angle_offset = cur_bottom_servo_angle - 135
    
    # 偏角在大于30左右的时候，延时与转角之间类似线性关系
    if abs(angle_offset) < 30:
        print('[STAT3] Sangle_offset: {}  less than {}'.format(angle_offset, 30))
        cur_status = 3
        return
    else:
        # 计算得到延时时间， 根据当前电压可以调节这个比例系数
        delay_ms = abs(angle_offset) * 2
        # 速度开启满速
        speed_percent = 100
        
        # 舵机复位
        sdk.set_bottom_servo_angle(135)
        cur_bottom_servo_angle = 135

        # 向目标方向旋转
        if angle_offset > 0:
            print('Rotate Left')
            sdk.turn_left(speed_percent=speed_percent, delay_ms=delay_ms)
        elif angle_offset < 0:
            print('Rotate Right')
            sdk.turn_right(speed_percent=speed_percent, delay_ms=delay_ms)

        
        print('delay_ms: {}'.format(delay_ms))
        print('start refresh frame')
        
        cv2.waitKey(int(delay_ms))
        # # 在舵机转向的同时，video_capture也在刷新
        # state=False
        # timer = threading.Timer(delay_ms/1000*1.5, toggle_state)
        # while True:
        #     if state:
        #         break
        #     # 不断刷新video capture
        #     ret,img = video_cap.read()

        print('end refresh frame')    
        # 进入下一个状态
        cur_status = 3
        
    # print('Angle Offset {}')
    # # 舵机复位
    # sdk.set_bottom_servo_angle(135)
    # cur_bottom_servo_angle = 135
    
    # # 需要延时一段时间，让舵机云台复位（更新image）
    # for i in range(10):
    #     ret, img = video_cap.read()
    
    # while True:
    #     ret,img = video_cap.read()
    #     img_bin, rects = color_block_finder(img, lowerb=ref_lowerb, upperb=ref_upperb, min_h=5, min_w=5)

        
    #     if len(rects) > 0:
    #         rect = max(rects, key=lambda rect: rect[2]*rect[3])
    #         canvas = draw_color_block_rect(img, [rect])
    #         x_offset, y_offset = get_posi_offset(img, rect)
            
    #         if abs(x_offset) < 0.1:
    #             print('Rotate End')
    #             sdk.stop()
    #             cur_status = 3
    #             break
    #     else:
    #         canvas = img
            
        
    #     cv2.imshow('result', canvas)
    #     cv2.imshow('binary', img_bin)
        
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    #     # 向目标方向旋转
    #     if angle_offset > 0:
    #         print('Rotate Left')
    #         sdk.turn_left(speed_percent=55)
    #     elif angle_offset < 0:
    #         print('Rotate Right')
    #         sdk.turn_right(speed_percent=55)    

def stat3_go(x_offset, y_offset, area_offset):
    '''
    小车走直线（前进或后退）
    '''
    global sdk
    global posi_min_threshold
    global cur_status
    # cp_top_servo_control(y_offset, kp=-5, max_delta_angle=5)
    # cp_bottom_servo_control(x_offset, kp=-5, max_delta_angle=5)
    if abs(x_offset) > 3*posi_min_threshold or abs(y_offset) > 3*posi_min_threshold:
        sdk.stop()
        cur_status = 1
        print('STAT3 ==> STAT1')
        return

    print('[STAT3] area_offset = {}'.format(area_offset))
    if area_offset > 0.1:
        print('[STAT3] Go Backward')
        sdk.go_backward(speed_percent=55)
    elif area_offset < -0.1:
        print('[STAT3] Go Forward')
        sdk.go_forward(speed_percent=55)
    else:
        cur_status = 0


mqtt_client = mqtt.Client()
# mqtt_client.on_message = on_message
mqtt_client.connect('localhost', 1883, 60)
sdk = PyCarSDK(mqtt_client, is_debug=True)

sdk.cp_reset()
sdk.turn_left(speed_percent=0)

# TODO 调整这个阈值
# 舵机可以很准确
posi_min_threshold = 0.05
area_min_threshold = 0.1

STATS_LIST = [stat0_stop, stat1_cp_ctl, stat2_car_turn, stat3_go] 
cur_status = 0


video_cap = None
phone_ip = '192.168.43.1'
init_video_capture(phone_ip)

cv2.namedWindow('result', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
cv2.namedWindow('binary', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)



ignore_cnt = 100
ref_lowerb = (144, 109, 27)
ref_upperb = (184, 211, 206)

# ref_lowerb = (101, 111, 0)
# ref_upperb = (140, 255, 255)

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

updateThreshold(None)

# 过滤帧
for i in range(ignore_cnt):
    ret, img = video_cap.read()


while True:
    ret,img = video_cap.read()
    if ret:
        img_bin, rects = color_block_finder(img, lowerb=lowerb, upperb=upperb, min_h=20, min_w=20)
        if len(rects) >= 1:
            rect = max(rects, key=lambda rect: rect[2]*rect[3])
            x_offset, y_offset = get_posi_offset(img, rect)
            area_offset = get_area_offset(img, rect)

            print('OFFSET \n X: {} , Y: {}'.format(x_offset, y_offset))
            print('Area Offset: {}'.format(area_offset))
            print('Status: {}'.format(cur_status))
            print('Bottom Servo: {}'.format(cur_bottom_servo_angle))
            print('Top Servo: {}'.format(cur_top_servo_angle))

            STATS_LIST[cur_status](x_offset, y_offset, area_offset)

            # cp_pid_control(x_offset, y_offset)
            canvas = draw_color_block_rect(img, [rect])
        else:
            # # 进入周边搜寻模式
            # cur_status = 2
            # # sdk.cp_reset()
            # sdk.set_bottom_servo_angle(140)
            # # 舵机复位进入特定的角度
            # sdk.set_top_servo_angle(70)
            # cur_bottom_servo_angle = 135
            # cur_top_servo_angle = 70

            canvas = img
            # sdk.cp_reset()
            # sdk.stop()
            # time.sleep(1)

        cv2.imshow('result', canvas)
        cv2.imshow('binary', img_bin)
        cv2.imwrite('sreenshot.png', canvas)
        # 这里做一下适当的延迟，每帧延时0.05s钟
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sdk.stop()
            sdk.cp_reset()
            # 断开MQTT连接
            sdk.mqtt_client.disconnect()
            break

cv2.destroyAllWindows()