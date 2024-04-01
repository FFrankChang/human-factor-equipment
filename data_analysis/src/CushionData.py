import pandas as pd
import numpy as np

def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class CushionData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.process_data()

    def process_data(self):
        """
        处理坐垫数据文件，提取每帧的时间戳和压力矩阵，并计算重心。
        """
        processed_data_list = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 33):  
                timestamp = float(lines[i].strip().split(',')[1]) / 1000
                pressure_matrix = np.array([list(map(float, line.strip().split(',')[1:])) for line in lines[i+1:i+33]])
                centroid_x, centroid_y = self.calculate_centroid(pressure_matrix)
                pressure_data_str = ','.join(map(str, pressure_matrix.flatten()))
                processed_data_list.append([timestamp, pressure_data_str, centroid_x, centroid_y])

        return pd.DataFrame(processed_data_list, columns=['timestamp', 'Pressure Data', 'Centroid X', 'Centroid Y'])

    def calculate_centroid(self, matrix):
        """计算给定矩阵的重心"""
        total_mass = matrix.sum()
        if total_mass == 0:
            return np.nan, np.nan  
        indices = np.indices(matrix.shape)
        x_center = (indices[1] * matrix).sum() / total_mass
        y_center = (indices[0] * matrix).sum() / total_mass
        return x_center, y_center
    
    def extract_data_for_task(self, start_time, end_time, task_name):
        filtered_data = self.data[(self.data['timestamp'] >= start_time) & (self.data['timestamp'] <= end_time)].copy()
        if filtered_data.empty:
            print(f"{task_name} has no data")
            return None
        else:
            filtered_data.loc[:, '任务名称'] = task_name
            return filtered_data
        
    def save_data(self, file_path):
        self.data.to_csv(file_path, index=False)

    def calculate_centroid_shift(self, extracted_data,initial_period=10):
        """
        计算重心偏移的指标。
        参数：
        - initial_period: 起始时长（秒），用于计算平均重心位置的数据切分点。
        """
        relative_timestamps = extracted_data['timestamp'] - extracted_data['timestamp'].iloc[0]
        initial_data = extracted_data[relative_timestamps <= initial_period]
        subsequent_data = extracted_data[relative_timestamps > initial_period]
        initial_centroid_x, initial_centroid_y = self.calculate_average_centroid(initial_data)
        subsequent_centroid_x, subsequent_centroid_y = self.calculate_average_centroid(subsequent_data)
        shift = euclidean_distance(initial_centroid_x, initial_centroid_y, subsequent_centroid_x, subsequent_centroid_y)
        return shift
    
    def calculate_average_centroid(self, data):
        """计算给定数据的平均重心位置"""
        if data.empty:
            return np.nan, np.nan
        average_x = data['Centroid X'].mean()
        average_y = data['Centroid Y'].mean()
        return average_x, average_y
    
    def count(self,extracted_data):
        return len(extracted_data)
    
    def count_pressure_over_threshold(self, threshold_mmHg=0.43 * 7.50062,unit=1):
        """
        计算超过压力阈值的面积和，其中unit为单位传感器面积，暂定为1平方厘米
        """
        def count_over_threshold(row):
            pressure_values = np.array(list(map(float, row.split(','))))
            return (pressure_values > threshold_mmHg).sum()*unit
        
        self.data['Pressure Over Threshold'] = self.data['Pressure Data'].apply(count_over_threshold)
    
    def calculate_pressure_sum_change(self):
        """
        计算数据帧压力和之间的差值及变化率
        """
        pressure_sums = self.data['Pressure Data'].apply(lambda x: np.sum(np.array(list(map(float, x.split(','))))))
        
        pressure_sum_change = pressure_sums.diff()
        time_diff = self.data['timestamp'].diff()
        # self.data['timedelta'] = time_diff
        pressure_sum_change_rate = pressure_sum_change / time_diff.replace(0, np.nan)
        pressure_sum_change_rate = pressure_sum_change_rate.replace(np.inf, 0).fillna(0)
        pressure_sum_change.iloc[0] = 0
        pressure_sum_change_rate.iloc[0] = 0
        if len(pressure_sum_change) > 1:  # Check if there's more than one frame to avoid index errors
            pressure_sum_change.iloc[1] = 0
            pressure_sum_change_rate.iloc[1] = 0
        self.data['Pressure Sum Change'] = pressure_sum_change
        self.data['Pressure Sum Change Rate'] = pressure_sum_change_rate

    def calculate_centroid_movement(self, given_centroid_x=0, given_centroid_y=0):
        """
        计算与指定重心位置的偏移量
        """
        distances = np.sqrt((self.data['Centroid X'] - given_centroid_x) ** 2 + (self.data['Centroid Y'] - given_centroid_y) ** 2)
        self.data['Centroid Movement Distance'] = distances
