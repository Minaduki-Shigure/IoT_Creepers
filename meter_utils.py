# @Time         :20-07-17
# @Author       :WJZ
# @Team         :IoT_Creepers
# @Version      :v1.3

import cv2
import numpy as np
from math import cos, pi, sin


def get_rad(img,c_x,c_y,c_r):
# input image: img, circle paras: c_x,c_y,c_r
    src = img.copy()
    freq_list = []
    for i in range(361):
        x = c_r * cos(i * pi / 180) + c_x
        y = c_r * sin(i * pi / 180) + c_y
        temp = np.ones(img.shape, dtype="uint8")
        temp = temp *255
        cv2.line(temp, (c_x, c_y), (int(x), int(y)), (0, 0, 0), thickness=3)
        src1 = src.copy()
        c = cv2.bitwise_or(temp, src1)
        points = c[c == 0]
        freq_list.append((len(points), i))
    print('Result:',max(freq_list, key=lambda x: x[0]),'rad')
    return max(freq_list, key=lambda x: x[0])

def rad2meter(rad):
    if rad<0 or rad>361:
        return False
    else:
        if rad < 90:
            meter = 1.35 + rad* 0.00611111
        elif rad > 138:
            meter = (rad-139) * 0.00611111
        else :
            meter = 0
    return round(meter,2)

def img_process(image):
    img = image.copy()
    img = cv2.resize(img, (640,480))
    dst = cv2.pyrMeanShiftFiltering(img, 10, 100)
    cimage = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    try:
        circles = cv2.HoughCircles(cimage, cv2.HOUGH_GRADIENT, 1, 80, param1=100, param2=30, minRadius=80, maxRadius=0)
        c_x, c_y, c_r = circles[0][0]
        circle = np.ones(img.shape, dtype="uint8")
        circle = circle * 255
        cv2.circle(circle, (c_x, c_y), int(c_r), 0, -1)
        mask = cv2.bitwise_or(img, circle) 
        mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask_binary = cv2.adaptiveThreshold(mask_gray,255,cv2.THRESH_BINARY,cv2.THRESH_BINARY,11,2)
        rad = get_rad(mask_binary,c_x,c_y,c_r)
        meter = rad2meter(rad[1])
        paras = {'c_x':c_x, 'c_y':c_y, 'c_r':c_r, 'rad':rad[1]}
        print("Get meter value successfully!")
        return meter,paras
    except Exception as e:
        print("img_process:  ",e) 
        return False, False

def get_image(type='CAMERA', file='img1.png'):
    if type=='CAMERA':
        cap = cv2.VideoCapture(0)
        success,img = cap.read()
        if not success:
            print("Fail to get image!")
            return False
        else:
            return img
    elif type=='FILE':
        try:
            img = cv2.imread(file)
            return img
        except Exception as e:
            print(e) 
            return False

def Recognition(type='CAMERA', file='img1.png'):
    try:
        img = get_image(type, file)
        meter, paras = img_process(img)
        return meter, paras, img
    except Exception as e:
        print(e)
        return False, False, False

def result_show(paras,img):
    c_x = paras['c_x']
    c_y = paras['c_y']
    c_r = paras['c_r']
    rad = paras['rad']
    x = c_r * cos(rad * pi / 180) + c_x
    y = c_r * sin(rad * pi / 180) + c_y
    result = cv2.line(img.copy(), (c_x, c_y), (int(x), int(y)), (0, 0, 255), thickness=3)
    cv2.imshow('result', result)
    cv2.waitKey(1000)
    cv2.destroyWindow('result')
