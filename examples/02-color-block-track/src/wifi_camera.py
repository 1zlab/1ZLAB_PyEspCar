'''
Wifi摄像头类
'''
import cv2

class IPCameraAPP:
    '''IP摄像头APP'''
    INIT_JUMP_FRAME_NUM = 50
    CAP_BUFFER_SIZE = 1
    def __init__(self, phone_ip):
        ip_camera_url = 'http://admin:admin@{}:8081/'.format(phone_ip)
        self.cap = cv2.VideoCapture(ip_camera_url)
        # 设置缓存区的大小
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, self.CAP_BUFFER_SIZE)

        for i in range(self.INIT_JUMP_FRAME_NUM):
            ret, img = self.cap.read()
    
    def read(self):
        ret, img = self.cap.read()
        if ret:
            return img
        else:
            print('[ERROR] failed to get image')
            exit(-1)