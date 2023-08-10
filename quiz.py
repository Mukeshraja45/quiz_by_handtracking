import numpy as np
import cv2 as cv
from collections import defaultdict
import pyautogui
import HandTrackingModule as htm
import time

import mediapipe as mp 
from google.protobuf.json_format import MessageToDict

mpHands = mp.solutions.hands 
hands = mpHands.Hands()


width, height = pyautogui.size()

detector = htm.handDetector()

tipIds = [4,8,12,16,20]

def createques(ques_list,no_ques):
    width, height = pyautogui.size()
    width = width//2-60
    height = height-60

    for i,(ques,ans) in enumerate(ques_list.items()):
        img = np.zeros([height,width,3],dtype="uint8")
        for k in range(height):
            for j in range(width):
                img[k][j] = (255,255,255)
        cv.rectangle(img,(0,40),(width,200),(187,200,200),-1)
        cv.putText(img,f"Question-{i+1}:",(0,30),cv.FONT_HERSHEY_SIMPLEX,0.7,(245,9,169),2)
        cv.putText(img,f"{ques}",(0,100),cv.FONT_HERSHEY_SIMPLEX,0.7,(245,9,169),2)
        cv.putText(img,f"a){ans[0]}",(10,300),cv.FONT_HERSHEY_SIMPLEX,1,(245,9,169),2)
        cv.putText(img,f"b){ans[1]}",(10,500),cv.FONT_HERSHEY_SIMPLEX,1,(245,9,169),2)
        cv.putText(img,f"c){ans[2]}",(10,700),cv.FONT_HERSHEY_SIMPLEX,1,(245,9,169),2)
        cv.putText(img,f"d){ans[3]}",(10,900),cv.FONT_HERSHEY_SIMPLEX,1,(245,9,169),2)
        cv.imshow("img",img)
        st = "questions/"+str(i+1)+".jpg"
        cv.imwrite(st,img)
        print(f"Image{i+1} created")
        cv.waitKey(0)

cap = cv.VideoCapture(0)
cap.set(3,640) #width
cap.set(4,480) #height

imageBackground = cv.imread("Background.jpg")

no_ques = int(input("How many questions do you have the students to answer?"))
ques_list=defaultdict(list)
q = list()
correct_ans = list()
for i in range(no_ques):
    ques = input("Enter the question=")
    q.append(ques)
    for j in range(4):
        ans = input("Enter answer for the question=")
        ques_list[ques].append(ans)
    correct = int(input("Enter correct option-1,2,3,4="))
    ques_list[ques].append(correct)

# createques(ques_list,no_ques)

for key,value in ques_list.items():
    print(key,value)

print(q)
current_ques = 0
draw=False
which_place = 0
count_correct = 0
color = (0,0,0)
counter = 0
set_val = True
totalFingers=0
rcounter = 0
set_rcounter = False
lcounter=0
set_lcounter=False

li = [i for i in range(no_ques)]

