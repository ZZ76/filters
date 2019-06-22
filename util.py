import cv2
import numpy as np
import math
from numpy import random
import sys
import time


def get_avgcolor_crop(src, mask):  # fast
    #start = time.time()
    _, contours, _ = cv2.findContours(cv2.resize(mask[:, :, 0], (mask.shape[1], mask.shape[0])), 1, 2)
    if len(contours) == 0:
        return
    cnt = contours[0]
    lb, ub, wr, hr = cv2.boundingRect(cnt)
    rb, bb = lb + wr, ub + hr
    m = mask[ub:bb, lb:rb]  # sub mask
    #m = cv2.resize(m, (wr, hr))  # fix a small shape problem
    subsrc = src[ub:bb, lb:rb]
    subsrc = subsrc * m
    #b, g, r = cv2.split(subsrc)
    n = m[:, :, 0].sum()
    if n == 0:
        return
    b = int(subsrc[:, :, 0].sum()/n)  # value sum in b where is 1 in mask
    g = int(subsrc[:, :, 1].sum()/n)
    r = int(subsrc[:, :, 2].sum()/n)
    avgcolor = (b, g, r)
    #print(avgcolor)
    #end = time.time()
    #print('time  ', end - start)
    return avgcolor


def get_avgcolor_full(src, mask):  # slow
    #start = time.time()
    if mask.sum() == 0:
        return
    subsrc = src * mask
    n = np.sum(mask[:, :, 0])
    b = int(subsrc[:, :, 0].sum()/n)  # value sum in b where is 1 in mask
    g = int(subsrc[:, :, 1].sum()/n)
    r = int(subsrc[:, :, 2].sum()/n)
    avgcolor = (b, g, r)
    #print(avgcolor)
    #end = time.time()
    #print('time 2', end - start)
    return avgcolor
    
    
def get_avgcolor_downsize(src, mask, smallerwidth):   # calculate on smaller size, the fastest
    #start = time.time()
    h, w = src.shape[0], src.shape[1]
    w2, h2 = smallerwidth, int(h*smallerwidth/w)
    masksmall = cv2.resize(mask, (w2, h2))
    srcsmall = cv2.resize(src, (w2, h2))
    color = get_avgcolor_crop(srcsmall, masksmall)
    #print(color)
    #end = time.time()
    #print('time s', end - start)
    return color