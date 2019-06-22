import cv2
import numpy as np
import math
from numpy import random
import sys
import time
import util


def mousecontrol(event, x, y, flags, param):
    global x1, y1, x2, y2, readytoavg, pt1, maskgray
    if event == cv2.EVENT_LBUTTONDOWN:  # record start point
        print('\non')
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
    if abs(x1 - x2) >= abs(y1 - y2):
        rc = abs(int((y2 - y1) / 2))
    else:
        rc = abs(int((x2 - x1) / 2))
    if y2 >= y1:
        yc = y1 + rc
    else:
        yc = y1 - rc
    if x2 >= x1:
        xc = x1 + rc
    else:
        xc = x1 - rc
    #xc, yc, rc = int((x2 + x1) / 2), int((y2 + y1) / 2), abs(int((x2 - x1) / 2))
    cv2.circle(masktoshow, (xc, yc), rc, (0, 255, 0), 2, lineType=cv2.LINE_AA)
    cv2.circle(canvasmask, (xc, yc), rc, (0, 255, 0), 1, lineType=cv2.LINE_AA)
    if maskgray is not None:
        maskgray[:, :, :] = 0
        cv2.circle(maskgray, (xc, yc), rc, (1, 1, 1), -1, lineType=cv2.LINE_AA)
    #print('pt1 = (%d, %d), pt2 = (%d, %d), ptc = (%d, %d), rc = %d' % (x1, y1, x2, y2, xc, yc, rc))
    print('r = ', rc, end='\r', flush=True)


def main(src, loadimg=None):
    global maskgray, masktoshow, canvas, canvasmask, readytoavg, rc, mode
    maskgray = np.zeros((h, w, 3), np.uint8)
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
    while mode:
        cv2.imshow('masktoshow', masktoshow)
        cv2.imshow('canvas', canvasmask)
        #cv2.imshow('canvasmask', canvasmask)
        #cv2.imshow('maskgray', maskgray)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):   # calculate color
            if readytoavg is True:
                color = util.get_avgcolor_downsize(src, maskgray, 100)
                #util.get_avgcolor_crop(src, maskgray)
                #util.get_avgcolor_full(src, maskgray)
                print(color)
                cv2.circle(canvas, (xc, yc), rc, color, -1, lineType=cv2.LINE_AA)
                canvasmask = canvas.copy()
                drawonsrc(x1, y1, x2, y2)
        elif k == ord('o'):  # save/output
            cv2.imwrite('result/canvas.png', canvas)
        elif k == ord('e'):  # clear
            masktoshow = src.copy()
            canvasmask = canvas.copy()
            maskgray[:, :, :] = 0
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
mode = 1

src = cv2.imread('image/parrot.jpg')
h, w, _ = src.shape
w, h = 800, int(h*800/w)
src = cv2.resize(src, (w, h))
loadimg = cv2.imread('result/randomcircle.png')
loadimg = None

main(src, loadimg=loadimg)
