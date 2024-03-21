import pandas as pd
import numpy as np
import pytz

class TaskManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tasks = self.load_tasks()
        
    def load_tasks(self):
        try:
            tasks_df = pd.read_csv(self.filepath)
            
            beijing_timezone = pytz.timezone('Asia/Shanghai')
            
            def to_timestamp(dt_str):
                dt = pd.to_datetime(dt_str)
                dt = beijing_timezone.localize(dt)
                return dt.timestamp()
            tasks_df['开始时间'] = tasks_df['开始时间'].apply(to_timestamp).round(3)
            tasks_df['结束时间'] = tasks_df['结束时间'].apply(to_timestamp).round(3)
            return tasks_df
        except FileNotFoundError:
            print(f"{self.filepath} not found")
            return None

    def get_tasks(self):
        return self.tasks

    def save_data(self, filepath=None):
        if filepath is None:
            filepath = self.filepath  
        self.tasks.to_csv(filepath, index=False,encoding='utf-8')