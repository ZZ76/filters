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
        self.speed = 2  # change speed

    def update(self, img, newradius=None):
        if newradius is not None:
            self.r_target = newradius
        if self.r_target != self.r_now:
            if self.r_target - self.r_now > self.speed:   # increase
                self.r_next = self.r_now + self.speed
            elif self.r_target - self.r_now < -self.speed:   # decrease
                self.r_next = self.r_now - self.speed
            else:
                self.r_next = self.r_target

        #print('target =', self.r_target, 'now =', self.r_now, 'next =', self.r_next, )
        cv2.circle(img, self.location, self.r_next, black, -1, lineType=cv2.LINE_AA)
        self.r_now = self.r_next

black = (0, 0, 0)
maxradius = 15
dots = None

def createdotmat(img):
    h, w, _ = img.shape
    w, h = int(w/30), int(h/30)
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
    return dots

def createmasks(img):
    h, w, _ = img.shape
    w, h = int(w / 30), int(h / 30)
    f = np.zeros((int(2 * h * maxradius), int(2 * w * maxradius), 1), np.uint8)
    f[:] = 255
    mask = cv2.resize(img, (w, h))  # small
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    return f, mask

def updatematrix(src, dst, mat):
    dst[:] = 255
    h, w = src.shape
    for i in range(h):
        for j in range(w):
            mat[j, i].update(dst, newradius=int(maxradius*(255-src[i, j])/255))

cap = cv2.VideoCapture(0)
while(True):
    _, frame = cap.read()
    h, w, _ = frame.shape
    if dots is None:
        dots = createdotmat(frame)
    frame = cv2.resize(frame, (64, 48))
    frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
    f, m = createmasks(frame)
    updatematrix(m, f, dots)
    cv2.imshow('main', frame)
    cv2.imshow('f', f)
    cv2.imshow('m', m)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

'''n = np.zeros((200, 200, 3), np.uint8)
n[:] = 255
flag = True
dots = [dot((50, 50)), dot((150, 150))]
dots.append(dot((50, 150)))
while n is not None:
    r = nr.randint(0, 30)
    r2 = nr.randint(0, 30)
    r3 = nr.randint(0, 30)
    print('r=', r)
    if flag is True:
        pass
    else:
        break
    for i in range(10):
        n[:] = 255
        dots[0].update(n, r)
        dots[1].update(n, r2)
        dots[2].update(n, r3)
        cv2.imshow('dst', n)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            flag = False
            break
cv2.destroyAllWindows()'''
