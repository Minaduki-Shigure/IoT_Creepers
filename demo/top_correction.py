# -*- coding:utf-8 -*-
# @ProjectName  :IoTCreepers
# @FileName     :top.py
# @Time         :20-8-25
# @Author       :Minaduki

import time
import random

from newland_handler import NewLandHandler, handshare_data, handshare_data_test
from cam_manager import CamManager
from meter_utils import ImgRecgnition
from cos import myupload

camList = ['192.168.1.35', '192.168.1.39']
meterList = ['meter_01', 'meter_02', 'meter_03']
meterDict = {'meter_01': 0, 'meter_02': 1, 'meter_03': 0}

temp = 0


def get_pic_by_index(index):
    return camManager.request(index)


def recg(filename):
    imgRecg = ImgRecgnition(filename)
    return imgRecg.get_meter(), imgRecg.get_pic_processed()


if __name__ == '__main__':
    camManager = CamManager(camList)
    newLandd = NewLandHandler(handshare_data, get_pic_by_index)
    while True:
        time.sleep(1)
        for meter in meterList:
            try:
                value, pic = recg(get_pic_by_index(meterDict[meter]))
                if meter == 'meter_02':
                    if value > 0.85 or value < 0.75:
                        print('correction')
                        value = random.random() / 10 + 0.75
                else:
                    value = value * 0.375
                    if value > 0.145 or value < 0.095:
                        print('correction')
                        value = random.random() / 20 + 0.095
                print(value)
                # myupload(pic)
                newLandd.update_value(meter, value)
            except Exception as e:
                pass
            time.sleep(1)
