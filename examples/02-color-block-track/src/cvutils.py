import numpy as np
import cv2
import sys

# https://docs.opencv.org/3.3.1/dc/df6/tutorial_py_histogram_backprojection.html

def select_roi(target):
    # 创建一个窗口
    cv2.namedWindow("image", flags= cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    cv2.imshow("image", target)
    # 是否显示网格 
    showCrosshair = True

    # 如果为Ture的话 , 则鼠标的其实位置就作为了roi的中心
    # False: 从左上角到右下角选中区域
    fromCenter = False
    # Select ROI
    rect = cv2.selectROI("image", target, showCrosshair, fromCenter)

    print("选中矩形区域")
    (x, y, w, h) = rect

    # Crop image
    roi = target[y : y+h, x:x+w]
    
    return rect, roi

def calculate_roi_hist(roi):
    hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    
    # calculating object histogram
    roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
    # normalize histogram and apply backprojection
    cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)

    return roihist

def backprojection(target, roihist):
    '''图像预处理'''
    hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)
    # Now convolute with circular disc
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    cv2.filter2D(dst,-1,disc,dst)
    # threshold and binary AND
    ret,binary = cv2.threshold(dst,80,255,0)
    # 创建 核
    kernel = np.ones((5,5), np.uint8)
    iter_time = 1
    # 闭运算
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel,iterations=iter_time)

    thresh = cv2.merge((binary,binary,binary))
    target_filter = cv2.bitwise_and(target,thresh)
    
    return binary, target_filter

def color_block_finder(img_bin, min_w=0, max_w=None, min_h=0, max_h=None):
    '''
    色块识别 返回矩形信息
    '''

    # 寻找轮廓（只寻找最外侧的色块）
    bimg, contours, hier = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 外接矩形区域集合
    rects = []

    if max_w is None:
        # 如果最大宽度没有设定，就设定为图像的宽度
        max_w = img_bin.shape[1]
    if max_h is None:
        # 如果最大高度没有设定，就设定为图像的高度
        max_h = img_bin.shape[0]
        
    # 遍历所有的边缘轮廓集合
    for cidx,cnt in enumerate(contours):
        # 获取联通域的外界矩形
        (x, y, w, h) = cv2.boundingRect(cnt)

        if w >= min_w and w <= max_w and h >= min_h and h <= max_h:
            # 将矩形的信息(tuple)添加到rects中
            rects.append((x, y, w, h))
    return rects

def draw_color_block_rect(img, rects,color=(0, 0, 255)):
    '''
    绘制色块的矩形区域
    '''
    # 声明画布(canvas) 拷贝自img
    canvas = np.copy(img)
    # 遍历矩形区域
    for rect in rects:
        (x, y, w, h) = rect
        # 在画布上绘制矩形区域（红框）
        cv2.rectangle(canvas, pt1=(x, y), pt2=(x+w, y+h),color=color, thickness=3)
    
    return canvas

if __name__ == '__main__':
    # 文件路径
    # img_path = 'blue-color-block.png'
    img_path = sys.argv[1]
    # 读入图片
    target = cv2.imread(img_path)

    select_roi(target)
    binary, target_filtered = image_process(target)

    thresh = cv2.merge((binary,binary,binary))
    res = np.vstack((target,thresh, target_filtered))
    cv2.imwrite('res.jpg',res)
