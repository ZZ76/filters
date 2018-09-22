import cv2
import numpy as np
import math
from numpy import random as nr
import sys


def lines(code=None, step=12):
    l = np.zeros((h, w, 3), np.uint8)
    l[:] = 255

    if code == 0:  # - horizontal
        for i in range(0, h, step):
            l = cv2.line(l, (0, i), (w, i), black)
    elif code == 1:  # | horizontal
        for i in range(0, w, step):
            l = cv2.line(l, (i, 0), (i, h), black)
    elif code == 2:  # \ 45
        l = lines(code=3, step=step)
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
    else:
        pass   # empty
    return l


def tsh(img, stage=None, Numberoftsh=None, equalizeHist=False):
    type = cv2.THRESH_BINARY
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if equalizeHist == False:
        pass
    else:
        img_gray = cv2.equalizeHist(img_gray, img_gray)
    _, th = cv2.threshold(img_gray, 255-int(((stage)/Numberoftsh)*255), 255, type)
    th = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
    return th


def createmasks(img, Numberoftsh=None):
    global masks
    for i in range(Numberoftsh):
        if seqline[i] == 4:
            step = 16
        elif seqline[i] == 5:
            step = 10
        else:
            step = 8
        if masks is not None:
            masks = np.append(masks, np.expand_dims(lines(code=seqline[i], step=step), axis=0), axis=0)
        else:
            masks = lines(code=seqline[i], step=step)
            masks = np.expand_dims(masks, axis=0)
        #print(masks.shape)
    return masks


def crosshatching(img, Numberoftsh=None, equalizeHist=False, color=False):
    global frame, flag, w, h
    h, w, _ = img.shape
    frame = np.zeros((h, w, 3), np.uint8)
    frame[:] = 255
    if flag is False:
        createmasks(img, Numberoftsh=Numberoftsh)
        flag = True
    for i in range(Numberoftsh):
        th = tsh(img, stage=i, Numberoftsh=Numberoftsh, equalizeHist=equalizeHist)
        dst = cv2.addWeighted(masks[i], 1, th, 1, 0)
        dst = cv2.bitwise_and(dst, frame)
        frame = dst
    if color is False:
        return frame
    else:
        frame = cv2.bitwise_or(frame, img)
        return frame



def showimage(img, Numberoftsh = 7, equalizeHist=False):
    global w, h
    h, w, _ = img.shape
    dst = crosshatching(img, Numberoftsh=Numberoftsh, equalizeHist=equalizeHist, color=True)
    #dst = cv2.resize(dst, (int(w/2), int(h/2)))
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def playvideo(video, Numberoftsh=None, color=False):
    global w, h
    while (True):
        _, frame = video.read()
        frame = crosshatching(frame, Numberoftsh=Numberoftsh, equalizeHist=False, color=color)
        cv2.imshow('main', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


black = (0, 0, 0)
white = (255, 255, 255)
#red = (0, 0, 255)
#green = (0, 255, 0)
#blue = (255, 0, 0)
seqline = (-1, 0, 4, 3, 5, 2, 1)
masks = None
flag = False  # existence of line masks

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pass
    else:
        #img = cv2.imread('eagle.jpg')
        #h, w, _ = img.shape
        #img = cv2.resize(img, (int(w/8), int(h/8)))
        #showimage(img)
        video = cv2.VideoCapture(0)
        #video = cv2.VideoCapture('Wildlife.wmv')
        playvideo(video, Numberoftsh=7, color=True)


