import cv2
import numpy as np
import math
from numpy import random as nr
import sys


def lines(img, code=None, step=12):
    l = np.zeros((h, w, 3), np.uint8)
    l[:] = 255

    if code == 0:  # - horizontal
        for i in range(0, h, step):
            l = cv2.line(l, (0, i), (w, i), black)
    elif code == 1:  # | horizontal
        for i in range(0, w, step):
            l = cv2.line(l, (i, 0), (i, h), black)
    elif code == 2:  # \ 45
        l = lines(img, code=3, step=step)
        l = cv2.flip(l, 0)
    elif code == 3:  # / 45
        for i in range(0, 2*w, step):
            l = cv2.line(l, (i, 0), (0, i), black)
    elif code == 4:  # / 22.5
        cotheta = 2.4142
        tantheta = 0.4142
        for i in range(0, int(w+h*cotheta), step):
            l = cv2.line(l, (i, 0), (0, int(i*tantheta)), black)
    elif code == 5:  # / 67.5
        cotheta = 0.4142
        tantheta = 2.4142
        for i in range(0, int(w+h*cotheta), step):
            l = cv2.line(l, (i, 0), (0, int(i*tantheta)), black)
    return l


def tsh(img, stage=None, Numberoftsh=None, equalizeHist=False):
    type = cv2.THRESH_BINARY
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if equalizeHist == False:
        pass
    else:
        img_gray = cv2.equalizeHist(img_gray, img_gray)
    _, th = cv2.threshold(img_gray, 255-int(((stage+1)/Numberoftsh)*255), 255, type)
    th = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
    return th

def tsh2(img, code=None, equalizeHist=False):
    type = cv2.THRESH_BINARY
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if equalizeHist == False:
        pass
    else:
        img_gray = cv2.equalizeHist(img_gray, img_gray)
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


def crosshatching(img, Numberoftsh=None, equalizeHist=False):
    dst2 = np.zeros((h, w, 3), np.uint8)
    dst2[:] = 255
    for i in range(Numberoftsh):
        mask = lines(img, code=seqline[i], step=8)
        th = tsh(img, stage=i, Numberoftsh=Numberoftsh, equalizeHist=equalizeHist)
        dst = cv2.addWeighted(mask, 1, th, 1, 0)
        dst = cv2.bitwise_and(dst, dst2)
        dst2 = dst
    return dst2


def crosshatching2(img):
    mask = lines(img, code=0, step=8)
    th = tsh(img, code=0)
    dst = cv2.addWeighted(mask, 1, th, 1, 0)
    dst2 = dst
    mask = lines(img, code=4)
    th = tsh(img, code=1)
    dst = cv2.addWeighted(mask, 1, th, 1, 0)
    dst = cv2.bitwise_and(dst, dst2)
    dst2 = dst
    mask = lines(img, code=3)
    th = tsh(img, code=2)
    dst = cv2.addWeighted(mask, 1, th, 1, 0)
    dst = cv2.bitwise_and(dst, dst2)
    dst2 = dst
    mask = lines(img, code=5)
    th = tsh(img, code=3)
    dst = cv2.addWeighted(mask, 1, th, 1, 0)
    dst = cv2.bitwise_and(dst, dst2)
    dst2 = dst
    return dst

def main(img):
    global w, h, seqline
    h, w, _ = img.shape
    seqline = (0, 4, 3, 5, 1, 2)
    Numberoftsh = 6
    dst = crosshatching(img, Numberoftsh=Numberoftsh)
    #dst = cv2.resize(dst, (int(w/2), int(h/2)))
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def vd(img):
    global w, h, seqline, Numberoftsh
    h, w, _ = img.shape
    seqline = (0, 3, 1, 2)
    Numberoftsh = 5
    dst = crosshatching(img)
    return dst

black = (0, 0, 0)
white = (255, 255, 255)
red = (0, 0, 255)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pass
    else:
        img = cv2.imread('kim.jpg')
        main(img)
else:
    pass


