from src.TaskManager import TaskManager
from src.CushionData import CushionData
import pandas as pd

task_file_path = './data/Ma_task.csv'
cushion_data_file_path = './data/Ma_eye.csv'
pre_time = 10

if __name__ == "__main__":
    
    task_manager = TaskManager(task_file_path)
    cushion_data = CushionData(cushion_data_file_path)
    tasks = task_manager.get_tasks()
    extracted_data_list = []
    
    for index, row in tasks.iterrows():
        task_name = row['任务名称']
        start_time = row['开始时间']
        end_time = row['结束时间']
        
        extracted_data = cushion_data.extract_data_for_task(start_time-pre_time, end_time, task_name)
        
        if extracted_data is not None:
            extracted_data_list.append(extracted_data)
            tasks.loc[index, '坐垫匹配'] = len(extracted_data)

            
        else:
            tasks.loc[index, '坐垫匹配'] = 0
            
    if extracted_data_list:
        all_extracted_data = pd.concat(extracted_data_list, ignore_index=True)
        all_extracted_data.to_csv(task_file_path.replace('.csv', '_extracted.csv'), index=False)  
              
    tasks.to_csv(task_file_path.replace('.csv', '_calculated.csv'), index=False)