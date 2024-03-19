import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 读取CSV文件
df = pd.read_csv('test.csv', header=None)

# 预处理数据
frames = []
for start in range(0, df.shape[0], 33):
    frame_data = df.iloc[start+1:start+33].reset_index(drop=True)  # 跳过每帧的第一行
    frames.append(frame_data)

def calculate_centroid(matrix):
    y, x = np.indices(matrix.shape)
    total_weight = matrix.sum()
    if total_weight == 0:
        return np.nan, np.nan
    x_center = (x * matrix).sum() / total_weight
    y_center = (y * matrix).sum() / total_weight
    return x_center, y_center

# 计算所有帧的重心
centroids = np.array([calculate_centroid(frame.to_numpy()) for frame in frames])

# 计算重心的平均位置
mean_centroid = np.nanmean(centroids, axis=0)

# 计算每一帧重心与平均重心位置的距离差值
distances = np.sqrt((centroids[:, 0] - mean_centroid[0])**2 + (centroids[:, 1] - mean_centroid[1])**2)

# 计算每一帧的压力数据矩阵平均值
mean_pressures = np.array([frame.to_numpy().mean() for frame in frames])

# 准备动画
fig, axs = plt.subplots(1, 3, figsize=(20, 6))
cax = axs[0].imshow(frames[0].to_numpy(), cmap='hot', interpolation='nearest')
centroid, = axs[0].plot([], [], 'wo', markersize=10)  # 初始化重心点
fig.colorbar(cax, ax=axs[0])
axs[0].set_title('Pressure Map')

line1, = axs[1].plot([], [], label='Distance from Mean Centroid')  # 初始化第二个折线图
axs[1].set_xlim(0, len(frames))
axs[1].set_ylim(0, np.max(distances) * 1.1)
axs[1].set_title('Distance from Mean Centroid')
axs[1].set_xlabel('Frame')
axs[1].set_ylabel('Distance')
axs[1].legend()

line2, = axs[2].plot([], [], 'r', label='Mean Pressure')  # 初始化第三个折线图
axs[2].set_xlim(0, len(frames))
axs[2].set_ylim(0, np.max(mean_pressures) * 1.1)
axs[2].set_title('Mean Pressure Over Frames')
axs[2].set_xlabel('Frame')
axs[2].set_ylabel('Mean Pressure')
axs[2].legend()

def update(frame_number):
    matrix = frames[frame_number].to_numpy()
    cax.set_data(matrix)
    axs[0].set_title(f'Frame {frame_number + 1}')
    x_center, y_center = centroids[frame_number]
    if np.isnan(x_center) or np.isnan(y_center):
        centroid.set_data([], [])
    else:
        centroid.set_data(x_center, y_center)
    
    # 更新第二个折线图数据
    line1.set_data(range(frame_number+1), distances[:frame_number+1])
    
    # 更新第三个折线图数据
    line2.set_data(range(frame_number+1), mean_pressures[:frame_number+1])

ani = FuncAnimation(fig, update, frames=len(frames), interval=10, repeat=False)

plt.tight_layout()
plt.show()