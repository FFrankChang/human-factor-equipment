from .Datafile import DataFile
import pandas as pd

class EyeData(DataFile):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.convert_storage_time()

    def convert_storage_time(self):
        if 'StorageTime' in self.data.columns:
            self.data['timestamp'] = self.data['StorageTime'] / 10000000
            self.data.drop('StorageTime', axis=1, inplace=True)
        else:
            print("StorageTime not found")

    def extract_data_for_task(self, start_time, end_time, task_name):
        filtered_data = self.data[(self.data['timestamp'] >= start_time) & (self.data['timestamp'] <= end_time)].copy()
        if filtered_data.empty:
            print(f"{task_name} has no data")
            return None
        else:
            filtered_data.loc[:, '任务名称'] = task_name
            return filtered_data

    def save_data(self, filepath=None):
        if filepath is None:
            filepath = self.filepath  
        self.data.to_csv(filepath, index=False,encoding='utf-8')
        
    def calculate_fixation_points(self, extracted_data, rect_coords):
            """
            计算注视点个数。rect_coords 应为 (x_min, y_min, x_max, y_max) 格式，定义矩形范围。
            """
            if extracted_data is None:
                return 0
            x_min, y_min, x_max, y_max = rect_coords
            fixation_points = extracted_data[
                (extracted_data['fvo|ScreenPoint_x'] >= x_min) & 
                (extracted_data['fvo|ScreenPoint_x'] <= x_max) &
                (extracted_data['fvo|ScreenPoint_y'] >= y_min) & 
                (extracted_data['fvo|ScreenPoint_y'] <= y_max)
            ]
            return len(fixation_points)
    
    def calculate_blinks(self, data, blink_threshold):
        """
        计算数据集中的眨眼次数。
        参数：
        - data: 要分析的Pandas DataFrame。
        - blink_threshold: 眨眼的阈值，用于判断眼睑是否闭合。
        """
        blink_count = 0
        is_blinking = False
        for opening_value in data['smarteye|LeftEyelidOpening']:
            if opening_value < blink_threshold and not is_blinking:
                is_blinking = True
            elif opening_value >= blink_threshold and is_blinking:
                is_blinking = False
                blink_count += 1

        return blink_count

    def calculate_total_gaze_time(self, data, rect_coords):
        """
        计算注视点落入指定矩形范围内的总时间。
        参数：
        - data: 要分析的Pandas DataFrame。
        - rect_coords: 矩形坐标，格式为 (x_min, y_min, x_max, y_max)。
        """
        total_gaze_time = 0
        previous_timestamp = None
        for index, row in data.iterrows():
            x = row['fvo|ScreenPoint_x']
            y = row['fvo|ScreenPoint_y']
            current_timestamp = row['timestamp']
            if rect_coords[0] <= x <= rect_coords[2] and rect_coords[1] <= y <= rect_coords[3]:
                if previous_timestamp is not None:
                    time_diff_ms = current_timestamp - previous_timestamp
                    total_gaze_time += time_diff_ms
            previous_timestamp = current_timestamp
        total_gaze_time_seconds = total_gaze_time
        return total_gaze_time_seconds
    
    def calculate_pupil_diameter_std(self, data, eye='Left'):
        """
        计算给定数据中瞳孔直径的标准差。
        参数：
        - data: 要分析的Pandas DataFrame。
        - eye: 指定是计算左眼还是右眼的瞳孔直径标准差，可选值为 'Left' 或 'Right'。
        """
        if eye == 'Left':
            column_name = 'smarteye|LeftPupilDiameter'
        elif eye == 'Right':
            column_name = 'smarteye|RightPupilDiameter'
        else:
            print("Invalid eye specified. Please choose 'Left' or 'Right'.")
            return None
        
        if column_name in data.columns:
            pupil_diameter_std = data[column_name].std()
            return pupil_diameter_std
        else:
            print(f"{column_name} column does not exist in the data.")
            return None
    
    def count(self,extracted_data):
        return len(extracted_data)

    def calculate_pupil_diameter_std_rolling(self,min_periods=1):
        """
        使用pandas的rolling方法优化计算，计算每一帧数据（每一行）smarteye|LeftPupilDiameter，
        smarteye|RightPupilDiameter的前1秒内所有数据的标准差，并将结果保存到新的列中。
        """
        time_diffs = self.data['timestamp'].diff().fillna(0)  # 计算时间差
        approx_rows_per_second = int(1 / time_diffs.median())  # 估算1秒内大约有多少行

        self.data['left_pupil_diameter_std'] = self.data['smarteye|LeftPupilDiameter'].rolling(window=approx_rows_per_second, min_periods=min_periods).std()
        self.data['right_pupil_diameter_std'] = self.data['smarteye|RightPupilDiameter'].rolling(window=approx_rows_per_second, min_periods=min_periods).std()

        self.data['left_pupil_diameter_std'].fillna(0, inplace=True)
        self.data['right_pupil_diameter_std'].fillna(0, inplace=True)

    def calculate_max_head_movement(self):
        """
        计算smarteye|HeadHeading, smarteye|HeadPitch, 和 smarteye|HeadRoll三列数据中每一帧的最大值，
        并将这个最大值保存到一个新列中。
        """
        self.data['max_head_movement'] = self.data[['smarteye|HeadHeading', 'smarteye|HeadPitch', 'smarteye|HeadRoll']].max(axis=1)
    
    def calculate_head_movement_differences(self):
        """
        计算smarteye|HeadHeading, smarteye|HeadPitch, smarteye|HeadRoll三列数据的差值，
        并将结果保存到新的三列中。确保第一帧和第二帧的差值被设置为0。
        """
        for column in ['smarteye|HeadHeading', 'smarteye|HeadPitch', 'smarteye|HeadRoll']:
            new_column_name = f'delta_{column}'
            self.data[new_column_name] = self.data[column].diff()
            self.data[new_column_name].fillna(0, inplace=True)
            if len(self.data) > 1:
                self.data.iat[1, self.data.columns.get_loc(new_column_name)] = 0
