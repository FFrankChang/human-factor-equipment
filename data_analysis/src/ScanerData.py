from Datafile import DataFile
import pandas as pd

class ScanerData(DataFile):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.convert_time()

    def convert_time(self):
        if 'time_stamp(s)' in self.data.columns:
            self.data['timestamp'] = self.data['time_stamp(s)']
            self.data.drop('time_stamp(s)', axis=1, inplace=True)
        else:
            print("time_stamp(s) not found")

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
        
    def calculate_speed_std(self,extracted_data):
        vehicle_speed_std = extracted_data[' vehicle_speed(m/s)'].std()
        return vehicle_speed_std
    
    def calculate_lateral_shift_std(self,extracted_data):
        vehicle_lateral_shift_std = extracted_data[' lateral_shift_center(m)'].std()
        return vehicle_lateral_shift_std
    
    def calculate_break_pedal_reaction_time(self,extracted_data,threshold=0.5):
        filtered_data = extracted_data[extracted_data['break_pedal(N)'] > threshold]
        if not filtered_data.empty:
            change_time = filtered_data.iloc[0]['timestamp']-extracted_data.iloc[0]['timestamp']
        else:
            change_time = 0
        return change_time

    def calculate_steering_reaction_time(self,extracted_data,threshold=4):
        first_wheeling = extracted_data.iloc[0]['wheeling']
        change_time = None
        for i in range(1, len(extracted_data)):
            if abs(extracted_data.iloc[i]['wheeling'] - first_wheeling)*540 > threshold:
                change_time = extracted_data.iloc[i]['timestamp'] - extracted_data.iloc[0]['timestamp']
                break
        if change_time is not None:
            return change_time
        else:
            return 0
    
    def count(self,extracted_data):
        return len(extracted_data)