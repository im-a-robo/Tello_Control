import pygame
import cv2
import sys
import numpy as np

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


color_masking()