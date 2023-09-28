import sys; sys.path.append('..')  # make sure that pylsl is found (note: in a normal program you would bundle pylsl with the program)
import pylsl
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import threading
import time

def create_plots():
    num_plots = 24  # Number of subplots
    num_rows = 4     # Number of rows of subplots
    num_cols = 6     # Number of columns of subplots

    x_vals = np.linspace(0, 10, 100)  # X-axis data range
    plt.ion()  # Turn on interactive mode

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(16, 9))  # Create multiple subplots

    # Flatten the 2D subplot array for indexing
    axes = axes.ravel()

    o2hb_lines = []  # List to store o2hb lines
    hhb_lines = []  # List to store hhb lines
    y1_values = []
    y2_values = []
    
    for i, ax in enumerate(axes):
        y1_values.append(np.zeros_like(x_vals))  # Initialize Y-axis data for the curve to zeros
        y2_values.append(np.zeros_like(x_vals))  # Initialize Y-axis data for the curve to zeros
        line1, = ax.plot(x_vals, y1_values[i], label=f'Curve {i}', color='lightcoral')  # Create a line object
        line2, = ax.plot(x_vals, y2_values[i], label=f'Curve {i}', color='lightblue')  # Create a line object
        ax.set_xlim(0, 10)  # Set X-axis range
        ax.set_ylim(-200, 200)  # Set Y-axis range
        ax.set_title(f'channel{2*i}x{2*i+1}')  # Set subplot title
        o2hb_lines.append(line1)  # Append the line object to the list
        hhb_lines.append(line2)  # Append the line object to the list

    plt.tight_layout()  # Automatically adjust subplot layout

    def on_key(event):
        if event.key == 'q':
            plt.close()  # Close the plot window
            sys.exit(0)

    fig.canvas.mpl_connect('key_press_event', on_key)  # Bind the key press event handler

    while True:
        global sample

        for i in range(num_plots):
            a = 2*i
            b = 2*i+1
            y1_values[i][:-1]= y1_values[i][1:]  # Corrected variable name to y_values
            y1_values[i][-1] = sample[a]  # Get new data
            o2hb_lines[i].set_ydata(y1_values[i]) 

            y2_values[i][:-1]= y2_values[i][1:]  # Corrected variable name to y_values
            y2_values[i][-1] = sample[b]  # Get new data
            hhb_lines[i].set_ydata(y2_values[i]) 

        plt.draw()
        plt.pause(0.1)

def receive():
    # first resolve an EEG stream on the lab network
    print("looking for an AudioCaptureWin stream...")
    streams = pylsl.resolve_stream('type','NIRS')
    # create a new inlet to read from the stream
    inlet = pylsl.stream_inlet(streams[0])
    global sample
    sample = pylsl.vectorf()
    while True:
        # get a new sample (you can also omit the timestamp part if you're not interested in it)
        timestamp = inlet.pull_sample(sample)
        print(sample)
        print(type(sample))
        # time.sleep(10)


def main():
    threading.Thread(target=receive).start()
    threading.Thread(target=create_plots).start()

main()