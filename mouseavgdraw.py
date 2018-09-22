import cv2
import numpy as np
import math
from numpy import random
import sys
import time


def mousecontrol(event, x, y, flags, param):
    global x1, y1, x2, y2, readytoavg, pt1, maskgray
    if event == cv2.EVENT_LBUTTONDOWN:  # record start point
        print('on')
        if pt1 is False:
            x1, y1 = x, y  # point 1
            pt1 = True  # point 1 is recorded
            readytoavg = False

    elif event == cv2.EVENT_MOUSEMOVE:
        if pt1 is True:
            x2, y2 = x, y
            drawonsrc(x1, y1, x2, y2)

    elif event == cv2.EVENT_LBUTTONUP:  # record end point
        x2, y2 = x, y
        if pt1 is True:
            drawonsrc(x1, y1, x2, y2, maskgray=maskgray)
            pt1 = False
            readytoavg = True
        pass


def drawonsrc(x1, y1, x2, y2, maskgray=None):
    global masktoshow, src, xc, yc, rc
    masktoshow = src.copy()
    xc, yc, rc = int((x2+x1)/2), int((y2+y1)/2), abs(int((x2-x1)/2))
    cv2.circle(masktoshow, (xc, yc), rc, (0, 255, 0), 2, lineType=cv2.LINE_AA)
    if maskgray is not None:
        maskgray[:] = 0
        cv2.circle(maskgray, (xc, yc), rc, 255, -1, lineType=cv2.LINE_AA)



def avgcolor(src, mask):
    _, contours, _ = cv2.findContours(mask, 1, 2)
    cnt = contours[0]
    lb, ub, wr, hr = cv2.boundingRect(cnt)
    rb, bb = lb + wr, ub + hr
    start = time.time()
    colorlist = None
    for i in range(ub, bb):
        for j in range(lb, rb):
            if mask[i, j] != 0:
                if colorlist is None:
                    colorlist = [src[i, j]]
                    #print(mask[i, j], src[i, j])
                else:
                    colorlist = np.append(colorlist, [src[i, j]], axis=0)
                    #print(mask[i, j], src[i, j])
    print(colorlist.shape)
    avg = np.mean(colorlist, axis=0)
    avgcolor = avg.astype(int)
    print(avgcolor)
    end = time.time()
    print('time', end - start)
    avgcolor = (int(avgcolor[0]), int(avgcolor[1]), int(avgcolor[2]))
    return avgcolor

pt1 = False
src = cv2.imread('kim.jpg')
h, w, _ = src.shape
w, h = 400, int(h*400/w)
src = cv2.resize(src, (w, h))
maskgray = np.zeros((h, w, 1), np.uint8)
canvas = np.zeros((h, w, 3), np.uint8)
canvas[:] = 255
mode = 0
masktoshow = src.copy()
cv2.namedWindow('masktoshow')
cv2.setMouseCallback('masktoshow', mousecontrol)

while(1):
    cv2.imshow('masktoshow', masktoshow)
    cv2.imshow('canvas', canvas)
    cv2.imshow('maskgray', maskgray)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('c'):
        if readytoavg is True:
            color = avgcolor(src, maskgray)
            print(color)
            cv2.circle(canvas, (xc, yc), rc, color, -1, lineType=cv2.LINE_AA)
    elif k == ord('s'):
        cv2.imwrite('canvas.png', canvas)
    elif k == 27:
        break

cv2.destroyAllWindows()