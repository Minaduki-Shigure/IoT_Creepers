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


def recg(imgRecg, filename):
    imgRecg.img_init(filename)
    ret = imgRecg.get_meter()
    imgRecg.get_pic_processed()
    return ret


if __name__ == '__main__':
    camManager = CamManager(camList)
    newLandd = NewLandHandler(handshare_data, get_pic_by_index)
    imgRecg0 = ImgRecgnition()
    imgRecg1 = ImgRecgnition()
    while True:
        # time.sleep(0.1)
        for meter in meterList:
            try:
                pic = get_pic_by_index(meterDict[meter])
                # time.sleep(0.5)
                if meter == 'meter_02':                     
                    value = recg(imgRecg1, pic)
                else:
                    value = recg(imgRecg0, pic)                                       
                    value = value * 2.5                   
                print(value)
                # myupload(pic)
                newLandd.update_value(meter, value)
            except Exception as e:
                print(e)
                pass
            # time.sleep(0.1)
