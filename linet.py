import cv2
import numpy as np
import math
from numpy import random as nr

img = cv2.imread('lena.jpg')
h, w, _ = img.shape
black = (0, 0, 0)
white = (255, 255, 255)

def lines(img, code=None, step=8):
    lines = np.zeros((h, w, 3), np.uint8)
    lines[:] = 255

    if code == 0:  # - horizontal
        for i in range(0, h, step):
            lines = cv2.line(lines, (0, i), (w, i), black)
    elif code == 1:  # | horizontal
        for i in range(0, w, step):
            lines = cv2.line(lines, (i, 0), (i, h), black)
    elif code == 2:  # \ 45
        #tmp = int(h*math.sqrt(2))
        for i in range(0, w, step):
            lines = cv2.line(lines, (i, 0), (h + i, h), black)
        for i in range(0, h, step):
            lines = cv2.line(lines, (0, i), (h - i, h), black)
    elif code == 3:  # / 45
        for i in range(0, 2*w, step):
            lines = cv2.line(lines, (i, 0), (0, i), black)
        #for i in range(0, h, step):
            #lines = cv2.line(lines, (w, i), (w - h + i, h), black)
    return lines

def tsh(img, code=None):
    type = cv2.THRESH_BINARY
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img_gray = cv2.equalizeHist(img_gray, img_gray)
    if code == 0:
        _, th = cv2.threshold(img_gray, 205, 255, type)
    elif code == 1:
        _, th = cv2.threshold(img_gray, 153, 255, type)
    elif code == 2:
        _, th = cv2.threshold(img_gray, 102, 255, type)
    elif code == 3:
        _, th = cv2.threshold(img_gray, 51, 255, type)
    th = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
    return th

def crosshatching():
    mask = lines(img, code=0)
    th = tsh(img, code=0)
    dst = cv2.addWeighted(mask, 1, th, 1, 0)
    dst2 = dst
    mask = lines(img, code=3)
    th = tsh(img, code=1)
    dst = cv2.addWeighted(mask, 1, th, 1, 0)
    dst = cv2.bitwise_and(dst, dst2)
    dst2 = dst
    mask = lines(img, code=1)
    th = tsh(img, code=2)
    dst = cv2.addWeighted(mask, 1, th, 1, 0)
    dst = cv2.bitwise_and(dst, dst2)
    dst2 = dst
    mask = lines(img, code=2)
    th = tsh(img, code=3)
    dst = cv2.addWeighted(mask, 1, th, 1, 0)
    dst = cv2.bitwise_and(dst, dst2)
    dst2 = dst
    return dst

seqline = (0, 3, 1, 2)
seqtsh = (0, 1, 2, 3)
dst = crosshatching()
#dst = cv2.resize(dst, (int(w/2), int(h/2)))
cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
