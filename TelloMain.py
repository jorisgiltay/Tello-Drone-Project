from utils import *
import cv2
import pygame
import time

#Initialize Variables
pid = [0.5, 0.5, 0]
startCounter = 0 # NO FLIGHT = 1, FLIGHT = 0
up_down, yaw, forward_backward, left_right = 0, 0, 0, 0
flying, take_off, land, show_frame = False, False, False, False
w, h = 360, 240
pError = 0.0
i = 0
k = 0
img, pictures, trackedfaces = [], [], []

#Initialize Pygame and Joystick
pygame.init()
Joysticks = init_joysticks()
XBox_360 = Joysticks[0]

#Initialize Drone
giltayDrone = initializeTello()
giltayDrone.streamon()
telloGetFrame(giltayDrone,1080, 720)

while True:
    for event in pygame.event.get():  # User did something.
        if event.type == pygame.JOYBUTTONDOWN:
            [take_off, land, show_frame] = joystick_get_buttons(XBox_360)
        if event.type == pygame.JOYAXISMOTION:
            [yaw, up_down, left_right, forward_backward] = joystick_get_axes(XBox_360)

    if take_off is 1 and flying == False:
        print('take_off')
        response = giltayDrone.takeoff()
        flying = True


    if land is 1 and flying == True:
        print('land')
        giltayDrone.land()
        flying = False
        for images in pictures:
            img_name = "Pictures/picture" + str(i) + ".jpg"
            cv2.imwrite(img_name,pictures[i])
            i = i + 1
        for faces in trackedfaces:
            tracked_img_name = "TrackedFaces/trackedface" + str(k) + ".jpg"
            cv2.imwrite(tracked_img_name, trackedfaces[k])
            k = k+1

    giltayDrone.send_rc_control(left_right_velocity= left_right,
                                up_down_velocity= up_down,
                                forward_backward_velocity= forward_backward,
                                yaw_velocity= yaw)

    time.sleep(0.001)
    img = telloGetFrame(giltayDrone, 360, 240)
    trackedFace = findFace(img)
    if (trackedFace is not None):
        trackedfaces.append(trackedFace)


    if show_frame == 1:
        print("TOOK PICTURE")
        show_frame = 0
        pictures.append(img)












