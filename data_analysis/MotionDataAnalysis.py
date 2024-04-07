import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__))
data_dir = join(Example_dir, 'data')
modules_dir = join(Example_dir, 'src')
sys.path.append(modules_dir)
from TaskManager import TaskManager
from MotionData import MotionData
import pandas as pd

task_file_path = join(data_dir, 'Guo_task.csv')
motion_data_file_path = join(data_dir, 'Guo_motion.csv')
finger = 'RightSecondDP'

if __name__ == "__main__":
    
    task_manager = TaskManager(task_file_path)
    motion_data = MotionData(motion_data_file_path)
    tasks = task_manager.get_tasks()
    extracted_data_list = []
    
    for index, row in tasks.iterrows():
        task_name = row['任务名称']
        start_time = row['开始时间']
        end_time = row['结束时间']
        
        extracted_data = motion_data.extract_data_for_task(start_time, end_time, task_name)
        
        if extracted_data is not None:
            extracted_data_list.append(extracted_data)
            tasks.loc[index, '动捕匹配'] = len(extracted_data)
            tasks.loc[index, '右手拇指累计位移'] = motion_data.calculate_total_movement(extracted_data,finger=finger)
        else:
            tasks.loc[index, '动捕匹配'] = 0
            
    if extracted_data_list:
        all_extracted_data = pd.concat(extracted_data_list, ignore_index=True)
        all_extracted_data.to_csv(task_file_path.replace('.csv', '_extracted.csv'), index=False)  
              
    tasks.to_csv(task_file_path.replace('.csv', '_calculated.csv'), index=False)