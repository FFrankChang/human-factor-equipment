import pandas as pd

class CushionData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.process_data()

    def process_data(self):
        processed_data_list = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 33): 
                timestamp = float(lines[i].strip().split(',')[1])
                pressure_matrix = [line.strip().split(',')[1:] for line in lines[i+1:i+33]]
                pressure_data = [item for sublist in pressure_matrix for item in sublist]
                pressure_data_str = ','.join(pressure_data)
                processed_data_list.append([timestamp, pressure_data_str])

        return pd.DataFrame(processed_data_list, columns=['timestamp', 'Pressure Data'])
    
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
