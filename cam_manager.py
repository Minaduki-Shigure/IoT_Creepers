import os
import sys
import struct
from socket import *
from threading import Thread

import cv2


class CamManager:

    __camList = []
    __instanceList = []

    def __init__(self, camList):
        super().__init__()
        self.__camList = camList
        for camAddr in self.__camList:
            instance = CamServer(camAddr)
            self.__instanceList.append(instance)

    def request_all(self):
        picList = []
        for instance in self.__instanceList:
            picList.append(instance.request_pic())
        return picList


class CamServer:

    __camPort = 11451
    # __clientSocket = socket(AF_INET, SOCK_STREAM)
    # Socket一旦关闭之后是不能复用的，即使client这边重新connect了，
    # 但是根据我的推测server会把这个socket认为是上一个已经关掉的，
    # 从而不会accept，因此还是不行。

    def __init__(self, camAddr):
        super().__init__()
        self.__camAddr = camAddr

    def request_pic(self):
        self.__clientSocket = socket(AF_INET, SOCK_STREAM)
        self.__clientSocket.connect((self.__camAddr, self.__camPort))
        filename = self.__data_recv()
        self.__clientSocket.close()
        return filename

    def __data_recv(self):
        fileinfo_size = struct.calcsize('128sl')
        buf = self.__clientSocket.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.decode().strip('\00')
            fn = self.__camAddr + '_' + fn
            filepath = os.path.join('./', fn)
            # print('file new name is {0}, filesize if {1}'.format(filepath, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(filepath, 'wb')
            # print('start receiving...')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = self.__clientSocket.recv(1024)
                    recvd_size += len(data)
                else:
                    data = self.__clientSocket.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            # print ('end receive...')
        return fn


if __name__ == '__main__':
    camManager = CamManager(['127.0.0.1'])
    picList = camManager.request_all()
    print(picList)
    print(camManager.request_all())
    # print(picList)