import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime=0
cTime=0

while True:
    success,img = cap.read()
    imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
              #print(id,lm)
              h,w,c = img.shape
              cx,cy = int(lm.x*w),int(lm.y*h)
              print(id,cx,cy)
              if id==0:
                cv.circle(img,(cx,cy),15,(255,0,255),-1)

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    img = cv.flip(img,1)
    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv.imshow("Image",img)
    cv.waitKey(1)

cap.release()