import cv2
import time
import numpy as np
from math import cos, pi, sin

# handshare_data = {
#         "t": 1,                                    
#         "device": "nju_iot",                 
#         "key": "c5cab3c5ebb04116accac802545005d0",
#         "ver": "v1.0"} 

class ImgRecgnition:
    c_x = 0
    c_y = 0
    c_r = 0
    rad = 0
    meter = 0
    # __clientSocket = socket(AF_INET, SOCK_STREAM) 
    # __host = "117.78.1.201"
    # __port = 8700           
    # __meter_list = ["meter_01","meter_02","meter_03"]
    def __init__(self):
        super().__init__()
        # try:
        #     self.__clientSocket.connect((self.__host,self.__port))                                
        #     self.__clientSocket.send(json.dumps(handshare_data).encode())           
        #     resMsg = self.__clientSocket.recv(1024).decode()   
        # except Exception as e:
        #     print(e)
            
        # tcpListen = Thread(target = self.__TCP_Listen) 
        # tcpListen.start()
        # tcpHeartbeat = Thread(target = self.__TCP_Ping)       
        # tcpHeartbeat.start()
        
    # def __TCP_Listen(self):
    #     while True:
    #         try:
    #             res = self.__clientSocket.recv(1024).decode() 
    #             if not res:
    #                 exit()
    #         except Exception as e:
    #             print(e)
    #             exit()

    # def __TCP_Ping(self):
    #     while True:
    #         try:
    #             self.__clientSocket.send("$#AT#".encode())   
    #             time.sleep(30)
    #         except Exception as e:
    #             print(e)
    #             exit()
    
    def img_init(self,filename):
        image = cv2.imread(filename)
        self.image = cv2.resize(image, (640,480))
        # self.meter_name = self.__meter_list[meter_No]

    def __get_rad(self,img_binary):
# input image: img, circle paras: c_x,c_y,c_r
        src = img_binary.copy()
        
        freq_list = []
        for i in range(160,360):
            x = self.c_r * cos(i * pi / 180) + self.c_x
            y = self.c_r * sin(i * pi / 180) + self.c_y
            temp = np.ones(src.shape, dtype="uint8")
            temp = temp *255
            cv2.line(temp, (self.c_x, self.c_y), (int(x), int(y)), (0, 0, 0), thickness=3)
            src1 = src.copy()
            c = cv2.bitwise_or(temp, src1)
            points = c[c == 0]
            freq_list.append((len(points), i))
        #print('Result:',max(freq_list, key=lambda x: x[0]),'rad')
        return max(freq_list, key=lambda x: x[0])

    def  __img_process(self):
        img = self.image.copy()
        dst = cv2.pyrMeanShiftFiltering(img, 10, 100)
        cimage = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        try:
            circles = cv2.HoughCircles(cimage, cv2.HOUGH_GRADIENT, 1, 80, param1=100, param2=30, minRadius=80, maxRadius=0)
            self.c_x, self.c_y, self.c_r = circles[0][0]
            self.c_r = self.c_r*0.8
            circle = np.ones(img.shape, dtype="uint8")
            circle = circle * 255
            cv2.circle(circle, (self.c_x, self.c_y), int(self.c_r), 0, -1)
            mask = cv2.bitwise_or(img, circle) 
            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            mask_binary = cv2.adaptiveThreshold(mask_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            #print(self.c_x,self.c_y,self.c_r)
            Rad = self.__get_rad(mask_binary)
            self.rad = Rad[1]
            #print(self.rad)
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
        result = cv2.circle(result,(c_x,c_y),int(c_r/0.8),(0,255,0),2)
        result = cv2.resize(result, (1280,960))
        cv2.imshow('result', result)
        cv2.waitKey(100)
        return
    
    # def send_meter(self):
    #     data = {
    #     "t": 3,
    #     "datatype" : 1,
    #     "datas": {
    #         self.meter_name : self.meter,
    #     },
    #     "msgid": str(random.randint(100,100000))  
    #     }
    #     try:
    #         self.__clientSocket.send(json.dumps(data).encode()) 
    #         print("send:",self.meter_name,self.meter)
    #     except Exception as e:
    #         print(e)
    #         return False


if __name__=="__main__":
    # This is an example

    test = img_recgnition()
    cap = cv2.VideoCapture(1)
    while(1):
        ret,img = cap.read()
        if not ret:
            print("fail")
        cv2.imwrite('1.png',img,[int(cv2.IMWRITE_PNG_COMPRESSION)])
        test.img_init("1.png")
        meter = test.get_meter()  #necessary!!!
        result = test.get_pic_processed()
        print(meter)
        cv2.imshow('result', result)
        cv2.waitKey(1000)
        cv2.destroyWindow('result')

