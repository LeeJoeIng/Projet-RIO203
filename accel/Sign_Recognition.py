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
import datetime

Stop_cascade = cv2.CascadeClassifier('Stop_classificateur.xml')

#stream = CamGear(source='https://youtu.be/Nbira-ZTPq0', stream_mode = True, logging=True).start() # YouTube Video URL as input
stream = cv2.VideoCapture("pane.mp4")

if not stream.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

font = cv2.FONT_HERSHEY_SIMPLEX

temps = 0
temps_entier = 0
entier_precedent = 0
presence_stop = 0
tempsActuel = 0
t = 0.0
tempsPrecedent = 0
tabStop = []

t0 = time.time()


# infinite loop
while True:


    tempsActuel = time.time()
    ret, frame = stream.read()


    fps = 1/(tempsActuel-tempsPrecedent)
    multiplicateur = fps/30

    t_transition = tempsActuel-tempsPrecedent
    temps += (tempsActuel-tempsPrecedent)*multiplicateur
    temps

    tempsPrecedent = tempsActuel
    fps = int(fps)

    #print("temps : " + str(temps) + " fps : " + str(fps))

    if frame is None:
        print('--(!) No captured frame -- Break!')
        break


    if ret:
        frame = cv2.resize(frame,(720,480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.putText (frame, str(temps) + " : " + str(fps),(40,40),
        font, 1,
        (0,0,0),
        2,
        cv2.LINE_4)

        stop = Stop_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in stop:
            cv2.putText (frame, "Stop",(x,y),
                    font, 1,
                    (0,255,0),
                    2,
                    cv2.LINE_4)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            stop = frame[y:y+h, x:x+w]
            presence_stop = 1
            cv2.imshow('panneau STOP', stop)

        cv2.imshow("Output Frame", frame)
        # Show output window

        key = cv2.waitKey(1) & 0xFF
        # check for 'q' key-press
        if key == ord("q"):
            #if 'q' key-pressed break out
            break

        temps_entier = int(temps)
        if(entier_precedent != temps_entier):
            tabStop.append(presence_stop)
        entier_precedent = temps_entier





    presence_stop = 0

print(tabStop)
print(len(tabStop))
cv2.destroyAllWindows()
# close output window