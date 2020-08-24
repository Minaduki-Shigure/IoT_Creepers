# -*- coding:utf-8 -*-
# @ProjectName  :IoTCreepers
# @FileName     :top.py
# @Time         :20-8-25
# @Author       :Minaduki

import time
import random

from newland_handler import NewLandHandler, handshare_data_test
from cam_manager import CamManager
from meter_utils import ImgRecgnition

camList = ['127.0.0.1', '192.168.3.13']
meterList = ['meter_1', 'meter_2', 'meter_3']
meterDict = {'meter_1': 0, 'meter_2': 1, 'meter_3': 0}

temp = 0


def get_pic_by_index(index):
    return camManager.request(index)


def recg(filename):
    imgRecg = ImgRecgnition(filename)
    return imgRecg.get_meter(), imgRecg.get_pic_processed()


if __name__ == '__main__':
    camManager = CamManager(camList)
    newLandd = NewLandHandler(handshare_data_test, get_pic_by_index)
    while True:
        time.sleep(1)
        for meter in meterList:
            value, pic = recg(get_pic_by_index(meterDict[meter]))
            newLandd.update_value(meter, value)
            time.sleep(0.5)
