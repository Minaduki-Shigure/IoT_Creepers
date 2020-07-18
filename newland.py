# -*- coding:utf-8 -*-
# @ProjectName  :IoTCreepers
# @FileName     :newland.py
# @Time         :20-7-19
# @Author       :Minaduki

import socket
import json
import time
import random
from threading import Thread

from cos import myupload
from meter_utils import get_rad, get_img


host = "117.78.1.201" #AIOT云平台tcp连接host地址
port = 8700           #AIOT云平台tcp连接port

meters = ['meter_01', 'meter_02', 'meter_03']

def socket_client(host,port):
    ''''
    创建TCP连接
    '''
    handshare_data = {
            "t": 1,                                    #固定数据代表连接请求
            "device": "Player",                       #设备标识
            "key": "84d1a6f1fec04f12b60cfb9b83b297e4", #传输密钥
            "ver": "v1.0"}                             #客户端代码版本号,可以是自己拟定的一组客户端代码版本号值
    try:
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建socket
        tcp_client.connect((host,port))                                #建立tcp连接
        tcp_client.send(json.dumps(handshare_data).encode())           #发送云平台连接请求
        res_msg = tcp_client.recv(1024).decode()                       #接收云平台响应
    except Exception as e:
        print(e)
        return False
    return tcp_client                #返回socket对象


def upload_img(command):
    try:
        img = get_img()
        myupload(img)
        status = 0
    except Exception as e:
        print(e)
        status = 1	# 1 for failed, 0 for success
    # print(command['cmdid'])
    reply = command
    reply['t'] = 6
    reply['status'] = status
    reply['data'] = 'https://newlandiot-1300406808.cos.ap-shanghai.myqcloud.com/' + img
    try:
        tcp_client.send(json.dumps(reply).encode())       #发送数据
    except Exception as e:
        print(e)


def listen_server(socket_obj):
    '''
    监听TCP连接服务端消息
    :param socket_obj:
    :return:
    '''
    while True:
        try:
            res = socket_obj.recv(1024).decode() #接收服务端数据
            if not res:
                exit()
            if res != '$OK##\r':
                command = json.loads(res)
                upload_img(command)
            if 0:
                exit()
        except Exception as e:
            print(e)
            exit()


def tcp_ping(socket_obj):
    '''
    TCP连接心跳包
    :param socket_obj:
    :param obj:
    :return:
    '''
    while True:
        try:
            socket_obj.send("$#AT#".encode())   #发送心跳包数据
            time.sleep(30)
        except Exception as e:
            print(e)
            exit()


def send_meter_value(tcp_client, meter, value):
    data = {
        "t": 3,
        "datatype" : 1,
        "datas": {
            meter: value,
        },
        "msgid": str(random.randint(100,100000))
    }
    try:
        tcp_client.send(json.dumps(data).encode())
    except Exception as e:
        print(e)
        return False


def meter_recognize_daemon(tcp_client):
    while True:
	for meter in meters:
            val, paras, img = Recognition(meter, type='CAMERA')
            if not val:
                print("Fail to recognize the value of meter!")
                exit()
            send_meter_value(tcp_client, meter, value)
            time.sleep(0.2)
        # print("Send: ",meter_list[0], val)
        # result_show(paras, img)
        time.sleep(2.4)


if __name__ == "__main__":
    tcp_client = socket_client(host,port)                  #创建tcp　sockt 对象
    tcp_listen = Thread(target=listen_server, args=(tcp_client,))  #监听服务端发送数据
    tcp_listen.start()
    tcp_heartbeat = Thread(target=tcp_ping, args=(tcp_client,))       #创建与云平台保持心跳的线程
    tcp_heartbeat.start()
    recgnd = Thread(target=meter_recognize_daemon, args=(tcp_client,))
    recgnd.start()
