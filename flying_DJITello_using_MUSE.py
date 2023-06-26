import matplotlib
from pylsl import StreamInlet, resolve_stream # first resolve an EEG # stream on the lab network
import time
from djitellopy import Tello, BackgroundFrameRead
import cv2
import math
import keyboard
import threading
import queue
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter


def frame_read():
     """
    Continuously reads frames from the drone's video stream and puts them into a queue.
    """
    while True:
        # Get the next frame from the video stream
        frame = tello.get_frame_read().frame
        frame = cv2.resize(frame, (360, 240))
        if not frame_queue.full():
            frame_queue.put(frame)
            time.sleep(1/50)   # Video resulotion - 50fps


def display_frames():
    """
    Continuously retrieves frames from the queue and displays them using OpenCV.
    """
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            cv2.imshow("Tello View", frame)
            cv2.waitKey(1)


tello = Tello()
tello.connect()
print("Tello initial battery is: " + str(tello.get_battery()))
print("Tello initial height is: " + str(tello.get_height()))
print("Tello initial temperature is: " + str(tello.get_temperature()))
tello.streamon()

# video start early because it have some delay time to rise
frame_queue = queue.Queue()
read_thread = threading.Thread(target=frame_read)
read_thread.daemon = True
display_thread = threading.Thread(target=display_frames)
display_thread.daemon = True
display_thread.start()
read_thread.start()

time.sleep(3)

# ESC key for keyboard control
keys = ["esc"]

# first resolve an EEG stream on the lab network
print("looking for an Accelemator stream...")
print("looking for an EEG stream...")
streams_EEG = resolve_stream('type', 'EEG')
streams_Accel = resolve_stream('type', 'Accelerometer')

# create a new inlet to read from the stream
inlet_EEG = StreamInlet(streams_EEG[0])
inlet_Accel = StreamInlet(streams_Accel[0])
time_start = time.time()
EEG_data_TP9_tot=[]
EEG_data_TP10_tot=[]
Accel_x_tot=[]
Accel_y_tot=[]
Accel_z_tot=[]

#standard values:
standard_Accelemator_x= 0.0   # in future insert those variables to main flow.
standard_Accelemator_y= 0.1
standard_EEG_TP9_TP10 = -30

# a flag to detect 2 blinks in a row
second_blink = False
tello_on_air = False
while (time.time()-time_start < 80):
  time_start_section = time.time()
  EEG_data_TP9 = []
  EEG_data_TP10 = []
  Accel_x = []
  Accel_y = []

  while (time.time()-time_start_section <1):
    chunk1, timestamps1 = inlet_EEG.pull_chunk()
    chunk2, timestamps2 = inlet_Accel.pull_chunk()

    if timestamps1:
      EEG_data_TP9.append((np.mean(np.array(chunk1), axis=0))[0])
      EEG_data_TP10.append((np.mean(np.array(chunk1), axis=0))[3])

      # Data to print final graphs
      EEG_data_TP9_tot.append((np.mean(np.array(chunk1), axis=0))[0])
      EEG_data_TP10_tot.append((np.mean(np.array(chunk1), axis=0))[3])

    if timestamps2:
      Accel_x.append((np.mean(np.array(chunk2), axis=0))[0])
      Accel_y.append((np.mean(np.array(chunk2), axis=0))[1])

      # Data to print final graphs
      Accel_x_tot.append((np.mean(np.array(chunk2), axis=0))[0])
      Accel_y_tot.append((np.mean(np.array(chunk2), axis=0))[1])

  EEG_data_TP9=np.array(EEG_data_TP9)
  EEG_data_TP10=np.array(EEG_data_TP10)

  EEG_data_TP9 = gaussian_filter(np.array(EEG_data_TP9), sigma=2)
  EEG_data_TP10 = gaussian_filter(np.array(EEG_data_TP10), sigma=2)

  Accel_x = np.array(Accel_x)
  Accel_y = np.array(Accel_y)

  if(np.any(EEG_data_TP9<-380)  and np.any(EEG_data_TP10 <- 300) ):
    if not second_blink and tello_on_air:
        tello.move("up", 40)
        print("blink - rise up")
        continue
    if second_blink:
        print("second blink in a row - take off")
        if tello.get_height() == 0:
            tello.takeoff()
            tello_on_air = True
            second_blink = False
            continue
    second_blink = True
    print("first blink in a row")
  elif mean_Accel_x < -0.4 and tello_on_air:
        tello.move("forward", 40)
        second_blink = False
        print("up")
  elif mean_Accel_x > 0.4 and tello_on_air:
        if tello.get_height() < 40:
            print("down - land")
            second_blink = False
            tello.land()
            tello_on_air = False
        else:
            tello.move("down", 40)
            second_blink = False
            print("down")
  elif mean_Accel_y > 0.5 and tello_on_air:
        tello.rotate_clockwise(45)
        second_blink = False
        print("right")
  elif mean_Accel_y < -0.5 and tello_on_air:
        tello.rotate_counter_clockwise(45)
        second_blink = False
        print("left")
  elif keyboard.is_pressed('esc'):  # Landing
        second_blink = False
        tello.move("unkown command to tello to land", 0)
  else:
        continue

