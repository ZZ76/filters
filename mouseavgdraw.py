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


def change(code):
    global x1, y1, x2, y2
    if readytoavg is True:
        if code == 0:  # w up
            y1, y2 = y1 - 1, y2 - 1
        elif code == 1:  # a left
            x1, x2 = x1 - 1, x2 - 1
        elif code == 2:  # s down
            y1, y2 = y1 + 1, y2 + 1
        elif code == 3:  # d right
            x1, x2 = x1 + 1, x2 + 1
        elif code == 4:  # increase
            if x1 > x2:
                x1, y1, x2, y2 = x1 + 1, y1 + 1, x2 - 1, y2 - 1
            else:
                x1, y1, x2, y2 = x1 - 1, y1 - 1, x2 + 1, y2 + 1
        elif code == 5:  # decrease
            if x2 > x1:
                x1, y1, x2, y2 = x1 + 1, y1 + 1, x2 - 1, y2 - 1
            else:
                x1, y1, x2, y2 = x1 - 1, y1 - 1, x2 + 1, y2 + 1
        drawonsrc(x1, y1, x2, y2, maskgray=maskgray)


def drawonsrc(x1, y1, x2, y2, maskgray=None):
    global masktoshow, canvasmask, src, xc, yc, rc
    masktoshow = src.copy()
    canvasmask = canvas.copy()
    xc, yc, rc = int((x2+x1)/2), int((y2+y1)/2), abs(int((x2-x1)/2))
    cv2.circle(masktoshow, (xc, yc), rc, (0, 255, 0), 2, lineType=cv2.LINE_AA)
    cv2.circle(canvasmask, (xc, yc), rc, (0, 255, 0), 1, lineType=cv2.LINE_AA)
    if maskgray is not None:
        maskgray[:] = 0
        cv2.circle(maskgray, (xc, yc), rc, 255, -1, lineType=cv2.LINE_AA)
    #print('pt1 = (%d, %d), pt2 = (%d, %d), ptc = (%d, %d), rc = %d' % (x1, y1, x2, y2, xc, yc, rc))
    print('r = ', rc)


def avgcolor(src, mask):
    _, contours, _ = cv2.findContours(mask, 1, 2)
    if len(contours) == 0:
        return -1
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


def main(src, loadimg=None):
    global maskgray, masktoshow, canvas, canvasmask, readytoavg
    maskgray = np.zeros((h, w, 1), np.uint8)
    if loadimg is None:
        canvas = np.zeros((h, w, 3), np.uint8)
        canvas[:] = 255
    else:
        canvas = loadimg
    masktoshow = src.copy()
    #canvasmask = canvas.copy()
    cv2.namedWindow('masktoshow')
    cv2.setMouseCallback('masktoshow', mousecontrol)
    cv2.namedWindow('canvas')
    cv2.setMouseCallback('canvas', mousecontrol)
    canvasmask = canvas.copy()
    while 1:
        cv2.imshow('masktoshow', masktoshow)
        cv2.imshow('canvas', canvasmask)
        #cv2.imshow('canvasmask', canvasmask)
        #cv2.imshow('maskgray', maskgray)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):   # calculate color
            if readytoavg is True:
                color = avgcolor(src, maskgray)
                print(color)
                cv2.circle(canvas, (xc, yc), rc, color, -1, lineType=cv2.LINE_AA)
                canvasmask = canvas.copy()
                drawonsrc(x1, y1, x2, y2)
        elif k == ord('o'):  # save/output
            cv2.imwrite('canvas.png', canvas)
        elif k == ord('e'):  # clear
            masktoshow = src.copy()
            canvasmask = canvas.copy()
            maskgray[:] = 0
            readytoavg = False
        elif k == ord('w'):  # up
            change(0)
        elif k == ord('a'):  # left
            change(1)
        elif k == ord('s'):  # down
            change(2)
        elif k == ord('d'):  # right
            change(3)
        elif k == ord(']'):  # increase
            change(4)
        elif k == ord('['):  # decrease
            change(5)
        elif k == 27:
            break

    cv2.destroyAllWindows()


pt1 = False
readytoavg = False

src = cv2.imread('lena.jpg')
h, w, _ = src.shape
w, h = 400, int(h*400/w)
src = cv2.resize(src, (w, h))
loadimg = cv2.imread('lena2.png')
#loadimg = None

main(src, loadimg=loadimg)