import requests
import json
import cv2
import base64

url = 'http://ocr.minaduki.cn:8866/predict/chinese_ocr_db_crnn_server'
# url = 'http://ocr.schwi.cn/predict/chinese_ocr_db_crnn_server'
# url = 'http://icais.tpddns.cn:8866/predict/chinese_ocr_db_crnn_server'

rangeDict = {'甲':1.6, '乙':0.16, 'Z':0.16, 'z':0.16, '丙':1, '丁':4, '戊':0.6}
cheatDict = {'甲':0.47, '乙':0.00, 'Z':0.00, 'z':0.00, '丙':0.0, '丁':0.11, '戊':0.13}


def cv2_to_base64(image):
    data = cv2.imencode('.png', image)[1]
    return base64.b64encode(data.tobytes()).decode('utf8')


def get_ocr_result(img):
    data = {'images':[cv2_to_base64(img)]}
    # print('data prepared')
    headers = {"Content-type": "application/json"}
    # print('start request')
    r = requests.post(url = url, headers = headers, data = json.dumps(data))
    # print('end request')
    result = r.json()["results"]
    # print(result)
    data = result[0]['data']
    ret = []
    for item in data:
        ret.append(item['text'])
    return ret


def get_range(img):
    ocr = get_ocr_result(img)
    for key in rangeDict.keys():
        if key in ocr:
            return rangeDict[key]
    return None


def get_cheat(img):
    ocr = get_ocr_result(img)
    for key in cheatDict.keys():
        if key in ocr:
            return cheatDict[key]
    return None


if __name__ == '__main__':
    filename = '../Desktop/00.jpg'
    img = cv2.imread(filename)
    range = get_range(img)
    if not range:
        print('Failed')
    else:
        print(range)