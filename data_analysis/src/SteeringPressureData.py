import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import ndimage
from scipy.ndimage import gaussian_filter, binary_dilation, label, center_of_mass


class SteeringPressureData:
    def __init__(self, file_path):
        self.colorbar = [None, None]
        self.filepath = file_path
        self.data = self.load_and_process_data()
        self.calculate_pressure_sums()

    def load_and_process_data(self):
        """
        根据文件扩展名读取方向盘压力数据文件，并进行预处理。
        支持TXT和CSV格式的文件。
        """
        if self.filepath.endswith('.txt'):
            with open(self.filepath, 'r') as file:
                lines = file.readlines()
            data_frames = [lines[i:i+33] for i in range(0, len(lines), 33)]

            results = []
            for frame in data_frames:
                timestamp = datetime.strptime(frame[0].split('\t')[0], '%Y-%m-%d %H:%M:%S.%f')
                timestamp_sec = timestamp.timestamp()
                pressure_data = [row.split('\t')[:32] for row in frame[1:31]]
                pressure_df = pd.DataFrame(pressure_data, dtype=float)
                
                top = pressure_df.iloc[:10].values.flatten()
                middle = pressure_df.iloc[10:20].values.flatten()
                bottom = pressure_df.iloc[20:].values.flatten()
                reshaped_data = list(top) + list(middle) + list(bottom)
                pressure_data_str = ','.join(map(str, reshaped_data))
                results.append([timestamp_sec, pressure_data_str])
            columns = ['timestamp', 'Pressure_Data']
            return pd.DataFrame(results, columns=columns)

        elif self.filepath.endswith('.csv'):
            return pd.read_csv(self.filepath, names=['timestamp', 'Pressure_Data'], header=None)
        else:
            raise ValueError("Unsupported file format. Only '.txt' and '.csv' files are supported.")

    def save_data(self, filepath=None):
        if filepath is None:
            filepath = self.filepath  
        self.data.to_csv(filepath, index=False,encoding='utf-8')

    def extract_data_for_task(self, start_time, end_time, task_name):
        filtered_data = self.data[(self.data['timestamp'] >= start_time) & (self.data['timestamp'] <= end_time)].copy()
        if filtered_data.empty:
            print(f"{task_name} has no data")
            return None
        else:
            filtered_data.loc[:, '任务名称'] = task_name
            return filtered_data
    
    def calculate_pressure_sums(self):
        """
        计算每帧的压力和，并将结果作为新列添加到DataFrame中。
        """
        pressure_sums = []

        for index, row in self.data.iterrows():
            pressure_data_str = row['Pressure_Data']  
            pressure_data = np.fromstring(pressure_data_str, sep=',')
            pressure_sum = round(np.sum(pressure_data),6)
            pressure_sums.append(pressure_sum)
        self.data['Pressure_Sum'] = pressure_sums
    
    def calculate_pressure_range(self,extracted_data):
        """
        计算压力和的极差
        """
        pressure_range = extracted_data['Pressure_Sum'].max() - extracted_data['Pressure_Sum'].min()
        return pressure_range

    def count(self,extracted_data):
        return len(extracted_data)
    

    def animate_heatmaps(self):
        """
        创建一个动画，展示全部数据的热力图，每个热力图为10x96的矩阵。
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        def update(frame):
            ax.clear()
            pressure_data_str = self.data.iloc[frame]['Pressure_Data']
            pressure_data = np.fromstring(pressure_data_str, sep=',').reshape((10, 96))
            c = ax.imshow(pressure_data, cmap='hot', interpolation='nearest')
            ax.set_title(f"Frame {frame}")
            return c,

        ani = FuncAnimation(fig, update, frames=len(self.data), interval=100, blit=True,repeat=False)
        fig.colorbar(ax.images[0], ax=ax, orientation='vertical')

        plt.show()

    def show_heatmap(self,sigma):
        window = tk.Tk()
        window.title("Steering Pressure Data")
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))  # 创建两个子图
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
         

        def update_plot(frame):
            for ax in axs: 
                ax.clear()
                
            pressure_data_str = self.data.iloc[frame]['Pressure_Data']
            pressure_data = np.fromstring(pressure_data_str, sep=',').reshape((10, 96))
    
            im1 = axs[0].imshow(pressure_data, cmap='hot', interpolation='nearest')
            axs[0].set_title('Original Data')
            if not self.colorbar[0]:
                self.colorbar[0] = fig.colorbar(im1, ax=axs[0])
            else:
                self.colorbar[0].update_normal(im1)
                
            # 高斯滤波处理的数据
            filtered_data = gaussian_filter(pressure_data, sigma=sigma)

            #binary
            #filtered_data = (filtered_data > 2).astype(int)

            im2 = axs[1].imshow(filtered_data, cmap='hot', interpolation='nearest')
            axs[1].set_title(f'Filtered Data (sigma={sigma})')
            
            if not self.colorbar[1]:
                self.colorbar[1] = fig.colorbar(im2, ax=axs[1])
            else:
                self.colorbar[1].update_normal(im2)
            timestamp = self.data.iloc[frame]['timestamp']
            dt_object = datetime.fromtimestamp(timestamp)
            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            timestamp_label.config(text=f"Timestamp: {formatted_time}")
            canvas.draw()

        timestamp_label = tk.Label(window, text="Time: ", font=("Arial", 12))
        timestamp_label.pack(side=tk.TOP, fill=tk.X, expand=0)
        slider = ttk.Scale(window, from_=0, to=len(self.data)-1, orient=tk.HORIZONTAL, command=lambda s: update_plot(int(float(s))))
        slider.pack(side=tk.BOTTOM, fill=tk.X, expand=1)
        update_plot(0)  
        window.mainloop()

    def calculate_max_min(self):
        """
        计算每一帧数据中的最大值和最小值，并将这些值作为新的列添加到DataFrame中。
        """
        max_values = []
        min_values = []
        for index, row in self.data.iterrows():
            pressure_data_str = row['Pressure_Data']
            pressure_data = np.fromstring(pressure_data_str, sep=',')
            max_values.append(pressure_data.max())
            min_values.append(pressure_data.min())
    
        self.data['Max_Pressure'] = max_values
        self.data['Min_Pressure'] = min_values


    def detect_hand_positions(self,threshold=2,sigma=3):
        """
        为数据帧的每一帧数据识别手的位置，并将这些位置保存到一个新列中。
        在这个过程中，将压力数据从字符串转换为10x96的矩阵，以便识别手的位置。
        """
        def find_hand_centroids(pressure_matrix, threshold, sigma=sigma, structure=np.ones((3,3))):
            """
            应用高斯滤波和形态学膨胀操作来识别手的位置。
            参数:
            - pressure_matrix: 压力数据矩阵。
            - threshold: 用于二值化处理的阈值。
            - sigma: 高斯滤波的标准差。
            - structure: 用于形态学膨胀的结构元素。
            """
            smoothed_matrix = gaussian_filter(pressure_matrix, sigma=sigma)
            binary_matrix = (smoothed_matrix > threshold).astype(int)
            # 应用形态学膨胀操作合并接近的区域
            dilated_matrix = binary_dilation(binary_matrix, structure=structure)
            labeled_matrix, num_features = label(dilated_matrix)
            centroids = np.array(center_of_mass(pressure_matrix, labeled_matrix, range(1, num_features+1)))

            return centroids

        def calculate_angle(col, total_cols=96):
            angle = (col / total_cols) * 360
            return angle if angle <= 180 else angle - 360  
        
        hand_positions = []
        hand_angles = []

        for _, row in self.data.iterrows():
            pressure_data_str = row['Pressure_Data']
            pressure_data = np.fromstring(pressure_data_str, sep=',').reshape(10, 96)
            hand_pos = find_hand_centroids(pressure_data,threshold)
            hand_positions.append(','.join([f"({round(pos[0],3)},{round(pos[1],3)})" for pos in hand_pos]))
            hand_angles.append(','.join([f"{calculate_angle(pos[1]):.2f}" for pos in hand_pos]))

        self.data['Hand_Positions'] = hand_positions
        self.data['Hand_Angles'] = hand_angles
