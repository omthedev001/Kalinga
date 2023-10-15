import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
# from computer_vision_python.Serialconn import Serial_object
import serial
import time
data = ""
arduino = serial.Serial('com4')
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50], invert=True)

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (0,0,255)
status = ""
arduino.baudrate = 9600  # set Baud rate to 9600
arduino.bytesize = 8     # Number of data bits = 8
arduino.parity   ='N'    # No parity
arduino.stopbits = 1  
time.sleep(3)
while True:


    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 1,(0,255,0), cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, (0, 0, 255), 1)
        cv2.line(img, leftLeft, leftRight, (0, 0, 255), 1)

        ratio = int((lenghtVer / lenghtHor) * 100)
        # print(ratio)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0,0,255)
            counter = 1
            status = "Closed"
            # arduino.send('1')
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (0,255, 0)
                status = "Open"
                # arduino.send('1')
        
        
        cvzone.putTextRect(img, f'Eye: {status} ', (50, 100),
                           colorR=color)

        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
        val = str(blinkCounter%2)
        
        if val == "0" :
            data = b'A'
        else:
            data = b'B'

        # time.sleep(2)
        print(data)
        arduino.write(data)
    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("Image", imgStack)
    cv2.waitKey(25)
arduino.close()