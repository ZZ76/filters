import cv2
import crosshatching as ch

cap = cv2.VideoCapture(0)
flag = False
Numberoftsh = 7
while(True):
    _, frame = cap.read()
    ch.h, ch.w, _ = frame.shape
    if flag == False:
        ch.masks = ch.createmasks(frame, Numberoftsh=Numberoftsh)
        flag = True
    frame = ch.videocrosshatching(frame, Numberoftsh=Numberoftsh)
    cv2.imshow('main', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
