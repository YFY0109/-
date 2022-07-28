import os
import re
# import winsound

import cv2
import numpy as np
from pyzbar import pyzbar

import robot

result = []


def decodeDisplay(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)
        barcodeData = barcode.data.decode('utf-8')
        iscorrect = False
        if re.search(r'https://ymt.shaanxi.gov.cn/ptrace/view/login.html.code=.*', barcodeData):
            iscorrect = not iscorrect
        if not iscorrect:
            # winsound.Beep(1000, 1000)
            os.system('play ~/scanHealthQR/res/cant.wav')
            result.append("伪造")
            break
        # if detectColor(image, "grey"):
        #     winsound.Beep(1000, 1000)
        #     os.system('play ~/scanHealthQR/res/grey.wav')
        #     break
        if detectColor(image, "green"):
            # winsound.Beep(1000, 1000)
            thread = robot.thread(1, 2)
            thread.start()
            os.system('play ~/scanHealthQR/res/go.wav')
            result.append("正常")
            break
        if detectColor(image, "red"):
            # winsound.Beep(1000, 1000)
            os.system('play ~/scanHealthQR/res/not.wav')
            result.append("隔离")
    return image


color_dict = {
    'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
    'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
    'green': {'Lower': np.array([50, 43, 46]), 'Upper': np.array([77, 255, 255])},
    # 'grey': {'Lower': np.array([50, 10, 46]), 'Upper': np.array([90, 205, 230])}
}


def detectColor(image, color):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gs = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(gs, cv2.COLOR_BGR2HSV)
    erode_hsv = cv2.erode(hsv, None, iterations=2)
    inRange_hsv = cv2.inRange(
        erode_hsv, color_dict[color]['Lower'], color_dict[color]['Upper'])
    contours = cv2.findContours(
        inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    return len(contours) > 0


def detect():
    camera = cv2.VideoCapture(0)
    ret, frame = True, None
    while True:
        ret, frame = camera.read()
        color = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        im = decodeDisplay(color)
        cv2.imshow('camera', im)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    detect()
