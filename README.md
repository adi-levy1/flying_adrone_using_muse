# Drone Control with EEG and Accelerometer

This script enables you to control a Tello drone using eye blinks and head movements captured from a Muse2 EEG device. The script utilizes the Muse LSL library to stream EEG data and accelerometer readings to control the drone's flight.

## Prerequisites

Before running the script, make sure you have the following prerequisite installed:
- Python (version 3.x)
  
## Dependencies
The script relies on the following Python libraries:
- Matplotlib
- pylsl
- djitellopy
- OpenCV (cv2)
- NumPy
- SciPy

You can install the dependencies by running the following command:
```shell
pip install matplotlib pylsl djitellopy opencv-python numpy scipy

#Usage
1. Connect your Muse2 EEG device via BlueMuse (Bluetooth).
2. Connect your Tello drone to your computer via Wi-Fi.
3. Run the script
   The script will start capturing EEG data and accelerometer readings from the Muse2 device.

To control the drone:
Blink your eyes to trigger the drone's ascent.
Tilt your head up or down to make the drone move forward or down.
Tilt your head left or right to rotate the drone.

Note: Ensure that your Tello drone is in a safe and open environment before flying it.

