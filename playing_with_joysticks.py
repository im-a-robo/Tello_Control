import cv2
from inputs import get_gamepad
import numpy as np
import time
import sys

'''
left stick x = ABS_X
left stick y = ABS_Y
right stick x = ABS_RX
right stick y = ABS_RY

left bumber = BTN_TL 1 Key or BTN_TL 0 Key
right bumber = BTN_TR 1 Key or BTN_TR0Key

left trigger = ABS_Z[0-255] Absolute
right trigger = ABS_RZ[0-255] Absolute

left stick button down = BTN_THUMBL 1 Key or BTN_THUMBL 0 Key
right stick button down = BTN_THUMBR 1 Key or BTN_THUMBR 0 Key

D-pad up = ABS_HAT0Y -1 Absolute or ABS_HAT0Y 0 Absolute
D-pad down = ABS_HAT0Y 1 Absolute or ABS_HAT0Y 0 Absolute
D-pad left = ABS_HAT0X -1 Absolute or ABS_HAT0X 0 Absolute
D-pad right = ABS_HAT0X 1 Absolute ABS_HAT0X 0 Absolute

start button = BTN_SELECT 1 Key or BTN_SELECT 0 Key
select button = BTN_START 1 Key or BTN_START 0 Key
 
button A = BTN_SOUTH 1Key or BTN_SOUTH 0 Key
button B = BTN_EAST 1Key or BTN_EAST 0 Key
button X = BTN_WEST 1Key or BTN_WEST 0 Key
button Y = BTN_NORTH 1Key or BTN_NORTH 0 Key

'''

fps = 240


max_speed = 120


def scale_js(val):
    inputRange = 32768 - (-32767)
    outputRange = 100 - (-100)
    val = int((val - (-32767)) * outputRange / inputRange + (-100))
    return val if abs(val) > 30 else 0

left_stickX_val = 0
left_stickY_val = 0
right_stickX_val = 0
right_stickY_val = 0

while 1:
    events = get_gamepad()

    for event in events:
        if not event.ev_type == "Sync":
                if event.code == 'ABS_Y':
                    left_stickY_val = scale_js(int(event.state))
                if event.code == 'ABS_X':
                    left_stickX_val = scale_js(int(event.state))
                if event.code == 'ABS_RY':
                    right_stickY_val = scale_js(int(event.state))
                if event.code == 'ABS_RX':
                    right_stickX_val = scale_js(int(event.state))
    
        print("left_stickX_val {} left_stickY_val {} right_stickX_val {} right_stickY_val {}".format(left_stickX_val, left_stickY_val, right_stickX_val, right_stickY_val))