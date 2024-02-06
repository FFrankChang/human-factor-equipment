import sys
sys.path.append('..')  # make sure that pylsl is found
import pylsl
import csv
import keyboard
import time
# first resolve an EEG stream on the lab network
print("looking for an AudioCaptureWin stream...")
streams = pylsl.resolve_stream('type', 'NIRS')

# create a new inlet to read from the stream
inlet = pylsl.stream_inlet(streams[0])
sample = pylsl.vectorf()
filename = 'trust_fnirs_20240206_1.csv'


# Open a CSV file for writing
with open(filename, 'w', newline='') as csvfile:
    data_writer = csv.writer(csvfile, delimiter=',')
    
    while True:
        # Check if ESC is pressed
        if keyboard.is_pressed('esc'):
            print("ESC pressed, exiting loop.")
            break

        # get a new sample
        timestamp = inlet.pull_sample(sample)
        # Write the timestamp and the sample to the CSV

        result=time.time(),list(sample)
        print(result)
        data_writer.writerow(result)
        time.sleep(0.01)
print("Data collection stopped.")
