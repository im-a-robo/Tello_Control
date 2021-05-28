from djitellopy import Tello
import pygame
import threading
from time import sleep

tello = Tello()

tello.connect()
#tello.streamon()
#frame_read = tello.get_frame_read()

tello.takeoff()

sleep(10)

tello.land()
