import cv2
import time
import os
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480

cap.set(3, wCam)  ## 3 indicates width of the camera
cap.set(4, hCam)  ## 4 indicates height of the camera

folderpath = r"C:\Users\Yachna Hasija\PycharmProjects\HandTrackingProject\Finger_Images"

myList = os.listdir(folderpath)
print(myList)
overlaylist = []
for imgPath in myList:
    image = cv2.imread(f'{folderpath}\{imgPath}')
    # print(image[0])
#
#     # print(f'{folderpath}\{imgPath}')
    overlaylist.append(image)
print(overlaylist[0].shape)
pTime = 0
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]
while (True):
    success,img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw = False)
    # print(lmlist)
    if len(lmlist)!=0:
        fingers = []
        ## Thumb
        if lmlist[tipIds[0]][1] > lmlist[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        ## 4 Fingers
        for id in range(1,5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        h,w,c = cv2.resize(overlaylist[totalFingers-1],(150,150)).shape
        img[0:h, 0:w] =  cv2.resize(overlaylist[totalFingers-1],(150,150))

        cv2.rectangle(img, (20, 225), (170, 425), (0,255,0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),8)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS: {int(fps)}', (0,200), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),3)

    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

