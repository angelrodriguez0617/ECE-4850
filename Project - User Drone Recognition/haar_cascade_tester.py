'''Haar Cascade detection tester. This version will be used to test different Cascade Classifiers without taking off the drone
By Angel Rodriguez and Austin Philips 2023'''

from haar_cascade import find_face
import cv2 as cv
from djitellopy import Tello
import movement as mov
from check_camera import check_camera
from image_interface import trackObject

# w, h = 720, 480 # display size of the screen

if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    tello.streamon()

    # Display battery level
    battery = tello.get_battery()
    print(f'>>>>>>>>>> DRONE BATTERY: {battery}')
    if battery < 20:
        print('>>>>>>>>>> CHANGE DRONE BATTERY')

    # We want to detect a face a certain number of times just to be sure
    count = 10

    # While loop to output the live video feed
    while count > 0: # Output live video feed of the drone to user until face has been detected a certein number of times    
        frame = tello.get_frame_read()
        img = frame.frame
        # img = cv.resize(img, (w, h))
        img, info = check_camera(tello)
        # Display output window showing the drone's camera frames
        cv.imshow("Output", img)
        cv.waitKey(1)

        x, y = info[0]  # The x and y location of the center of the bounding box in the frame
        area = info[1]  # The area of the bounding box
        width = info[2] # The width of the bounding box

        if info[0][0]:
            print('>>>>>>>>>> FACE DETECTED')
            count -= 1
    
    # Close the window
    cv.destroyWindow("Output")

    # Set height of drone to match height of person's face to track
    drone = mov.movement(tello=tello)
    info = check_camera(drone.get_drone())[1] 
    for i in range(100):
        found = trackObject(drone, info, [drone.get_x_location(), drone.get_y_location(), drone.get_angle()]) 
        print(f'>>>>>>>>>> found: {found}')

    


