from djitellopy import Tello
import cv2
import numpy as np
import pygame

def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.forward_backward_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    print(myDrone.get_battery())
    return myDrone


def telloGetFrame(myDrone, w = 180, h = 120):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img

def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,4)

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0),2)
        cx = x + w // 2
        cy = y + h // 2
        area = w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img , [myFaceListC[i], myFaceListArea[i]]
    else:
        return img , [[0, 0],0]


def trackface(myDrone, info, w, h, pid, pError):
    error = np.array([0, 0, 0])
    ## PID
    error[0] = info[0][0] - w//2
    error[1] = info[0][1] - h//2
    error[2] = info[1] - 15000

    speed = pid[0]*error + pid[1] * (error - pError)
    speed_front_back = pid[2]*error[2] + pid[2] * (error[2] - pError[2])
    speed[0] = int(np.clip(speed[0],-100,100))
    speed[1] = -int(np.clip(speed[1],-100,100))
    speed[2] = -int(np.clip(speed_front_back, -100,100))




    if info[0][0] != 0:
        myDrone.yaw_velocity = round(speed[0])
        myDrone.up_down_velocity = round(speed[1])
        myDrone.forward_backward_velocity = round(speed[2])
    else:
        myDrone.forward_backward_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = np.array([0, 0 , 0])
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.forward_backward_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
    return error

def init_joysticks():
    joystick_list = []
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick_list.append(pygame.joystick.Joystick(i))
        print("Initialized joystick: ", joystick_list[i].get_name(), "with ID: ", joystick_list[i].get_id())

    return joystick_list

def joystick_get_axes(joystick):
    num_axes = joystick.get_numaxes()
    values = [0]*num_axes
    for i in range(num_axes):
        values[i] = round(joystick.get_axis(i)*100)
        # invert second axis only for xbox
        values[1] = values[1] * -1
        values[3] = values[3] * -1
        # include deadband
        if(abs(values[i]) < 15):
            values[i] = 0
    yaw = values[0]
    up_down = values[3]
    left_right = values[2]
    forward_backward = values[1]

    return [yaw, up_down, left_right, forward_backward]

def joystick_get_buttons(joystick):

    num_buttons = joystick.get_numbuttons()
    but_values = [0]*num_buttons
    for i in range(num_buttons):
        but_values[i] = joystick.get_button(i)

    take_off = but_values[0]
    land = but_values[1]
    turn_on_track_mode = but_values[3]
    turn_off_track_mode = but_values[2]
    snap_image = but_values[6]

    return [take_off, land, turn_on_track_mode, turn_off_track_mode, snap_image]

def joystick_get_hats(joystick):
    num_hats = joystick.get_numhats()
    flip_left_right = 0
    flip_front_back = 0
    for i in range(num_hats):
        hat = joystick.get_hat(i)
        flip_front_back = hat[1]
        flip_left_right = hat[0]

    return flip_left_right, flip_front_back





