'''Written by Angel Rodriguez and Austin Philips 2023'''
import haar_cascade as hc
import cv2 as cv
from time import sleep
from djitellopy import tello

w, h = 720, 480 # display size of the screen

def check_camera(our_drone):
    '''Takes the lower drone class frome drone.get_drone() and returns
    the information of the haar-cascade detection.'''
    frame = our_drone.get_frame_read()
    sleep(0.2)
    img = frame.frame
    # Set live feed video window to specific size
    img = cv.resize(img, (w, h))
    img, info = hc.find_face(img)
    # return info
    return img, info