tello.streamoff()
cv2.destroyAllWindows()

# At this point we start building our graphs
EEG_data_TP9_tot=np.array(EEG_data_TP9_tot)
EEG_data_TP10_tot=np.array(EEG_data_TP10_tot)

EEG_data_TP9_tot=gaussian_filter(np.array(EEG_data_TP9_tot), sigma=2)
EEG_data_TP10_tot=gaussian_filter(np.array(EEG_data_TP10_tot), sigma=2)

Accel_x_tot = np.array(Accel_x_tot)
Accel_y_tot = np.array(Accel_y_tot)

###EEG#####
plt.subplot(2,1,1)
plt.plot(EEG_data_TP9_tot, color='navy')
plt.axhline(y=standard_EEG_TP9_TP10 - 350,  color='gray')
plt.axhline(y=standard_EEG_TP9_TP10,  color='r')
plt.title('EEG_data_TP9')
plt.ylabel('Amplitude [uV]')
plt.xlabel('Time[1/25 sec]')

plt.subplot(2,1,2)
plt.plot(EEG_data_TP10_tot, color='purple')
plt.axhline(y=standard_EEG_TP9_TP10 - 270,  color='gray')
plt.axhline(y=standard_EEG_TP9_TP10,  color='r')
plt.title('EEG_data_TP10')
plt.ylabel('Amplitude [uV]')
plt.xlabel('Time[1/25 sec]')
plt.show()
###EEG#####

###Accele###
plt.subplot(2,1,1)
plt.plot(Accel_x_tot, color='green')
plt.axhline(y=standard_Accelemator_x - 0.4,  color='gray')
plt.axhline(y=standard_Accelemator_x + 0.4,  color='gray')
plt.axhline(y=standard_Accelemator_x,  color='r')
plt.title('Accelemator_x - head tilt up/down (Pitch)')
# Pitch is rotation on the X-axis, which means an object is tilted up or down.
plt.ylabel('Amplitude [m/s^2]')
plt.xlabel('Time[1/25 sec]')

plt.subplot(2,1,2)
plt.plot(Accel_y_tot, color='orange')
plt.axhline(y=standard_Accelemator_y - 0.5,  color='gray')
plt.axhline(y=standard_Accelemator_y + 0.5,  color='gray')
plt.axhline(y=standard_Accelemator_y,  color='r')
plt.title('Accel_y - head tilt left/right (Roll)')
# Roll is rotation on the Y-axis, which means an object is tilted right or left.
plt.ylabel('Amplitude [m/s^2]')
plt.xlabel('Time[1/25 sec]')
plt.show()
###Accele###
