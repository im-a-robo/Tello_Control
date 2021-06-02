from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
import sys

'''
bottom of stick = 1
top of stick = -1

right of stick = 1
left of stick = -1

left stick x-axis = axis 0 
left stick y-axis = axis 1

right stick x-axis = axis 2
right stick y-axis = axis 3
'''

pygame.init()

max_speed = 120

joystick_count=pygame.joystick.get_count()
if joystick_count == 0:
	# No joysticks!
    print ("Error, I didn't find any joysticks.")
else:
	# Use joystick #0 and initialize it
	my_joystick = pygame.joystick.Joystick(0)
	my_joystick.init()

should_stop = False
while not should_stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_stop = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                should_stop = True

    print("axis1 {} axis2 {}".format(np.round((my_joystick.get_axis(2) * max_speed), 1), np.round((my_joystick.get_axis(3) * max_speed), 1)))

    time.sleep(0.05)