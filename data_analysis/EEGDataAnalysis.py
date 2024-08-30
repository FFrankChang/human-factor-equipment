import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__))
data_dir = join(Example_dir, 'data')
modules_dir = join(Example_dir, 'src')
sys.path.append(modules_dir)
from TaskManager import TaskManager
from EEGData import EEGData
import pandas as pd

task_file_path = join(data_dir, 'HJY_50.csv')
eeg_data_file_path = join(data_dir, 'HJY_eeg.csv')


if __name__ == "__main__":
    
    task_manager = TaskManager(task_file_path)
    eeg_data = EEGData(eeg_data_file_path)
    tasks = task_manager.get_tasks()
    extracted_data_list = []
    
    for index, row in tasks.iterrows():
        task_name = row['任务名称']
        start_time = row['开始时间']
        end_time = row['结束时间']
        extracted_data = eeg_data.extract_data_for_task(start_time, end_time, task_name)
        if extracted_data is not None:
            extracted_data_list.append(extracted_data)
            if tasks.loc[index, '操作时间（s）']==0:
                duation = 1
            else:
                duation = tasks.loc[index, '操作时间（s）']

            tasks.loc[index, 'EEG匹配'] = len(extracted_data)
            tasks.loc[index, '平均心率'] = eeg_data.get_average_heart_rate(extracted_data)   
            tasks.loc[index, 'RMSSD'] = eeg_data.get_average_rmssd(extracted_data)   
            tasks.loc[index, 'β波相对功率'] = eeg_data.calculate_relative_beta_power(extracted_data)   
        else:
            tasks.loc[index, 'EEG匹配'] = 0
            
    # if extracted_data_list:
    #     all_extracted_data = pd.concat(extracted_data_list, ignore_index=True)
    #     all_extracted_data.to_csv(task_file_path.replace('.csv', '_extracted.csv'), index=False)  
              
    tasks.to_excel(task_file_path.replace('.csv', '_eeg_calculated.xlsx'), index=False)