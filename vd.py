import cv2
import numpy as np
import crosshatching as ch

cap = cv2.VideoCapture(0)
flag = False
Numberoftsh = 7
white = np.zeros((480, 640, 3), np.uint8)
white[:] = 255
while(True):
    _, frame = cap.read()
    ch.h, ch.w, _ = frame.shape
    frame = cv2.flip(frame, 1)
    #ch.h, ch.w = int(ch.h/2), int(ch.w/2)
    #frame = cv2.resize(frame, (ch.w, ch.h))
    if flag == False:
        ch.masks = ch.createmasks(frame, Numberoftsh=Numberoftsh)
        flag = True
    line = ch.videocrosshatching(frame, Numberoftsh=Numberoftsh,  equalizeHist=True)
    frame = cv2.bitwise_or(line, frame)
    #frame = cv2.resize(frame, (int(ch.w * 1.5), int(ch.h * 1.5)))
    cv2.imshow('main', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
