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

def get_joystick_power(joystick, axis):
    global max_speed
    if abs(np.round((joystick.get_axis(axis) * max_speed), 1)) < 20:
        power = 0
    else:
        power = np.round((joystick.get_axis(axis) * max_speed), 1)

    return power

joystick_count=pygame.joystick.get_count()
if joystick_count == 0:
	# No joysticks!
    print ("Error, I didn't find any joysticks.")
else:
	# Use joystick #0 and initialize it
	my_joystick = pygame.joystick.Joystick(0)
	my_joystick.init()

print_ary = []
should_stop = False
while not should_stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_stop = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                should_stop = True

    print_ary.append(("left_X_axis {} left_Y_axis {} right_X_axis {} right_Y_axis {}".format(get_joystick_power(my_joystick, 0), 
                                                                                 get_joystick_power(my_joystick, 1) * -1, 
                                                                                 get_joystick_power(my_joystick, 2), 
                                                                                 get_joystick_power(my_joystick, 3) * -1)))

    print(print_ary)

    print_ary.pop(0)

    time.sleep(0.05)