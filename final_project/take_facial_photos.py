import cv2 as cv
from time import sleep
import cv2 as cv
import shutil
import threading
import os
from djitellopy import Tello
import sys


# This will be used to specify which person the recording will be of
faces = ["Angel", "Austin", "Shekaramiz"] 
# This will be used tos specify which facial angle will be recorded
angles = ['smiling', 'non-smiling']
# These are variable to adjust depending on whose face we are recording and which angle it is
face = 0
angle = 1 

path = "Default"
# Use current working directory
# parent_directory = os.getcwd()
# Use directory of the script
parent_directory = os.path.realpath(os.path.dirname(__file__))
# Name of directory to save the video and pictures into 
directory = str(faces[face] + "_" + angles[angle])
path = os.path.join(parent_directory, directory)
if os.path.isdir(directory):
    shutil.rmtree(directory)
# Create directory to save video and pictures into
os.mkdir(path)
os.chdir(path)

def extract_pictures(video, face, angle):
    '''Extract and save photos from passed video parameter'''    
    # img_num is to give each picture a unique name so pictures are not overriden
    img_num=1
    count = 0
    while True:
        if count%30 == 0:
            # Save picture  
            cv.imwrite(f'{face}_{angle}_img{img_num}.png', frame_read.frame)
            img_num += 1
        count += 1
        video.write(frame_read.frame)
        sleep(1/60)

if __name__ == "__main__":
    # Turn on drone
    drone = Tello()
    drone.connect()
    drone.streamon()
    # Austin says this might work
    sleep(0.1)

    print(f'>>>>>>>>>>>>>>>> DRONE BATTERY: {drone.get_battery()}')
    if drone.get_battery() < 20: # if battery is under 20%
        print(">>>>>>>>>>>>>>>> DRONE BATTERY LOW. CHANGE BATTERY!")

    try:
        frame_read = drone.get_frame_read()
        height, width, _ = frame_read.frame.shape
        # Record video and choose name to save it under
        video = cv.VideoWriter(f'{faces[face]}_{angles[angle]}_video.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
        # Create thread to extract pictures from video while doing other processes
        video_thread = threading.Thread(target=extract_pictures, args=(video, faces[face], angles[angle]))
        video_thread.start()

        while True: # Continue showing live feed from drone until pressing ctrl + c
            frame_read = drone.get_frame_read()
            img = frame_read.frame
            # Display output window showing the drone's camera live feed
            cv.imshow("Output", img)
            cv.waitKey(1)

    except KeyboardInterrupt: # Supposed to come here after pressing ctrl + c
        # Video must be released, otherwise, saved video will be corrupted.
        video.release()
        sys.exit()

      
        
        