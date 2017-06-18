import cv2
import sys
import cv2 as cv
import numpy as np
import math as m

# Usage:
# tune.py cameraNumber / colorSpace / (defaultLowValues, defaultHighValues)

colorSpace = "rgb"
lowVal = (0, 0, 0)
highVal = (255, 255, 255)
if len(sys.argv) > 1:
    camera = cv2.VideoCapture(str(sys.argv[1]))
    if len(sys.argv) > 2:
        cS = sys.argv[2]
        if cS == "hsv":
            colorSpace = "hsv"
        if len(sys.argv) > 3:
            lowVal = sys.argv[3][0]
            highVal = sys.argv[3][1]
        else:
            if colorSpace == "hsv":
                highVal = (180, 255, 255)
else:
    camera = cv2.VideoCapture(0)

values = [0, 180, 0, 255, 0, 255]


def callback(idNumber, value):
    global values
    values[idNumber - 1] = value

def callback1(value): callback(1, value)
def callback2(value): callback(2, value)
def callback3(value): callback(3, value)
def callback4(value): callback(4, value)
def callback5(value): callback(5, value)
def callback6(value): callback(6, value)


cv2.namedWindow("Trackbars", 0)

if colorSpace == "hsv":
    cv2.createTrackbar("lowHue", "Trackbars", values[0], 181, callback1)
    cv2.createTrackbar("highHue", "Trackbars", values[1], 181, callback2)
    cv2.createTrackbar("lowSat", "Trackbars", values[2], 256, callback3)
    cv2.createTrackbar("highSat", "Trackbars", values[3], 256, callback4)
    cv2.createTrackbar("lowVib", "Trackbars", values[4], 256, callback5)
    cv2.createTrackbar("highVib", "Trackbars", values[5], 256, callback6)
else:
    cv2.createTrackbar("lowBlue", "Trackbars", values[0], 256, callback1)
    cv2.createTrackbar("highBlue", "Trackbars", values[1], 256, callback2)
    cv2.createTrackbar("lowGreen", "Trackbars", values[2], 256, callback3)
    cv2.createTrackbar("highGreen", "Trackbars", values[3], 256, callback4)
    cv2.createTrackbar("lowRed", "Trackbars", values[4], 256, callback5)
    cv2.createTrackbar("highRed", "Trackbars", values[5], 256, callback6)

while True:
    (grabbed, frame) = camera.read()
    # cv2.imshow("testing",frame)
    mask = cv2.inRange(frame, (values[0], values[2], values[4]), (values[1], values[3], values[5]))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=False)
        cnt = None
        # Replace Below with your code
        if True:
            for e in cnts:
                M = cv2.moments(e)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.line(frame, (cx, cy), (cx, cy), (255, 0, 255), 20)
                x, y, w, h = cv2.boundingRect(e)
                if cv2.contourArea(e) > 400:
                    cnt = e
            if cnt is not None:
                x, y, w, h = cv2.boundingRect(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame, [box], 0, (255, 0, 0), 2)
                hull = cv2.convexHull(cnt)
                cv2.drawContours(frame, [hull], 0, (255, 255, 0), 4)
        #Replace Above with your code
    cv2.drawContours(frame, cnts, -1, (0, 0, 255), 3)
    frame = cv2.resize(frame, (320, 240))
    mask = cv2.resize(mask, (320, 240))
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
camera.release()
