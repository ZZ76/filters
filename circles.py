import cv2
import numpy as np
import math
from numpy import random as nr
import sys
import crosshatching as ch


def putnoise(dense=None):
    n = np.zeros((h, w, 3), np.uint8)
    n[:] = 255
    t = int(dense/2000 * w * h)
    for i in range(t):
        x = nr.randint(1, w - 1)
        y = nr.randint(1, h - 1)
        n[y, x] = black
    return n


def createmasks(Numberoftsh=None):
    global masks
    for i in range(Numberoftsh):
        if masks is not None:
            masks = np.append(masks, np.expand_dims(putnoise(dense=denselist[i]), axis=0), axis=0)
        else:
            masks = putnoise(dense=denselist[i])
            masks = np.expand_dims(masks, axis=0)
        print(masks.shape)
    return masks


def combine(img, Numberoftsh=None, equalizeHist=False):
    dst2 = np.zeros((h, w, 3), np.uint8)
    dst2[:] = 255
    for i in range(Numberoftsh):
        mask = putnoise(dense=denselist[i])
        th = ch.tsh(img, stage=i, Numberoftsh=Numberoftsh, equalizeHist=equalizeHist)
        dst = cv2.addWeighted(mask, 1, th, 1, 0)
        dst = cv2.bitwise_and(dst, dst2)
        dst2 = dst
    return dst2


def videocombine(img, Numberoftsh=None, equalizeHist=False):
    dst2 = np.zeros((h, w, 3), np.uint8)
    dst2[:] = 255
    for i in range(Numberoftsh):
        th = ch.tsh(img, stage=i, Numberoftsh=Numberoftsh, equalizeHist=equalizeHist)
        dst = cv2.addWeighted(masks[i], 1, th, 1, 0)
        dst = cv2.bitwise_and(dst, dst2)
        dst2 = dst
    return dst2


def main():
    img = cv2.imread('lena.jpg')
    global w, h
    h, w, _ = img.shape
    w, h = int(w/2), int(h/2)
    img = cv2.resize(img, (w, h))
    dst = combine(img, Numberoftsh=4, equalizeHist=False)
    #dst = cv2.resize(dst, (int(w/2), int(h/2)))
    # voronoi start
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    points = None
    for i in range(w):
        for j in range(h):
            if dst[i, j] == 255:
                pass
            else:
                if points is None:
                    points = np.array([[i, j]])
                else:
                    points = np.append(points, [[i, j]], axis=0)
    print(points)
    from scipy.spatial import Voronoi, voronoi_plot_2d
    vor = Voronoi(points)
    import matplotlib.pyplot as plt
    voronoi_plot_2d(vor, show_points=True, vertices=False)
    plt.show()
    # voronoi end
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def vd(Numberoftsh=7):
    global w, h
    cap = cv2.VideoCapture(0)
    flag = False
    while (True):
        _, frame = cap.read()
        h, w, _ = frame.shape
        if flag == False:
            createmasks(Numberoftsh=Numberoftsh)
            flag = True
        frame = videocombine(frame, Numberoftsh=Numberoftsh)
        cv2.imshow('main', frame)
        #print(denselist[0].shape)
        #cv2.imshow('1', denselist[0])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


white = (255, 255, 255)
black = (0, 0, 0)
#denselist = (10, 20, 30, 40, 50, 60, 80)
denselist = (5, 25, 50, 80, 140, 220, 260)
masks = None

#main()
vd()
