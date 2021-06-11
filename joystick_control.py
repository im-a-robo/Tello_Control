from djitellopy import Tello
import cv2
import numpy as np
from inputs import get_gamepad
import time
import sys

# Speed of the drone
S = 120
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
FPS = 60

class FrontEnd(object):
    def __init__(self):
        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

    def run(self):

        self.tello.connect()
        self.tello.set_speed(self.speed)

        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        self.face_detection_mode = False
        self.face_location = (0, 0)
        self.distance = 0
        self.face_located = True
        self.moveing_distance = 0

        #TODO make function
        self.should_stop = False
        while not self.should_stop:
            events = get_gamepad()
            for event in events:
                if not event.ev_type == "Sync":
                    if event.code == 'ABS_Y':
                        for_back_velocity = self.scale_js(int(event.state))
                    if event.code == 'ABS_X':
                        left_right_velocity = self.scale_js(int(event.state))
                    if event.code == 'ABS_RY':
                        up_down_velocity = self.scale_js(int(event.state))
                    if event.code == 'ABS_RX':
                        yaw_velocity = self.scale_js(int(event.state))
                    if event.code == 'BTN_TL' and event.state == 1:
                        self.tello.flip_left()
                    if event.code == 'BTN_TR' and event.state == 1:
                        self.tello.flip_right()
                    if event.code == 'BTN_SELECT' and event.state == 1:
                        self.tello.takeoff()
                        self.send_rc_control = True
                    if event.code == 'BTN_START' and event.state == 1:
                        self.tello.land()
                        self.send_rc_control = False
                    if event.code == 'BTN_NORTH' and event.code == 1:
                        self.face_detection_mode == True

            # #TODO make function
            # if self.face_located and self.face_detection_mode:
            #     if self.face_location[0] < 360:
            #         self.yaw_velocity = -(S / 4)
            #     elif self.face_location[0] > 600:
            #         self.yaw_velocity = (S / 4)
            #     elif self.face_location[0] > 360 and self.face_location[0] < 600:
            #         self.yaw_velocity = 0
            #         if self.distance > 30:
            #             self.difference = float(self.distance - 30)
            #             self.moveing_distance = int(round(self.difference * 2.54, 0))
            #             self.tello.move_forward(self.moveing_distance)
            #         else:
            #             self.for_back_velocity = 0
            # elif not self.face_located:
            #     self.moveing_distance = 0

            if frame_read.stopped:
                break

            raw_frame = frame_read.frame

            if self.face_detection_mode == True:
                self.face_detection(raw_frame, face_cascade)

            display_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

            text_battery = "Battery: {}%".format(self.tello.get_battery())
            text_face_location_distance = "location {} distance {}".format(str(self.face_location), str(self.distance))
            cv2.putText(display_frame, text_battery, (5, 720 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(display_frame, text_face_location_distance, (5, 720 - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Tello Display", display_frame)

            if self.send_rc_control:
                self.tello.send_rc_control(int(self.left_right_velocity), int(self.for_back_velocity), int(self.up_down_velocity), int(self.yaw_velocity))

            #TODO See if removing provides faster input 
            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def scale_js(self, val):
        inputRange = 32768 - (-32767)
        outputRange = 100 - (-100)
        val = int((val - (-32767)) * outputRange / inputRange + (-100))
        return val if abs(val) > 30 else 0
    
    def face_detection(self, frame, face_cascade):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
        if type(faces) != tuple:
            for (x, y, w, h) in faces:
                one_face = faces[0]
                x = one_face[0]
                y = one_face[1]
                w = one_face[2]
                h = one_face[3]
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
            self.distance = round(((2 * 3.14 * 180) / (w + h * 360) * 1000 + 5), 0) # in inches
            self.face_location = (x, y)
            self.face_located = True
        else:
            print('no face detected')
            self.face_located = False

    def auton1(self):
        self.tello.move_forward(30)
        time.sleep(0.15)
        self.tello.rotate_clockwise(90)
        time.sleep(0.15)
        self.tello.move_forward(30)
    
    def auton2(self):
        self.tello.move_forward(30)
        time.sleep(0.15)
        self.tello.rotate_counter_clockwise(360)
        time.sleep(0.15)
        self.tello.flip_left()
        time.sleep(0.15)
        self.tello.flip_right()

def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()