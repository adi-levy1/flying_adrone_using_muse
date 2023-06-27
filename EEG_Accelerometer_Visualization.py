import muselsl
from muselsl import stream, list_muses, view, record_direct, record
from pylsl import StreamInlet, resolve_stream
import time
import pylsl
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to animate and plot EEG and accelerometer data for TP9 and TP10 electrodes
def animate_all_sig(i, axs, ays, bxs, bys, cxs, cys, dxs, dys):
    EEG_data_TP9 = []
    EEG_data_TP10 = []

    inlet_EEG = StreamInlet(streams_EEG[0])
    inlet_Accel = StreamInlet(streams_Accel[0])

    chunk1, timestamps1 = inlet_EEG.pull_chunk()
    chunk2, timestamps2 = inlet_Accel.pull_chunk()

    # Fetch EEG data if available
    if timestamps1:
        EEG_data_TP9.append((np.mean(np.array(chunk1), axis=0))[0])
        EEG_data_TP9 = gaussian_filter(np.array(EEG_data_TP9), sigma=2)
        EEG_data_TP10.append((np.mean(np.array(chunk1), axis=0))[3])
        EEG_data_TP10 = gaussian_filter(np.array(EEG_data_TP10), sigma=2)
        ays.append(EEG_data_TP9)
        axs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        bys.append(EEG_data_TP10)
        bxs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))

    # Fetch accelerometer data if available
    if timestamps2:
        cys.append((np.mean(np.array(chunk2), axis=0))[0])
        cxs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        dys.append((np.mean(np.array(chunk2), axis=0))[1])
        dxs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))

    # Limit x and y lists to 30 items
    axs = axs[-30:]
    ays = ays[-30:]
    bxs = bxs[-30:]
    bys = bys[-30:]
    cxs = cxs[-30:]
    cys = cys[-30:]
    dxs = dxs[-30:]
    dys = dys[-30:]

    # Clear the plot and draw the updated data
    ax.clear()
    ax.plot(axs, ays)

    bx.clear()
    bx.plot(bxs, bys)

    cx.clear()
    cx.plot(cxs, cys)

    dx.clear()
    dx.plot(dxs, dys)

    # Format the plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('EEG_TP9_and_TP10')
    plt.ylabel('Amplitude')

# Function to animate and plot only EEG data for TP9 and TP10 electrodes
def animate_EEG_TP9_and_TP10(i, axs, ays, bxs, bys):
    EEG_data_TP9 = []
    EEG_data_TP10 = []
    chunk1, timestamps1 = inlet_EEG.pull_chunk()

    # Fetch EEG data if available
    if timestamps1:
        EEG_data_TP9.append((np.mean(np.array(chunk1), axis=0))[0])
        EEG_data_TP9 = gaussian_filter(np.array(EEG_data_TP9), sigma=2)
        EEG_data_TP10.append((np.mean(np.array(chunk1), axis=0))[3])
        EEG_data_TP10 = gaussian_filter(np.array(EEG_data_TP10), sigma=2)
        ays.append(EEG_data_TP9)
        axs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        bys.append(EEG_data_TP10)
        bxs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))

    # Limit x and y lists to 30 items
    axs = axs[-30:]
    ays = ays[-30:]
    bxs = bxs[-30:]
    bys = bys[-30:]

    # Clear the plot and draw the updated data
    ax.clear()
    ax.plot(axs, ays)

    bx.clear()
    bx.plot(bxs, bys)

    # Format the plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('EEG_TP9_and_TP10')
    plt.ylabel('amplitude')

# Function to animate and plot only accelerometer data
def animate_Accelerometer_union(i, xs, ys):
    chunk2, timestamps2 = inlet_Accel.pull_chunk()

    # Fetch accelerometer data if available
    if timestamps2:
        ys.append((np.mean(np.array(chunk2), axis=0))[0:2])
        xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))

    # Limit x and y lists to 30 items
    xs = xs[-30:]
    ys = ys[-30:]

    # Clear the plot and draw the updated data
    ax.clear()
    ax.plot(xs, ys)

    # Format the plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Accelerometer - x and Y')
    plt.ylabel('amplitude')

# Function to animate and plot accelerometer data for both X and Y axes
def animate_Accelerometer(i, axs, ays, bxs, bys):
    chunk2, timestamps2 = inlet_Accel.pull_chunk()

    # Fetch accelerometer data if available
    if timestamps2:
        ays.append((np.mean(np.array(chunk2), axis=0))[0])
        axs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        bys.append((np.mean(np.array(chunk2), axis=0))[1])
        bxs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))

    # Limit x and y lists to 30 items
    axs = axs[-30:]
    ays = ays[-30:]

    # Clear the plot and draw the updated data
    ax.clear()
    ax.plot(axs, ays)

    bxs = bxs[-30:]
    bys = bys[-30:]

    bx.clear()
    bx.plot(bxs, bys)

    # Format the plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Accelerometer - x and Y')
    plt.ylabel('amplitude')

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(3, 1, 1)
bx = fig.add_subplot(3, 1, 3)

# Initialize empty lists for storing the data to be plotted
axs = []
ays = []
bxs = []
bys = []
cxs = []
cys = []
dxs = []
dys = []

# Resolve the streams for EEG and accelerometer data
streams_EEG = resolve_stream('type', 'EEG')
streams_Accel = resolve_stream('type', 'Accelerometer')

inlet_EEG = StreamInlet(streams_EEG[0])
inlet_Accel = StreamInlet(streams_Accel[0])

# Set up the animation to call the respective functions periodically
# Uncomment the desired animation function and comment out the rest based on your requirements

# Animation for plotting EEG and accelerometer data for TP9 and TP10 electrodes
#ani = animation.FuncAnimation(fig, animate_all_sig, fargs=(axs, ays, bxs, bys, cxs, cys, dxs, dys), interval=100)

# Animation for plotting only EEG data for TP9 and TP10 electrodes
ani = animation.FuncAnimation(fig, animate_EEG_TP9_and_TP10, fargs=(axs, ays, bxs, bys), interval=100)

# Animation for plotting only accelerometer data
#ani = animation.FuncAnimation(fig, animate_Accelerometer, fargs=(axs, ays, bxs, bys), interval=100)

# Animation for plotting accelerometer data for both X and Y axes
#ani = animation.FuncAnimation(fig, animate_Accelerometer_union, fargs=(axs, ays), interval=100)

# Display the plot
plt.show()
