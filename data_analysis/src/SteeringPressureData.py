import pandas as pd
import numpy as np
from datetime import datetime

class SteeringPressureData:
    def __init__(self, file_path):
        self.filepath = file_path
        self.data = self.load_and_process_data()
        self.calculate_pressure_sums()

    def load_and_process_data(self):
        """
        读取方向盘压力数据文件，并进行预处理。
        """
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
            pressure_sum = np.sum(pressure_data)
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