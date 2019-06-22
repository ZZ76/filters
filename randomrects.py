import cv2
import numpy as np
import math
from numpy import random
import sys
import time
import util


def randomrects(img):
    global wr, hr
    wr = random.randint(minl, maxl)  # rect width
    hr = random.randint(minl, maxl)  # rect height
    x = random.randint(0-minl, w-minl)
    y = random.randint(0-minl, h-minl)
    x2 = x + wr
    y2 = y + hr
    if x2 > w:
        x2 = w
    if y2 > h:
        y2 = h
    #print('x = %d, y = %d, x2 = %d, y2 = %d' % (x, y, x2, y2))
    img = cv2.rectangle(img, (x, y), (x2, y2), (1, 1, 1), thickness=-1)
    return img


def randomcircle(img):
    global x, y, cr
    cr = random.randint(minl, maxl)  # circle radius
    x = random.randint(0, w)
    y = random.randint(0, h)
    #print('centre = (%d, %d), r = %d' % (x, y, cr))
    img = cv2.circle(img, (x, y), cr, (1, 1, 1), thickness=-1, lineType=cv2.LINE_AA)
    return img


def avgcolorslow(src, mask):
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
                else:
                    colorlist = np.append(colorlist, [src[i, j]], axis=0)
    #print(colorlist.shape)
    avg = np.mean(colorlist, axis=0)
    avgcolor = avg.astype(int)
    print('color', avgcolor)
    end = time.time()
    print('time', end - start)
    avgcolor = (int(avgcolor[0]), int(avgcolor[1]), int(avgcolor[2]))
    return avgcolor


def main(mode='rect', show=True):
    global src, mask, canvas, minl, maxl, src400, src200
    w2, h2 = 400, int(h * 400 / w)
    src400 = cv2.resize(src, (w2, h2))
    w2, h2 = 200, int(h * 200 / w)
    src200 = cv2.resize(src, (w2, h2))
    if mode == 'rect':
        list = rectlist
    else:
        list = circlelist
    for k in range(len(list)):
        minl = list[k][0]
        maxl = list[k][1]
        for i in range(list[k][2]):
            mask[:] = 0
            if mode == 'rect':  # generate rectangular
                mask = randomrects(mask)
                #color = avgcolor(src, mask)
                _, contours, hierarchy = cv2.findContours(cv2.resize(mask[:, :, 0], (mask.shape[1], mask.shape[0])), 1, 2)
                cnt = contours[0]
                #canvas = cv2.fillPoly(canvas, [cnt], color)
                if wr < 100 or hr < 100:
                    color = util.get_avgcolor_crop(src, mask)
                    canvas = cv2.fillPoly(canvas, [cnt], color)
                elif wr >= 100 and wr <= 200 or hr >= 100 and hr < 200:
                    color = util.get_avgcolor_downsize(src, mask, 400)
                    canvas = cv2.fillPoly(canvas, [cnt], color)
                else:
                    color = util.get_avgcolor_downsize(src, mask, 200)
                    canvas = cv2.fillPoly(canvas, [cnt], color)

                if show is True:
                    cv2.imshow('canvas', canvas)
                    k = cv2.waitKey(1) & 0xFF
                    if k == ord('q'):
                        break

            else:  # generate circle
                mask = randomcircle(mask)
                if cr < 60:
                    color = util.get_avgcolor_crop(src, mask)
                    canvas = cv2.circle(canvas, (x, y), cr, color, thickness=-1, lineType=cv2.LINE_AA)
                elif cr >= 60 and cr <= 120:
                    color = util.get_avgcolor_downsize(src, mask, 400)
                    canvas = cv2.circle(canvas, (x, y), cr, color, thickness=-1, lineType=cv2.LINE_AA)
                else:
                    color = util.get_avgcolor_downsize(src, mask, 200)
                    canvas = cv2.circle(canvas, (x, y), cr, color, thickness=-1, lineType=cv2.LINE_AA)

                if show is True:
                    cv2.imshow('canvas', canvas)
                    cv2.waitKey(1)

    return canvas


rectlist = [(200, 250, 25), (100, 150, 35), (60, 80, 60), (40, 60, 80), (10, 30, 80), (5, 20, 80)]  # for width 400
circlelist = [(80, 120, 25), (50, 80, 35), (30, 40, 60), (20, 30, 80), (5, 15, 110), (3, 10, 110)]  # width 400
# min length/radius, max length/radius, loop times
rectlist = [(200, 400, 50), (100, 200, 300), (80, 160, 600), (20, 100, 600), (10, 50, 600)]  # width 800
circlelist = [(100, 120, 50), (40, 60, 600), (10, 30, 600), (6, 20, 600)]  # width 800


src = cv2.imread('image/21.jpg')
h, w, _ = src.shape
newsize = 800
w, h = newsize, int(h*newsize/w)
src = cv2.resize(src, (w, h))
mask = np.zeros((h, w, 3), np.uint8)
canvas = np.zeros((h, w, 3), np.uint8)
canvas[:] = 255

canvas = main(mode='circle', show=False)


cv2.imshow('canvas', canvas)
k = cv2.waitKey(0) & 0xFF
if k == ord('s'):
    cv2.imwrite('result/randomcircle.png', canvas)
    #cv2.imwrite('result/randomcircle.png', canvas)
if k == ord('q'):
    #cv2.imwrite('result/randomcircle.png', canvas)
    cv2.destroyAllWindows()
