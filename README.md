# Drone Control with EEG and Accelerometer

This script enables you to control a Tello drone using eye blinks and head movements captured from a Muse2 EEG device. The script utilizes the Muse LSL library to stream EEG data and accelerometer readings to control the drone's flight.
It also includes functionality to display frames from the drone's camera and generate graphs based on the collected data.
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
```
  
## Usage
1. Connect your Muse2 EEG device via BlueMuse (Bluetooth).
2. Connect your Tello drone to your computer via Wi-Fi.
3. Run the script
   The script will start capturing EEG data and accelerometer readings from the Muse2 device.

To control the drone:
- Blink your eyes to trigger the drone's ascent.
- Tilt your head up or down to make the drone move forward or down.
- Tilt your head left or right to rotate the drone.

Note: Ensure that your Tello drone is in a safe and open environment before flying it.
## breakdown of the script and its documentation

1. Importing Libraries:
   - `matplotlib`: A plotting library for creating visualizations.
   - `pylsl.StreamInlet`, `pylsl.resolve_stream`: Libraries for working with Lab Streaming Layer (LSL) streams.
   - `time`: Library for time-related functions.
   - `djitellopy.Tello`, `djitellopy.BackgroundFrameRead`: Libraries for controlling and reading frames from a Tello drone.
   - `cv2`: OpenCV library for computer vision tasks.
   - `math`: Library for mathematical functions.
   - `keyboard`: Library for detecting keyboard events.
   - `threading`, `queue`: Libraries for managing threads and queues.
   - `numpy`: Library for numerical operations.
   - `scipy.ndimage.filters.gaussian_filter`: Function for applying a Gaussian filter to an array.

2. Function Definitions:
   - `frame_read()`: Continuously reads frames from the Tello drone's video stream and puts them into a queue.
   - `display_frames()`: Continuously retrieves frames from the queue and displays them.
  
3. Tello Drone Initialization:
   - Connects to the Tello drone using the `Tello` class.
   - Retrieves initial battery level, height, and temperature of the Tello drone.
   - Starts the video stream from the drone.
   - Creates a queue for storing frames.
   - Creates and starts separate threads for frame reading and frame display.

4. Stream Resolution and Inlet Creation:
   - Resolves and creates an EEG stream inlet using LSL.
   - Resolves and creates an accelerometer stream inlet using LSL.
   - Initializes variables for storing EEG and accelerometer data.

5. Control Loop:
   - Enters a control loop 
   - Within the control loop, it performs the following steps:
     - Reads EEG and accelerometer data from the respective inlets.
     - Processes the data and stores it in appropriate variables.
     - Checks for specific conditions (e.g., blinks, accelerometer values) to control the Tello drone's movements.
     - Executes corresponding drone movements based on the detected conditions.

6. Stream Off and Clean-Up:
   - Stops the video stream from the Tello drone.
   - Closes any remaining OpenCV windows.

7. Data Plotting:
   - Plots and displays the EEG and accelerometer data collected during the control loop.
 

