# -*- coding:utf-8 -*-
# @ProjectName  :IoTCreepers
# @FileName     :top.py
# @Time         :20-8-25
# @Author       :Minaduki

from newland_handler import NewLandHandler, handshare_data
from cam_manager import CamManager

camList = ['192.168.1.32', '192.168.1.35']

def get_pic():
    return 


if __name__ == '__main__':
    camManager = CamManager(camList)
    newLandd = NewLandHandler(handshare_data, get_pic)