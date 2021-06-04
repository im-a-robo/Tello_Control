from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
import sys

# Speed of the drone
S = 120
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
FPS = 60

class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations (yaw)
            - W and S: Up and down.
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        joystick_count=pygame.joystick.get_count()
        if joystick_count == 0:
        	# No joysticks!
            print ("Error, I didn't find any joysticks.")
            sys.exit()
        else:
        	# Use joystick #0 and initialize it
        	self.my_joystick = pygame.joystick.Joystick(0)
        	self.my_joystick.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False
        self.deadzone = 15

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

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

        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                        pygame.quit()
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            self.for_back_velocity = (self.get_joystick_power(self.my_joystick, 1) * -1)
            self.left_right_velocity = (self.get_joystick_power(self.my_joystick, 0))

            self.up_down_velocity = (self.get_joystick_power(self.my_joystick, 3) * -1)
            self.yaw_velocity = (self.get_joystick_power(self.my_joystick, 2))


            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            text_battery = "Battery: {}%".format(self.tello.get_battery())
            text_face_location_distance = "location {} distance {}".format(str(self.face_location), str(self.distance))
            
            cv2.putText(frame, text_battery, (5, 720 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, text_face_location_distance, (5, 720 - 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #TODO test if needed
            #frame = np.rot90(frame)
            #frame = np.flipud(frame)

            if self.face_detection_mode == True:
                self.face_detection(frame, face_cascade)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_1:  # land
            self.send_rc_control = False
            self.auton1()
            self.send_rc_control = True
        elif key == pygame.K_2:  # land
            self.send_rc_control = False
            self.auton2()
            self.send_rc_control = True
        elif key == pygame.K_f:
            self.face_detection_mode = not self.face_detection_mode

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            #not self.tello.land()
            self.tello.land()
            self.send_rc_control = False

    def get_joystick_power(self, joystick, axis):
        if abs(np.round((joystick.get_axis(axis) * S), 0)) < self.deadzone:
            power = 0
        else:
            power = np.round((joystick.get_axis(axis) * S), 0)

        return power

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)
    
    def face_detection(self, frame, face_cascade):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
            if type(faces) != tuple:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
                self.distance = (2 * 3.14 * 180) / (w + h * 360) * 1000 + 3 # in inches
                self.face_location = (x, y)
            else:
                print('no face detected')

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