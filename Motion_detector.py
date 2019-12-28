import pandas as pd
import cv2,time
from datetime import datetime

first_f=None
status_list=[None,None]
times=[]
df = pd.DataFrame(columns=["start","end"])
vid = cv2.VideoCapture(0)

while True:
    state,frame=vid.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if first_f is None:
        first_f= gray
        continue
    delf = cv2.absdiff(first_f, gray)
    threshold = cv2.threshold(delf, 30, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=0)
    cnts,heir = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 3)
        status = 1
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow('Capturing', gray)
    cv2.imshow('delta', delf)
    cv2.imshow('Threshold', threshold)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({"start": times[i], "end": times[i + 1]}, ignore_index=1)

df.to_csv("Times.csv")


vid.release()
cv2.destroyAllWindows()