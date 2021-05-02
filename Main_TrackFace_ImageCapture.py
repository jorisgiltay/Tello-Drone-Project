from utils import *
import cv2
import pygame
import time

#Initialize Variables
pid = [0.5, 0.5, 0.0005]
startCounter = 0 # NO FLIGHT = 1, FLIGHT = 0
up_down, yaw, forward_backward, left_right = 0, 0, 0, 0
turn_off_tracking, turn_on_tracking = 0, 0
flip_left_right, flip_front_back = 0, 0
flying, take_off, land, snap_image = False, False, False, False
w, h = 360, 240
pError = np.array([0, 0, 0])
i = 0
k = 0
track_mode = 0
img, pictures, trackedfaces = [], [], []

#Initialize Pygame and Joystick
pygame.init()
Joysticks = init_joysticks()
XBox_360 = Joysticks[0]

#Initialize Drone
giltayDrone = initializeTello()
giltayDrone.streamon()
telloGetFrame(giltayDrone, 360 , 240)

while True:
    for event in pygame.event.get():  # User did something.
        if event.type == pygame.JOYBUTTONDOWN:
            [take_off, land, turn_on_tracking, turn_off_tracking, snap_image] = joystick_get_buttons(XBox_360)
        if event.type == pygame.JOYAXISMOTION:
            [yaw, up_down, left_right, forward_backward] = joystick_get_axes(XBox_360)
        if event.type == pygame.JOYHATMOTION:
            [flip_left_right, flip_front_back] = joystick_get_hats(XBox_360)


    img = telloGetFrame(giltayDrone, 360, 240)
    trackedFace, info = findFace(img)
    cv2.imshow("image",trackedFace)

    ## Toggle land or takeoff
    if take_off == 1 and flying == False:
        print('take_off')
        response = giltayDrone.takeoff()
        flying = True

    if land == 1 and flying == True:
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

    ## Toggling tracking mode
    if turn_on_tracking == 1 and track_mode == False:
        track_mode = True

    if turn_off_tracking == 1 and track_mode == True:
        track_mode = False

    if track_mode == False:
        giltayDrone.send_rc_control(left_right_velocity= left_right,
                                    up_down_velocity= up_down,
                                    forward_backward_velocity= forward_backward,
                                    yaw_velocity= yaw)


    if track_mode == True:
        pError = trackface(giltayDrone,info, w, h, pid, pError)




    if (trackedFace is not None):
        trackedfaces.append(trackedFace)


    if snap_image == 1:
        print("TOOK PICTURE")
        show_frame = 0
        pictures.append(img)

    if flying == True and track_mode == False:
        if flip_left_right == -1:
            giltayDrone.flip_left()
            time.sleep(0.3)
        if flip_left_right == 1:
            giltayDrone.flip_right()
            time.sleep(0.3)
        if flip_front_back == -1:
            giltayDrone.flip_back()
            time.sleep(0.3)
        if flip_front_back == 1:
            giltayDrone.flip_forward()
            time.sleep(0.3)

    time.sleep(0.001)














