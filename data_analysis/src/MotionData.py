from .Datafile import DataFile
import pandas as pd
import numpy as np

class MotionData(DataFile):
    def __init__(self, filepath):
        super().__init__(filepath)

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
        
    def calculate_total_movement(self,extracted_data,finger='RightSecondDP'):
        """
        计算手指的总空间位移。
        """
        extracted_data['dx'] = extracted_data[f'{finger} x'].diff()
        extracted_data['dy'] = extracted_data[f'{finger} y'].diff()
        extracted_data['dz'] = extracted_data[f'{finger} z'].diff()
        extracted_data['distance'] = np.sqrt(extracted_data['dx']**2 + extracted_data['dy']**2 + extracted_data['dz']**2)
        total_movement = extracted_data['distance'].sum()

        return total_movement