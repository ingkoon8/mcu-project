
import cv2
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.6
RED = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

model = YOLO('/Users/yujaemin/Yolov5/best2.pt')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:

    ret, frame = cap.read()
    if not ret:
        print('Cam Error')
        break

    detection = model(frame)[0]

    for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
        confidence = float(data[4])
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        a = (xmax + ymin)/2 # 낙상 계산식
        b = (xmin + ymax)/2 # 낙상 임계값
        if a >= b:
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), RED, 2)
            cv2.putText(frame, 'FALL DETECT', (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)
            print('FALL DETECT')
            continue
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
        cv2.putText(frame, 'Person'+' '+str(round(confidence, 2)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)
        print(xmin, ymin, xmax, ymax)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