while True:
    sucess,img = cap.read()
    img = cv.flip(img,1)

    imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    if(rcounter>=40):
        current_ques+=1
        if(current_ques>=no_ques):
            current_ques=0 
        set_rcounter = False
        rcounter = 0
    # if(lcounter>=80):
    #     current_ques-=1
    #     if(current_ques<0):
    #         current_ques=no_ques-1 
    #     set_lcounter = False
    #     lcounter = 0

    if results.multi_hand_landmarks:
        if(len(results.multi_handedness)==2):
            cv.putText(img,'BOTH HANDS',(250,250),cv.FONT_HERSHEY_PLAIN,0.9,(0,255,0),2)
            continue

        else:
            for i in results.multi_handedness:
                label = MessageToDict(i)['classification'][0]['label']
                # print(label,type(label),label=="Right")
                # print(MessageToDict(i),MessageToDict(i)['classification'])
                if label == 'Left':
                    cv.putText(img,'Left',(10,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
                    img = detector.findHands(img,draw=False)
                    
                    lmList = detector.findPosition(img)
                    if len(lmList)!=0:
                        # print(lmList[8][2] , lmList[8][1])
                        if 0<=lmList[8][2]<=50 and 60<=lmList[8][1]<=220:
                            # current_ques+=1
                            set_rcounter = True
                            # if(current_ques>=no_ques):
                            #     current_ques=0

                        # if 0<=lmList[8][2]<=50 and 400<=lmList[8][1]<=560:
                        #     set_lcounter = True
                            
                if label == "Right":
                    # cv.putText(img,'Right',(250,250),cv.FONT_HERSHEY_PLAIN,0.9,(0,255,0),2)
    
                    img = detector.findHands(img)
                    
                    lmList = detector.findPosition(img)
                    print(lmList)
                    if len(lmList)!=0:
                        fingers = []
                        # if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
                        #     fingers.append(1)
                        # else:
                        #     fingers.append(0)
                        for id in range(1,5):
                            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2] and lmList[tipIds[id]][2]<lmList[tipIds[id]-1][2]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                        # print(fingers)
                        totalFingers = fingers.count(1)
                        # print(totalFingers,ques_list[q[current_ques]][4])
                        try:
                            if(current_ques not in correct_ans and set_val and current_ques<no_ques and (totalFingers!=0 and totalFingers<5) and ques_list[q[current_ques]][4]==totalFingers and not set_rcounter):
                                color = (0,255,0)
                                draw = True
                                count_correct +=1
                                counter=0
                                set_val=False
                                correct_ans.append(current_ques)
                                li.remove(current_ques)
                                # current_ques+=1
                                if totalFingers==1:
                                    which_place=300
                                elif totalFingers==2:
                                    which_place=500
                                elif totalFingers==3:
                                    which_place=700
                                else:
                                    which_place=900
                            elif(current_ques not in correct_ans and set_val and current_ques<no_ques and ques_list[q[current_ques]][4]!=totalFingers and 1<=totalFingers<=4  and (not set_rcounter)):
                                color = (0,0,255)
                                draw = True
                                counter=0
                                set_val=False
                                correct_ans.append(current_ques)
                                li.remove(current_ques)
                                if totalFingers==1:
                                    which_place=300
                                elif totalFingers==2:
                                    which_place=500
                                elif totalFingers==3:
                                    which_place=700
                                else:
                                    which_place=900
                        except Exception as e:
                            print(e)
                        cv.rectangle(img,(20,225),(170,425),(0,255,0),-1)
                        cv.putText(img,str(totalFingers),(45,375),cv.FONT_HERSHEY_PLAIN,10,(255,0,0),25)

    imgCanvas = cv.imread("Nextpre.jpg")
    imgGray = cv.cvtColor(imgCanvas,cv.COLOR_BGR2GRAY)
    _,imgInv = cv.threshold(imgGray,50,255,cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv,cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img,imgInv)
    img = cv.bitwise_or(img,imgCanvas)
    imageBackground[280:280+480,160:160+640]=img
    im = cv.imread("questions/end.jpg")
    cv.putText(im,str(count_correct),(500,300),cv.FONT_HERSHEY_PLAIN,5,(255,0,0),7)
    try:
        if(current_ques>=no_ques and len(li)!=0):
            current_ques=li[0]
        if(current_ques<no_ques and len(correct_ans) == no_ques and (len(li)==0)):
            im = cv.imread("questions/end.jpg")
            cv.putText(im,str(count_correct),(500,300),cv.FONT_HERSHEY_PLAIN,5,(255,0,0),7)
        elif(current_ques<no_ques):
            st = "questions/"+str(current_ques+1)+".jpg"
            # print(st)
            try:
                im = cv.imread(st)
            except Exception as e:
                print(e)
            if draw and not set_rcounter:
                cv.line(im,(5,which_place-10),(15,which_place),color,5)
                cv.line(im,(15,which_place),(35,which_place-30),color,5)
        

    except Exception as e:
        print(e)
    try:
        imageBackground[20:20+1020,30+(width//2):30+(width//2)+900]=im
        
    except Exception as e:
        print(e)

    if draw and counter==40:
        draw=False
        current_ques+=1
        # print(current_ques,counter,draw)
        set_val=True
        color=(0,0,0)
    if draw==False or (counter<40 and draw):
        counter+=1
    if set_rcounter:
        rcounter+=1
    # if set_lcounter:
    #     lcounter+=1
    print("rcounter=",rcounter,correct_ans,li)
    # print("counter=",counter,draw,current_ques,no_ques)
    cv.imshow("Image",imageBackground)
    cv.waitKey(1)

cap.release()