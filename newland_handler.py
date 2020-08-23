# -*- coding:utf-8 -*-
# @ProjectName  :IoTCreepers
# @FileName     :newland_handler.py
# @Time         :20-7-19
# @Author       :Minaduki

import json
import time
import random
from socket import *
from threading import Thread

from cos import myupload
from cam_manager import *

handshare_data = {
        "t": 1,                                    #固定数据代表连接请求
        "device": "Player",                       #设备标识
        "key": "84d1a6f1fec04f12b60cfb9b83b297e4", #传输密钥
        "ver": "v1.0"}                             #客户端代码版本号,可以是自己拟定的一组客户端代码版本号值


class NewLandHandler:

    __clientSocket = socket(AF_INET, SOCK_STREAM) #创建socket
    __host = "117.78.1.201" #AIOT云平台tcp连接host地址
    __port = 8700           #AIOT云平台tcp连接port

    def __init__(self, handshare_data, get_pic):
        super().__init__()
        try:
            self.get_pic = get_pic
            self.__clientSocket.connect((self.__host,self.__port))                                #建立tcp连接
            self.__clientSocket.send(json.dumps(handshare_data).encode())           #发送云平台连接请求
            resMsg = self.__clientSocket.recv(1024).decode()   
        except Exception as e:
            print(e)
        
        tcpListen = Thread(target = self.__listen_server)  #监听服务端发送数据
        tcpListen.start()
        tcpHeartbeat = Thread(target = self.__tcp_ping)       #创建与云平台保持心跳的线程
        tcpHeartbeat.start()

    def __listen_server(self):
        '''
        监听TCP连接服务端消息
        '''
        while True:
            try:
                res = self.__clientSocket.recv(1024).decode() #接收服务端数据
                if not res:
                    exit()
                if res != '$OK##\r':
                    command = json.loads(res)
                    if command['t'] == 5:
                        self.__upload_pic(command)
                if 0:
                    exit()
            except Exception as e:
                print(e)
                exit()

    def __tcp_ping(self):
        '''
        TCP连接心跳包
        '''
        while True:
            try:
                self.__clientSocket.send("$#AT#".encode())   #发送心跳包数据
                time.sleep(30)
            except Exception as e:
                print(e)
                exit()

    def __upload_pic(self, command):
        try:
            #pic = brokerObj.get_pic()
            pic = self.get_pic()
            myupload(pic)
            status = 0
        except Exception as e:
            print(e)
            status = 1	# 1 for failed, 0 for success
        # print(command['cmdid'])
        reply = command
        reply['t'] = 6
        reply['status'] = status
        reply['data'] = 'https://newlandiot-1300406808.cos.ap-shanghai.myqcloud.com/' + pic
        try:
            self.__clientSocket.send(json.dumps(reply).encode())       #发送数据
        except Exception as e:
            print(e)

    def update_value(self, meter, value):
        data = {
            "t": 3,
            "datatype" : 1,
            "datas": {
                meter: value,
            },
            "msgid": str(random.randint(100,100000))
        }
        try:
            self.__clientSocket.send(json.dumps(data).encode())
        except Exception as e:
            print(e)
            return False


def get_pic_test():
    return camManager.request_all()[0]


if __name__ == "__main__":
    '''
    Test code
    '''
    camManager = CamManager(['127.0.0.1'])
    newLandd = NewLandHandler(handshare_data, get_pic_test)
    newLandd.update_value('127.0.0.1', 10086)