import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Load the dataset
data = pd.read_csv("..\data\motiontest.csv")

# Prepare the figure and axes for the animation
fig = plt.figure(figsize=(14, 6))

# 3D scatter plot for Left Hand and Head positions
ax1 = fig.add_subplot(131, projection='3d')
ax1.set_title('3D Positions')

# Define fixed limits for the 3D plot based on the overall min and max values
ax1_limits = {
    'xlim': [data[['Left Hand x', 'Head x']].min().min(), data[['Left Hand x', 'Head x']].max().max()],
    'ylim': [data[['Left Hand y', 'Head y']].min().min(), data[['Left Hand y', 'Head y']].max().max()],
    'zlim': [data[['Left Hand z', 'Head z']].min().min(), data[['Left Hand z', 'Head z']].max().max()],
}
ax1.set_xlim(ax1_limits['xlim'])
ax1.set_ylim(ax1_limits['ylim'])
ax1.set_zlim(ax1_limits['zlim'])

# Line plot for Left Hand data
ax2 = fig.add_subplot(132)
ax2.set_title('Left Hand x, y, z')
ax2.set_xlabel('Frame')
ax2.set_ylabel('Position')

# Line plot for Head data
ax3 = fig.add_subplot(133)
ax3.set_title('Head x, y, z')
ax3.set_xlabel('Frame')
ax3.set_ylabel('Position')

# Define the update function for the animation
def update(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Reapply fixed limits and titles for all subplots
    ax1.set_xlim(ax1_limits['xlim'])
    ax1.set_ylim(ax1_limits['ylim'])
    ax1.set_zlim(ax1_limits['zlim'])
    ax1.set_title('3D Positions')

    ax2.set_title('Left Hand x, y, z')
    ax2.set_xlabel('Frame')
    ax2.set_ylabel('Position')
    ax3.set_title('Head x, y, z')
    ax3.set_xlabel('Frame')
    ax3.set_ylabel('Position')

    # Recreate 3D scatter plot for Left Hand and Head
    ax1.scatter(data['Left Hand x'][frame], data['Left Hand y'][frame], data['Left Hand z'][frame], color='blue', label='Left Hand')
    ax1.scatter(data['Head x'][frame], data['Head y'][frame], data['Head z'][frame], color='red', label='Head')

    # Determine window for displaying the last 50 frames
    window_start = max(0, frame - 50)
    window_end = frame + 1

    # Plot Left Hand and Head data within the window
    ax2.plot(range(window_start, window_end), data['Left Hand x'][window_start:window_end], label='x')
    ax2.plot(range(window_start, window_end), data['Left Hand y'][window_start:window_end], label='y')
    ax2.plot(range(window_start, window_end), data['Left Hand z'][window_start:window_end], label='z')
    ax2.legend()

    ax3.plot(range(window_start, window_end), data['Head x'][window_start:window_end], label='x')
    ax3.plot(range(window_start, window_end), data['Head y'][window_start:window_end], label='y')
    ax3.plot(range(window_start, window_end), data['Head z'][window_start:window_end], label='z')
    ax3.legend()

# Create the animation
ani = FuncAnimation(fig, update, frames=range(len(data)), blit=False, interval=10)

plt.tight_layout()
plt.show()
