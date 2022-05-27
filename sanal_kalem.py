#!/usr/bin/env python3
import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
#HSV    
renklerHSV =[[0 ,100,20 ,10 ,255,255], #kırmızı
           [100,150,0 ,140,255,255], #mavi
           [100,100,100,140,255,255], #yeşil
           [40 ,100,100,80 ,255,255]] #sarı

renkler = [[0 ,0 ,255],          ## BGR
                 [255,0 ,0 ],
                 [0 ,255,0 ],
                 [255,255,0]]

pts =  []  ## [x , y , colorId ]

def findColor(img,renklerHSV,renkler):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    pts2=[]
    for color in renklerHSV:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),15,renkler[count],-1)
        if x!=0 and y!=0:
            pts2.append([x,y,count])
        count +=1
        
    return pts2

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(pts,renkler):
    for point in pts:
        cv2.circle(imgResult, (point[0], point[1]), 10, renkler[point[2]], -1)


while True:

    success, img = cap.read()
    imgResult = img.copy()
    pts2 = findColor(img, renklerHSV,renkler)
    if len(pts2)!=0:
        for pt2 in pts2:
            pts.append(pt2)
    if len(pts)!=0:
        drawOnCanvas(pts,renkler)


    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break