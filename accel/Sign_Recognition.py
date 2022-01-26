#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Steve
#
# Created:     19/01/2022
# Copyright:   (c) Steve 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# import libraries
from vidgear.gears import CamGear
import cv2
import numpy as np
import time

Stop_cascade = cv2.CascadeClassifier('Stop_classificateur.xml')
Pieton_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

#stream = CamGear(source='https://youtu.be/Nbira-ZTPq0', stream_mode = True, logging=True).start() # YouTube Video URL as input
stream = cv2.VideoCapture ("pane.mp4")
font = cv2.FONT_HERSHEY_SIMPLEX

# infinite loop
while True:
    ret, frame = stream.read()
    frame = cv2.resize(frame,(740,460))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # read frames

    # check if frame is None
    if frame is None:
        #if True break the infinite loop
        break

    stop = Stop_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in stop:
        cv2.putText (frame, "Stop",(x,y),
                font, 1,
                (0,255,0),
                2,
                cv2.LINE_4)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        stop = frame[y:y+h, x:x+w]
        print("Lewis, stop the car")
        cv2.imshow('panneau STOP', stop)

    # Car detection
    pieton = Pieton_cascade.detectMultiScale(gray, 1.3, 3)
    for (x,y,w,h) in pieton:
        cv2.putText (frame, "Pieton", (x,y),
                font, 1,
                (0,255,0),
                2,
                cv2.LINE_4)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        pieton = frame[y:y+h, x:x+w]
        print("Pieton")
        cv2.imshow('Pieton devant', pieton)

    cv2.imshow("Output Frame", frame)
    # Show output window

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        #if 'q' key-pressed break out
        break

cv2.destroyAllWindows()
# close output window

# safely close video stream.
stream.stop()