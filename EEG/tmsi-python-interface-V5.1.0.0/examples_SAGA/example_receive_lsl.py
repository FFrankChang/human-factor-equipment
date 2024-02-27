from pylsl import StreamInlet, resolve_stream
import time
import csv
import keyboard

# Resolve the stream
streams = resolve_stream('name', 'SAGA')
inlet = StreamInlet(streams[0])

# Set up CSV file for writing
with open('EEG_test2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp_EEG', 'Sample','timestamp_local'])  # Writing header

    sample_count = 0
    start_time = time.time()

    while True:
        # Check if escape key is pressed
        if keyboard.is_pressed('esc'):
            print("Escape key pressed, exiting loop")
            break

        # Pull sample from the inlet
        sample, timestamp = inlet.pull_sample()
        if timestamp:
            print(sample)
            writer.writerow([timestamp, sample,time.time()])
            sample_count += 1

# Optionally, you can print out the total time and samples recorded
end_time = time.time()
print(f"Recorded {sample_count} samples in {end_time - start_time} seconds.")
