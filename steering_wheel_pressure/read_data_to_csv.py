import serial
import struct
import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to calibrate data
def calibrate(data, a3, a2, a1, a0):
    R0 = 5000
    if data == 0:
        return 0
    else:
        Rf = R0 * (4095 - data) / data
        G = 1 / Rf
        P = a3 * (G**3) + a2 * (G**2) + a1 * G + a0
        return P

# Load calibration parameters
file_path = 'D:/Frank_Project/human-factor-equipment/steering_wheel_pressure/calibration/'
calibration_file = 'calibration3.txt'  # Update this path
calibration_file_path = file_path + calibration_file
calibration_parameters = np.loadtxt(calibration_file_path, usecols=(2, 3, 4, 5))
csv_file_path = 'sensor_data.csv' # Update this path
v_max = 20 # range

# Serial port configuration
serial_port = 'COM28'
baud_rate = 9600
timeout = 0.05

# Sensor array configuration
sensor_rows = 30
sensor_cols = 32

# Calculate expected number of bytes
num_bytes = sensor_rows * sensor_cols * 2

# Initialize serial port
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

# Initialize the baseline data variable as None
baseline_data = None

# Initialize plot for live updating
fig, ax = plt.subplots()
data_matrix = np.zeros((10, 96))
c = ax.imshow(data_matrix, cmap='hot', interpolation='nearest')
plt.colorbar(c)

# Open CSV file to write data
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)

    def update_fig(*args):
        global baseline_data
        ser.write(b'A\r\n')
        data = ser.read(num_bytes)
        
        if len(data) == num_bytes:
            values = struct.unpack('<' + 'H' * (sensor_rows * sensor_cols), data)
            
            # Calibrate each data point
            calibrated_values = []
            for i, value in enumerate(values):
                a3, a2, a1, a0 = calibration_parameters[i % len(calibration_parameters)]
                calibrated_value = calibrate(value, a3, a2, a1, a0)
                calibrated_values.append(calibrated_value)
            
            if baseline_data is None:
                baseline_data = np.array(calibrated_values).reshape(sensor_rows, sensor_cols)
            else:
                current_data = np.array(calibrated_values).reshape(sensor_rows, sensor_cols)
                diff_data = current_data - baseline_data
                
                # Process diff_data
                diff_data = np.maximum(diff_data, 0)  # Replace negative values with 0
                diff_data = np.round(diff_data, 5)  # Round to 5 decimal places
                print("Max: ",np.max(diff_data))
                # Rearrange diff_data for the heatmap
                part1 = diff_data[0:10, :]
                part2 = diff_data[10:20, :]
                part3 = diff_data[20:30, :]
                part3_flipped = np.fliplr(part3)
                data_matrix = np.hstack((part1, part2, part3_flipped))
                
                c.set_data(data_matrix)
                c.set_clim(vmin=0, vmax=v_max)
                
                # Convert diff_data to comma-separated string, preserving 5 decimal places
                diff_data_str = ','.join(f"{val:.5f}" for val in diff_data.flatten())
                
                # Write the timestamp and calibrated values to CSV
                csv_row = [time.time(), diff_data_str]
                writer.writerow(csv_row)
        else:
            print("Received incomplete data, please check connection and configuration.")

        return c,
    
    ani = animation.FuncAnimation(fig, update_fig, interval=100)
    plt.show()
