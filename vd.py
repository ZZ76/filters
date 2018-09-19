import cv2
import crosshatching as ch

cap = cv2.VideoCapture(0)

while(True):
    _, frame = cap.read()
    ho, wo, _ = frame.shape
    frame = ch.vd(frame)
    cv2.imshow('main', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
