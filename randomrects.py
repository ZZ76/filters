import cv2
import numpy as np
import math
from numpy import random
import sys
import time


def avgcolor(src, mask):
    _, contours, _ = cv2.findContours(mask, 1, 2)
    cnt = contours[0]
    lb, ub, wr, hr = cv2.boundingRect(cnt)
    rb, bb = lb + wr, ub + hr
    #start = time.time()
    colorlist = None
    for i in range(ub, bb):
        for j in range(lb, rb):
            if mask[i, j] != 0:
                if colorlist is None:
                    colorlist = [src[i, j]]
                else:
                    colorlist = np.append(colorlist, [src[i, j]], axis=0)
    #print(colorlist.shape)
    avg = np.mean(colorlist, axis=0)
    avgcolor = avg.astype(int)
    print('color', avgcolor)
    #end = time.time()
    #print('time', end - start)
    avgcolor = (int(avgcolor[0]), int(avgcolor[1]), int(avgcolor[2]))
    return avgcolor

def randomrects(img):
    wr = random.randint(minl, maxl)  # rect width
    hr = random.randint(minl, maxl)  # rect height
    x = random.randint(0, w-minl)
    y = random.randint(0, h-minl)
    x2 = x + wr
    y2 = y + hr
    if x2 > w:
        x2 = w
    if y2 > h:
        y2 = h
    print(x, y, x2, y2)
    img = cv2.rectangle(img, (x, y), (x2, y2), 255, thickness=-1)
    return img


def randomcircle(img):
    global x, y, cr
    cr = random.randint(minl, maxl)  # circle radius
    x = random.randint(0, w)
    y = random.randint(0, h)
    print(x, y, cr)
    img = cv2.circle(img, (x, y), cr, 255, thickness=-1, lineType=cv2.LINE_AA)
    return img


def main(mode='rect'):
    global mask, canvas, minl, maxl
    if mode == 'rect':
        list = rectlist
    elif mode == 'circle':
        list = circlelist
    for k in range(len(list)):
        minl = list[k][0]
        maxl = list[k][1]
        for i in range(list[k][2]):
            mask[:] = 0
            #mask = randomrects(mask)
            mask = randomcircle(mask)
            color = avgcolor(src, mask)
            #_, contours, hierarchy = cv2.findContours(mask, 1, 2)
            #cnt = contours[0]
            #canvas = cv2.fillPoly(canvas, [cnt], color)
            canvas = cv2.circle(canvas, (x, y), cr, color, thickness=-1, lineType=cv2.LINE_AA)
    return canvas


rectlist = [(200, 250, 10), (100, 150, 20), (60, 80, 30), (40, 60, 40), (10, 30, 50), (5, 20, 50)]
circlelist = [(80, 120, 25), (50, 80, 35), (30, 40, 60), (20, 30, 80), (5, 15, 120), (3, 10, 120)]
# minx, maxl, loop times


src = cv2.imread('kim.jpg')
h, w, _ = src.shape
w, h = 400, int(h*400/w)
src = cv2.resize(src, (w, h))
mask = np.zeros((h, w, 1), np.uint8)
canvas = np.zeros((h, w, 3), np.uint8)
canvas[:] = 255

canvas = main(mode='circle')

cv2.imshow('canvas', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
