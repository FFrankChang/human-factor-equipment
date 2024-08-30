import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__))
data_dir = join(Example_dir, 'data')
modules_dir = join(Example_dir, 'src')
sys.path.append(modules_dir)
from TaskManager import TaskManager
from CushionData import CushionData
import pandas as pd

task_file_path = join(data_dir, 'ZGY_50.csv')
cushion_data_file_path = join(data_dir, 'ZGY_cushion.csv')

initial_period = 10

if __name__ == "__main__":
    
    task_manager = TaskManager(task_file_path)
    cushion_data = CushionData(cushion_data_file_path)
    tasks = task_manager.get_tasks()
    extracted_data_list = []
    
    for index, row in tasks.iterrows():
        task_name = row['任务名称']
        start_time = row['开始时间']
        end_time = row['结束时间']
        
        extracted_data = cushion_data.extract_data_for_task(start_time-initial_period, end_time, task_name)
        
        if extracted_data is not None:
            extracted_data_list.append(extracted_data)
            tasks.loc[index, '坐垫匹配'] = len(extracted_data)
            tasks.loc[index, '坐垫压力重心偏移'] = cushion_data.calculate_centroid_shift(extracted_data,initial_period=initial_period)
            tasks.loc[index, '平均接触面积'] = cushion_data.count_pressure_over_threshold_mean(extracted_data)
            
        else:
            tasks.loc[index, '坐垫匹配'] = 0
            
    # if extracted_data_list:
    #     all_extracted_data = pd.concat(extracted_data_list, ignore_index=True)
    #     all_extracted_data.to_csv(task_file_path.replace('.csv', '_extracted.csv'), index=False)  
              
    tasks.to_excel(task_file_path.replace('.csv', '_cushion_calculated.xlsx'), index=False)