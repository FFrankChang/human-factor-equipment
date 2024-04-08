import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import socket
import threading

# Initialize socket for UDP
HOST = '0.0.0.0'
PORT = 9763
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.setblocking(0)  # Set socket to non-blocking mode

print(f"Listening for data on {HOST}:{PORT}...")

# Global variables
latest_frame_data = None
max_pressures = []
avg_pressures = []
centroid_distances = []
cumulative_x_center = 0
cumulative_y_center = 0
frame_count = 0

def receive_data():
    global latest_frame_data
    while True:
        try:
            data, addr = sock.recvfrom(4096)
            if addr[0] == '192.168.3.3':
                # Process and store the latest data
                data_str = data.decode()
                data_list = [int(val) for val in data_str.split(',') if val.isdigit()]
                if len(data_list) == 1025:  # Ensure the data list includes timestamp + 32x32 data points
                    latest_frame_data = np.array(data_list[1:]).reshape((32, 32))
        except BlockingIOError:
            continue

# Start receiving data in a separate thread
threading.Thread(target=receive_data, daemon=True).start()

def calculate_centroid(matrix):
    y, x = np.indices(matrix.shape)
    total_weight = matrix.sum()
    if total_weight == 0:
        return np.nan, np.nan
    x_center = (x * matrix).sum() / total_weight
    y_center = (y * matrix).sum() / total_weight
    return x_center, y_center

# Initialize plots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))  # 调整figsize以适应三个图表

# For the heat map
cax = ax1.imshow(np.zeros((32, 32)), cmap='hot', interpolation='nearest')
centroid, = ax1.plot([], [], 'wo', markersize=10)
fig.colorbar(cax, ax=ax1)

# For the pressure graph
lines, = ax2.plot([], [], '-', label='Max Pressure')
line_avg, = ax2.plot([], [], '--', label='Avg Pressure')
pressure_text = ax2.text(0.02, 0.94, '', transform=ax2.transAxes)  # Place text at top left of ax2
ax2.set_xlim(0, 99)  # Display the most recent 100 data points
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)

line_centroid_dist, = ax3.plot([], [], '-o', label='Centroid Distance')
centroid_dist_text = ax3.text(0.02, 0.94, '', transform=ax3.transAxes)
ax3.set_xlim(0, 99)  # 显示最近的100个数据点
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)
ax3.set_title('Centroid Distance Over Time')

def update(frame_number):
    global max_pressures, avg_pressures, centroid_distances, cumulative_x_center, cumulative_y_center, frame_count
    if latest_frame_data is not None:
        max_pressure = np.max(latest_frame_data)
        avg_pressure = np.mean(latest_frame_data)
        max_pressures.append(max_pressure)
        avg_pressures.append(avg_pressure)
        
        # Keep only the most recent 100 data points
        if len(max_pressures) > 100:
            max_pressures = max_pressures[-100:]
            avg_pressures = avg_pressures[-100:]
        
        # Update heatmap
        vmin = 0
        vmax = max(max_pressures[-100:], default=0)
        cax.set_clim(vmin, vmax)
        cax.set_data(latest_frame_data)
        x_center, y_center = calculate_centroid(latest_frame_data)
        if np.isnan(x_center) or np.isnan(y_center):
            centroid.set_data([], [])
        else:
            centroid.set_data(x_center, y_center)
        
        # Update line graph
        lines.set_data(range(len(max_pressures)), max_pressures)
        line_avg.set_data(range(len(avg_pressures)), avg_pressures)
        
        # Adjust y-axis dynamically based on the max and avg pressures
        all_pressures = max_pressures + avg_pressures
        ax2.set_ylim(min(all_pressures, default=0), max(all_pressures, default=1) * 1.1)  # Add some margin on top
        
        # Update pressure text
        pressure_text.set_text(f'Max Pressure: {max_pressure}\nAvg Pressure: {avg_pressure}')
        ax2.figure.canvas.draw()

        frame_count += 1
        cumulative_x_center += x_center
        cumulative_y_center += y_center
        avg_x_center = cumulative_x_center / frame_count
        avg_y_center = cumulative_y_center / frame_count
        centroid_distance = np.sqrt((x_center - avg_x_center)**2 + (y_center - avg_y_center)**2)
        centroid_distances.append(centroid_distance)
        
        # 保留最近的100个数据点
        if len(centroid_distances) > 100:
            centroid_distances = centroid_distances[-100:]
        
        # 更新重心距离折线图
        line_centroid_dist.set_data(range(len(centroid_distances)), centroid_distances)
        ax3.set_ylim(0, max(centroid_distances, default=1) * 1.1)  # 添加一些顶部边距
        centroid_dist_text.set_text(f'Centroid Distance: {centroid_distance:.2f}')
        ax3.figure.canvas.draw()

ani = FuncAnimation(fig, update, interval=10)

plt.tight_layout()
plt.show()
