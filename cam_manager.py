import os
import sys
import struct
from socket import *
from threading import Thread

import cv2


class CamManager:

    camList = []
    instanceList = []

    def __init__(self, camList):
        super().__init__()
        self.camList = camList
        for camAddr in camList:
            instance = CamServer(camAddr)
            self.instanceList.append(instance)

    def request_all(self):
        picList = []
        for instance in self.instanceList:
            picList.append(instance.request_pic())
        return picList


class CamServer:

    camPort = 11451
    clientSocket = socket(AF_INET, SOCK_STREAM)

    def __init__(self, camAddr):
        super().__init__()
        self.camAddr = camAddr

    def request_pic(self):
        self.clientSocket.connect((self.camAddr, self.camPort))
        filename = self.__data_recv()
        self.clientSocket.close()
        return filename

    def __data_recv(self):
        fileinfo_size = struct.calcsize('128sl')
        buf = self.clientSocket.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.decode().strip('\00')
            filepath = os.path.join('./', self.camAddr + '_' + fn)
            # print('file new name is {0}, filesize if {1}'.format(filepath, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(filepath, 'wb')
            # print('start receiving...')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = self.clientSocket.recv(1024)
                    recvd_size += len(data)
                else:
                    data = self.clientSocket.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print ('end receive...')
        return filepath


if __name__ == '__main__':
    camManager = CamManager(['127.0.0.1'])
    picList = camManager.request_all()