import os
import sys
import struct
from socket import *
from threading import Thread

import cv2

camList = ['127.0.0.1']
serverPort = 11451


def socket_client(serverIP):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverIP, serverPort))
    data_recv(clientSocket, serverIP)
    clientSocket.close()


def data_recv(connSocket, serverIP):
    fileinfo_size = struct.calcsize('128sl')
    buf = connSocket.recv(fileinfo_size)
    if buf:
        filename, filesize = struct.unpack('128sl', buf)
        fn = filename.decode().strip('\00')
        filepath = os.path.join('./', serverIP + '_' + fn)
        # print('file new name is {0}, filesize if {1}'.format(filepath, filesize))

        recvd_size = 0  # 定义已接收文件的大小
        fp = open(filepath, 'wb')
        # print('start receiving...')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = connSocket.recv(1024)
                recvd_size += len(data)
            else:
                data = connSocket.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        fp.close()
        print ('end receive...')
    connSocket.close()


def camera_manager_init():
    for server in camList:
        newConn = Thread(target = socket_client, args = (server,))
        newConn.start()


if __name__ == '__main__':
	camera_manager_init()