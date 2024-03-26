import serial
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 配置串口参数
serial_port = 'COM28'
baud_rate = 9600
timeout = 0.05

# 传感器阵列配置
sensor_rows = 30
sensor_cols = 32

# 计算应接收的字节数
num_bytes = sensor_rows * sensor_cols * 2

# 初始化串口
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

# 初始化图形显示
fig, ax = plt.subplots()
data_matrix = np.zeros((10, 96))
cmap = plt.cm.binary
c = ax.imshow(data_matrix, cmap='hot', interpolation='nearest')

def update_data(*args):
    ser.write(b'A\r\n')
    data = ser.read(num_bytes)
    
    if len(data) == num_bytes:
        values = struct.unpack('<' + 'H' * (sensor_rows * sensor_cols), data)
        raw_data_matrix = np.array(values).reshape(sensor_rows, sensor_cols)
        part1 = raw_data_matrix[0:10, :]
        part2 = raw_data_matrix[10:20, :]
        part3 = raw_data_matrix[20:30, :]
        part3_flipped = np.fliplr(part3)
        data_matrix = np.hstack((part1, part2, part3_flipped))

        print('Max value in matrix:', np.max(raw_data_matrix))

        c.set_data(data_matrix)
        c.set_clim(vmin=0, vmax=4000)  # 更新颜色映射范围
        plt.draw()  
    else:
        print("接收到的数据不完整，请检查连接和配置。")
    
    return c,
ani = animation.FuncAnimation(fig, update_data, interval=50, blit=False)

plt.show()
