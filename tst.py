import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
# from computer_vision_python.Serialconn import Serial_object
# import serial
import time
data = ""
# arduino = serial.Serial('com4')
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(1920, 1080, [20, 50], invert=True)

idListL = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
idListR = [252, 256, 253, 254, 339, 255, 359, 388, 387, 386, 385, 384,463]
ratioListL = []
ratioListR = []

blinkCounterR = 0
blinkCounterL = 0
counterL = 0
counterR = 0
blinkCounterL = 0
counterL = 0
color = (0,0,255)
statusL = ""
statusR = ""
# arduino.baudrate = 9600  # set Baud rate to 9600
# arduino.bytesize = 8     # Number of data bits = 8
# arduino.parity   ='N'    # No parity
# arduino.stopbits = 1  
time.sleep(3)
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for idL in idListL:
            cv2.circle(img, face[idL], 1,(0,255,0), cv2.FILLED)
        
        for idR in idListR:
            cv2.circle(img, face[idR], 1,(255,0,0), cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        
        rightUp = face[386]
        rightDown = face[253]
        rightLeft = face[463]
        rightRight = face[359]
        
        rightVer, _ = detector.findDistance(rightUp, rightDown)
        rightHor, _ = detector.findDistance(rightLeft, rightRight)
        
        leftVer, _ = detector.findDistance(leftUp, leftDown)
        leftHor, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, (0, 0, 255), 1)
        cv2.line(img, leftLeft, leftRight, (0, 0, 255), 1)
        
        cv2.line(img, rightUp, rightDown, (0, 0, 255), 1)
        cv2.line(img, rightLeft, rightRight, (0, 0, 255), 1)

        ratioL = int((leftVer / leftHor) * 100)
        # print(ratio)
        ratioListL.append(ratioL)
        if len(ratioListL) > 3:
            ratioListL.pop(0)
        ratioAvgL = sum(ratioListL) / len(ratioListL)

        if ratioAvgL < 35 and counterL == 0:
            blinkCounterL += 1
            color = (0,0,255)
            counterL = 1
            statusL = "Closed"
            # arduino.send('1')
        if counterL != 0:
            counterL += 1
            if counterL > 10:
                counterL = 0
                color = (0,255, 0)
                statusL = "Open"
                # arduino.send('1')
        
        
        cvzone.putTextRect(img, f'Eye: {statusL} ', (50, 100),
                           colorR=color)
        ratioR = int((rightVer / rightHor) * 100)
        # print(ratio)
        ratioListR.append(ratioR)
        if len(ratioListR) > 3:
            ratioListR.pop(0)
        ratioAvgR = sum(ratioListR) / len(ratioListR)

        if ratioAvgR < 35 and counterR == 0:
            blinkCounterR += 1
            color = (0,0,255)
            counterR = 1
            statusR = "Closed"
            # arduino.send('1')
        if counterR != 0:
            counterR += 1
            if counterR > 10:
                counterR = 0
                color = (0,255, 0)
                statusR = "Open"
                # arduino.send('1')
        
        
        cvzone.putTextRect(img, f'Eye: {statusR} ', (50, 300),
                           colorR=color)

        imgPlot = plotY.update(ratioAvgL, color)
        img = cv2.resize(img, (1920, 1080))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
        val = str(blinkCounterL%2)
        
        if val == "0" :
            data = b'A'
        else:
            data = b'B'

        # time.sleep(2)
        print(data)
        # arduino.write(data)
    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("Image", img)
    cv2.waitKey(25)
arduino.close()