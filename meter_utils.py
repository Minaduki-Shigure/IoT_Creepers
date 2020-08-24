import cv2
import numpy as np
from math import cos, pi, sin

class ImgRecgnition:
    c_x = 0
    c_y = 0
    c_r = 0
    rad = 0
    meter = 0

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        image = cv2.imread(filename)
        self.image = cv2.resize(image, (480,640))


    def __get_rad(self,img_binary):
# input image: img, circle paras: c_x,c_y,c_r
        src = img_binary.copy()
        freq_list = []
        for i in range(361):
            x = self.c_r * cos(i * pi / 180) + self.c_x
            y = self.c_r * sin(i * pi / 180) + self.c_y
            temp = np.ones(src.shape, dtype="uint8")
            temp = temp *255
            cv2.line(temp, (self.c_x, self.c_y), (int(x), int(y)), (0, 0, 0), thickness=3)
            src1 = src.copy()
            c = cv2.bitwise_or(temp, src1)
            points = c[c == 0]
            freq_list.append((len(points), i))
        print('Result:',max(freq_list, key=lambda x: x[0]),'rad')
        return max(freq_list, key=lambda x: x[0])

    def  __img_process(self):
        print("start process")
        img = self.image.copy()
        dst = cv2.pyrMeanShiftFiltering(img, 10, 100)
        cimage = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        try:
            circles = cv2.HoughCircles(cimage, cv2.HOUGH_GRADIENT, 1, 80, param1=100, param2=30, minRadius=80, maxRadius=0)
            self.c_x, self.c_y, self.c_r = circles[0][0]
            circle = np.ones(img.shape, dtype="uint8")
            circle = circle * 255
            cv2.circle(circle, (self.c_x, self.c_y), int(self.c_r), 0, -1)
            mask = cv2.bitwise_or(img, circle) 
            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            mask_binary = cv2.adaptiveThreshold(mask_gray,255,cv2.THRESH_BINARY,cv2.THRESH_BINARY,11,2)
            print(self.c_x,self.c_y,self.c_r)
            Rad = self.__get_rad(mask_binary)
            self.rad = Rad[1]
            print(self.rad)
            self.meter = self.__rad2meter(self.rad)
            
        except Exception as e:
            print("img_process:  ",e) 
            return False, False   

    def __rad2meter(self,rad):
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

    def get_meter(self):
        self.__img_process()
        return self.meter
    
    def get_pic_processed(self):
        c_x = self.c_x
        c_y = self.c_y
        c_r = self.c_r
        rad = self.rad
        img = self.image
        x = c_r * cos(rad * pi / 180) + c_x
        y = c_r * sin(rad * pi / 180) + c_y
        result = cv2.line(img.copy(), (c_x, c_y), (int(x), int(y)), (0, 0, 255), thickness=3)
        result = cv2.circle(result,(c_x,c_y),c_r,(0,255,0),2)
        fn = 'r_' + self.filename
        cv2.imwrite(fn, result)
        return fn

if __name__=="__main__":
    # This is an example
    test = ImgRecgnition("img5.jpg")
    print(test.get_meter())
    result = test.get_pic_processed()
    cv2.imshow('result', result)
    cv2.waitKey(-1)
    cv2.destroyWindow('result')
