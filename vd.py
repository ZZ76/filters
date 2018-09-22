import cv2
import numpy as np
import crosshatching as ch

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('Wildlife.wmv')

while(True):
    _, frame = cap.read()
    ch.h, ch.w, _ = frame.shape
    frame = cv2.flip(frame, 1)
    frame = ch.crosshatching(frame, Numberoftsh=7, equalizeHist=False, color=True)
    #frame = cv2.resize(frame, (int(ch.w * 1.5), int(ch.h * 1.5)))
    cv2.imshow('main', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
