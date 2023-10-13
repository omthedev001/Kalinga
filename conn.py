import serial
# import tkinter
import time




device = serial.Serial('com4',9600)
class  arduino():
 
    def send(msg):
        msg = msg + '\r'
        device.write(msg.encode())
while True:
    arduino.send("OFF")