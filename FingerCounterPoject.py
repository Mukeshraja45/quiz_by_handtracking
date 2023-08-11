import cv2 as cv
import numpy as np
import time
import os
import HandTrackingModule as htm

width,height = 640,480

cap = cv.VideoCapture(0)

cap.set(3,width)
cap.set(4,height)

cTime,pTime = 0,0

detector = htm.handDetector()

tipIds = [4,8,12,16,20]

while True:

    success,img = cap.read()
    # img=cv.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    # print(lmList)
    if len(lmList)!=0:
        fingers = []
        if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2] and lmList[tipIds[id]][2]<lmList[tipIds[id]-1][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        cv.rectangle(img,(20,225),(170,425),(0,255,0),-1)
        cv.putText(img,str(totalFingers),(45,375),cv.FONT_HERSHEY_PLAIN,10,(255,0,0),25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img,f"FPS:{int(fps)}",(400,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv.imshow('Image',img)
    cv.waitKey(1)
cap.release()