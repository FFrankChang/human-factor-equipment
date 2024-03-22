from src.TaskManager import TaskManager
from src.ScanerData import ScanerData
import pandas as pd

task_file_path = './data/Ma_task.csv'
scaner_data_file_path = './data/Ma_scaner.csv'
pedal_threshold = 0.5
steering_threshold = 10

if __name__ == "__main__":
    
    task_manager = TaskManager(task_file_path)
    scaner_data = ScanerData(scaner_data_file_path)
    tasks = task_manager.get_tasks()
    extracted_data_list = []
    
    for index, row in tasks.iterrows():
        task_name = row['任务名称']
        start_time = row['开始时间']
        end_time = row['结束时间']

        extracted_data = scaner_data.extract_data_for_task(start_time, end_time, task_name)
        
        if extracted_data is not None:
            extracted_data_list.append(extracted_data)
            tasks.loc[index, 'scaner匹配'] = len(extracted_data)
            tasks.loc[index, '车速偏移标准差'] = scaner_data.calculate_speed_std(extracted_data)
            tasks.loc[index, '车道偏移标准差'] = scaner_data.calculate_lateral_shift_std(extracted_data)
            tasks.loc[index, '踏板响应时间'] = scaner_data.calculate_break_pedal_reaction_time(extracted_data,threshold=pedal_threshold)
            tasks.loc[index, '方向盘响应时间'] = scaner_data.calculate_steering_reaction_time(extracted_data,threshold=steering_threshold)
            
        else:
            tasks.loc[index, 'scaner匹配'] = 0
            
    if extracted_data_list:
        all_extracted_data = pd.concat(extracted_data_list, ignore_index=True)
        all_extracted_data.to_csv(task_file_path.replace('.csv', '_extracted.csv'), index=False)  
              
    tasks.to_csv(task_file_path.replace('.csv', '_calculated.csv'), index=False)