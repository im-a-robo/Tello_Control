from cv2 import data
import pygame
import cv2
import sys
import numpy as np
from time import sleep
import os

fps = 5
pygame.init()

def color_masking():
    # define a video capture object
    vid = cv2.VideoCapture(0)

    cv2.namedWindow("Trackbars")

    def nothing(x):
        pass  
    f = open("color.txt", "r")

    l_h = f.readline()
    l_s = f.readline()
    l_v = f.readline()
    u_h = f.readline()
    u_s = f.readline()
    u_v = f.readline() 

    f.close()

    cv2.createTrackbar("L-H", "Trackbars", int(l_h), 179, nothing)
    cv2.createTrackbar("L-s", "Trackbars", int(l_s), 255, nothing)
    cv2.createTrackbar("L-v", "Trackbars", int(l_v), 255, nothing)
    cv2.createTrackbar("U-H", "Trackbars", int(u_h), 179, nothing)
    cv2.createTrackbar("U-S", "Trackbars", int(u_s), 255, nothing)
    cv2.createTrackbar("U-V", "Trackbars", int(u_v), 255, nothing)

    while(True):
        sleep(1 / fps)

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        l_h = cv2.getTrackbarPos("L-H", "Trackbars")
        l_s = cv2.getTrackbarPos("L-s", "Trackbars")
        l_v = cv2.getTrackbarPos("L-v", "Trackbars")
        u_h = cv2.getTrackbarPos("U-H", "Trackbars")
        u_s = cv2.getTrackbarPos("U-S", "Trackbars")
        u_v = cv2.getTrackbarPos("U-V", "Trackbars")

        # Color masking
        low_HSV = np.array([l_h, l_s, l_v])
        high_HSV = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv_frame, low_HSV, high_HSV)
        #mask = cv2.bitwise_and(frame, frame, mask = mask)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        cv2.imshow("Red", mask)

        # if escape is pressed break the loop
        if cv2.waitKey(1) == 27:
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    move_on  = input("would you like to wirte these values. y/n: ")

    if move_on == "y":
        f = open("color.txt", "w")
        f.write("{}\n{}\n{}\n{}\n{}\n{}".format(str(l_h), str(l_s), str(l_v), str(u_h), str(u_s), str(u_v)))
        f.close()
    elif move_on == "n":
        print("ok then")


def face_detection_all():  
    x, y, w, h = 0, 0, 0, 0

    location_bool = False

    # define a video capture object
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    vid = cv2.VideoCapture(0)

    while(True):

        sleep(1 / fps)

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        text_location = ''
        text_distance = ''

        face_location = (0, 0)

        if type(faces) != tuple:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
                distance = (2 * 3.14 * 180) / (w + h * 360) * 1000 + 5
            face_location = (x, y)
            text_location = "location {}".format(str(face_location))
            text_distance = "distance {}".format(str(round(distance, 0)))
        else:
            print('no face detected')

        if text_distance != '' and text_location != '': 
            cv2.putText(frame, text_location, (5, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, text_distance, (5, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('frame', frame)


        if (y > 250 and y != 0) and (x > 250 and x != 0):
            location_bool = True
        else:
            location_bool = False

        # if escape is pressed break the loop
        if cv2.waitKey(1) == 27:
            break


    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def face_detection_one():  
    x, y, w, h = 0, 0, 0, 0

    location_bool = False

    # define a video capture object
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    vid = cv2.VideoCapture(0)

    while(True):

        sleep(1 / fps)

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if type(faces) != tuple:
            one_faces = faces[0]
            x = one_faces[0]
            y = one_faces[1]
            w = one_faces[2]
            h = one_faces[3]
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
            print(location_bool)
        else:
            print('no face detected')

        # Display the resulting frame
        cv2.imshow('frame', frame)


        if (y > 150 and y != 0) and (x > 150 and x != 0):
            location_bool = True
        else:
            location_bool = False

        # if escape is pressed break the loop
        if cv2.waitKey(1) == 27:
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

def picture_taker():
    vid = cv2.VideoCapture(0)
    img_count = 1

    joystick_count=pygame.joystick.get_count()
    if joystick_count == 0:
    	# No joysticks!
        print ("Error, I didn't find any joysticks.")
    else:
    	# Use joystick #0 and initialize it
    	my_joystick = pygame.joystick.Joystick(0)
    	my_joystick.init()

    os.chdir('C:/Users/Ndas1/Code/Tello_Control/pictures/n')
    while(True):

        sleep(1 / fps)

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        cv2.imshow("frame", frame)
        if my_joystick.get_button(0) == 1:
            cv2.imwrite("facepic{}.png".format(str(img_count)), frame)
            print(img_count)
            img_count += 1

        # if escape is pressed break the loop
        if cv2.waitKey(1) == 27:
            break
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

picture_taker()