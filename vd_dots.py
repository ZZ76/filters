import cv2
import dots

cap = cv2.VideoCapture(0)


while(True):
    global dots
    _, frame = cap.read()
    h, w, _ = frame.shape
    if dots.dots is None:
        print('create')
        dots.createdotmat(frame)
    frame = cv2.resize(frame, (64, 48))
    frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
    cv2.imshow('main', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
