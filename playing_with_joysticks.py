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

button0 =  
button1 = 
button2 = 
button3 = 
button4 = 
button5 = 
button6 = 
button7 = 
button8 = 
button9 = 
'''

pygame.init()

max_speed = 120

def get_joystick_power(joystick, axis):
    global max_speed
    if abs(np.round((joystick.get_axis(axis) * max_speed), 0)) < 15:
        power = 0
    else:
        power = np.round((joystick.get_axis(axis) * max_speed), 0)

    return power

def get_joystick_button_state(joystick, button):
    return joystick.get_button(button)

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                should_stop = True

    print(("left_X_axis {} left_Y_axis {} right_X_axis {} right_Y_axis {}".format(get_joystick_power(my_joystick, 0), 
                                                                                 get_joystick_power(my_joystick, 1) * -1, 
                                                                                 get_joystick_power(my_joystick, 2), 
                                                                                 get_joystick_power(my_joystick, 3) * -1)))


    # print("button0 {} button1 {} button2 {} button3 {} button4 {} button5 {} button6 {} button7 {} button8 {} button9 {} button10 {} button11 {} button12 {} button13 {} button14 {} button15 {}".format(get_joystick_button_state(my_joystick, 0),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 1), 
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 2),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 3),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 4),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 5),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 6),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 7),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 8),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 9),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 10),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 11),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 12),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 13),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 14),
    #                                                                                                                                                                                                                   get_joystick_button_state(my_joystick, 15)))

    time.sleep(0.05)