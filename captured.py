import os
import sys
import struct
import datetime
from socket import *
from threading import Thread

import cv2

serverPort = 11451
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
cap.set(cv2.CAP_PROP_FPS, 1)

frame = []


def socket_server():
	# print('socket_server')
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', serverPort))	
	serverSocket.listen(10)

	captured = Thread(target = capture_daemon)
	captured.start()

	while True:
		connSocket, addr = serverSocket.accept()
		newClient = Thread(target = capture_server, args = (connSocket, addr))
		newClient.start()


def capture_once(cap, filename):
	# print('capture_once')
	try:
		# success, frame = cap.read()
		cv2.imwrite(filename, frame)
	except Exception as e:
		print(e) # Logging


def send_picture(connSocket):
	# print('send_picture')
	filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.png'
	capture_once(cap, filename)

	fileinfo_size = struct.calcsize('=128sl')
    # 定义文件头信息，包含文件名和文件大小
	fhead = struct.pack('=128sl', bytes(os.path.basename(filename).encode('utf-8')), os.stat(filename).st_size)
	connSocket.send(fhead)
	# print(fhead)

	fp = open(filename, 'rb')
	while True:
		data = fp.read(1024)
		if not data:
			break
		connSocket.send(data)

	
def capture_server(connSocket, addr):
	# print('capture_daemon')
	try:
		send_picture(connSocket)
		connSocket.close()
		# print('closed')
	except Exception as e:
		print(e) # Logging


def capture_daemon():
	while True:
		global frame
		success, frame = cap.read()

if __name__ == '__main__':
	socket_server()