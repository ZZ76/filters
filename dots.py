import cv2
import numpy as np
import math
from numpy import random as nr
import sys
import crosshatching as ch

class dot:
    def __init__(self, location):
        self.location = location  # centre
        self.r_now = 0  # radius
        self.r_next = 0
        self.r_target = 0
        self.speed = 2  # 2 change speed

    def update(self, img, newradius=None, color=None):
        if newradius is not None:
            self.r_target = newradius
        if self.r_target != self.r_now:
            if self.r_target - self.r_now > self.speed:   # increase
                self.r_next = self.r_now + self.speed
            elif self.r_target - self.r_now < -self.speed:   # decrease
                self.r_next = self.r_now - self.speed
            else:
                self.r_next = self.r_target
        if color is None:
            color = black
        else:
            color = (int(color[0]), int(color[1]), int(color[2]))
        #print('target =', self.r_target, 'now =', self.r_now, 'next =', self.r_next, )
        cv2.circle(img, self.location, self.r_next, color, -1, lineType=cv2.LINE_AA)
        self.r_now = self.r_next


def createdotmat(img):
    h, w, _ = img.shape
    w, h = int(w/resizerate), int(h/resizerate)
    tmp = None
    global dots
    for i in range(h):  # x
        for j in range(w):  # y
            if tmp is None:
                tmp = np.array([[dot((int((2*j+1)*maxradius), int((2*i+1)*maxradius)))]])
            else:
                tmp = np.append(tmp, [[dot((int((2*j+1)*maxradius), int((2*i+1)*maxradius)))]], axis=0)
            #print(tmp.shape)
        if dots is None:
            dots = tmp
            tmp = None
        else:
            dots = np.append(dots, tmp, axis=1)
            tmp = None
            #print(dots.shape)
    print(dots.shape)
    return dots

def createmasks(img, color=False):
    h, w, _ = img.shape
    w, h = int(w/resizerate), int(h/resizerate)
    if color is False:
        f = np.zeros((int(2 * h * maxradius), int(2 * w * maxradius), 1), np.uint8)   # frame
    else:
        f = np.zeros((int(2 * h * maxradius), int(2 * w * maxradius), 3), np.uint8)
    f[:] = 255
    gm = cv2.resize(img, (w, h))  # grayscale mask
    gm = cv2.cvtColor(gm, cv2.COLOR_BGR2GRAY)
    if color is False:
        return f, gm
    else:
        cm = cv2.resize(img, (w, h))
        #print('cm shape', cm.shape)
        return f, gm, cm


def updatematrix(src, dst, mat, colormat=None):
    dst[:] = 255
    h, w = src.shape
    for i in range(h):
        for j in range(w):
            if colormat is None:
                mat[j, i].update(dst, newradius=int(maxradius*(255-src[i, j])/255))
            else:
                #print(colormat[i, j])
                mat[j, i].update(dst, newradius=int(maxradius * (255 - src[i, j]) / 255), color=colormat[i, j])


def videodots(video=None):
    global dots
    if video is None:
        cap = cv2.VideoCapture(0)
    else:
        cap = video
    while(True):
        _, frame = cap.read()
        h, w, _ = frame.shape
        if dots is None:
            dots = createdotmat(frame)
        #frame = cv2.resize(frame, (64, 48))
        #cv2.imshow('frame', frame)
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
        frame = cv2.flip(frame, 1)
        f, gm, cm = createmasks(frame, color=True)
        updatematrix(gm, f, dots, colormat=cm)
        #cm = cv2.resize(cm, (w, h), interpolation=cv2.INTER_AREA)
        #gm = cv2.resize(gm, (w, h), interpolation=cv2.INTER_AREA)
        #f = cv2.resize(f, (w, h))
        #cv2.imshow('mask', cm)
        cv2.imshow('f', f)
        #cv2.imshow('gm', gm)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def imagedots(img):
    h, w, _ = img.shape
    global dots
    if dots is None:
        dots = createdotmat(img)
    while dots is not None:
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
        f, gm, cm = createmasks(img, color=True)
        gm = cv2.equalizeHist(gm, gm)
        updatematrix(gm, f, dots, colormat=cm)
        cm = cv2.resize(cm, (w, h), interpolation=cv2.INTER_AREA)
        #cv2.imshow('main', frame)
        cv2.imshow('mask', cm)
        cv2.imshow('f', f)
        #cv2.imshow('gm', gm)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


black = (0, 0, 0)
maxradius = 15   # 15
dots = None
resizerate = 25   # default 25, w/resizerate and h/resizerate is how many dots in x and y axis

#vd = cv2.VideoCapture('Wildlife.wmv')
videodots()   # use camera and display
'''img = cv2.imread('image/owl.jpg')
h, w, _ = img.shape
img = cv2.resize(img, (int(w/2), int(h/2)))
imagedots(img)'''
