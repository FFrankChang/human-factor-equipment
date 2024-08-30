import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__))
data_dir = join(Example_dir, 'data')
modules_dir = join(Example_dir, 'src')
sys.path.append(modules_dir)
from TaskManager import TaskManager
from EyeData import EyeData
import pandas as pd

task_file_path = join(data_dir, 'ZGY_50.csv')
eye_data_file_path = join(data_dir, 'ZGY_eye.csv')
CID_coords = (0, 0, 1000, 1000)
except_roads_coords = (0, 0, 1000, 1000)
blink_threshold = 0.0035

if __name__ == "__main__":
    
    task_manager = TaskManager(task_file_path)
    eye_data = EyeData(eye_data_file_path)
    tasks = task_manager.get_tasks()
    extracted_data_list = []
    
    for index, row in tasks.iterrows():
        task_name = row['任务名称']
        start_time = row['开始时间']
        end_time = row['结束时间']
        extracted_data = eye_data.extract_data_for_task(start_time, end_time, task_name)
        if extracted_data is not None:
            extracted_data_list.append(extracted_data)
            if tasks.loc[index, '操作时间（s）']==0:
                duation = 1
            else:
                duation = tasks.loc[index, '操作时间（s）']

            fixation_count = eye_data.calculate_fixation_points(extracted_data, CID_coords)
            blink_count = eye_data.calculate_blinks(extracted_data,blink_threshold)
            total_gaze_time_seconds = eye_data.calculate_total_gaze_time(extracted_data,except_roads_coords)
            pupil_diameter_std = eye_data.calculate_pupil_diameter_std(extracted_data,'Left')
            tasks.loc[index, '眼动匹配'] = len(extracted_data)
            tasks.loc[index, '中控注视点个数'] = fixation_count
            tasks.loc[index, '视线离路时间'] = round(total_gaze_time_seconds,4)
            tasks.loc[index, '瞳孔直径标准差'] = round(pupil_diameter_std,6)
            tasks.loc[index, '眨眼频率'] = blink_count / tasks.loc[index, '操作时间（s）']
            tasks.loc[index, '闭眼时长比例'] = eye_data.calculate_total_eyes_closed_time(extracted_data, duation)
            
        else:
            tasks.loc[index, '眼动匹配'] = 0
            
    # if extracted_data_list:
    #     all_extracted_data = pd.concat(extracted_data_list, ignore_index=True)
    #     all_extracted_data.to_csv(task_file_path.replace('.csv', '_extracted.csv'), index=False)  
              
    tasks.to_excel(task_file_path.replace('.csv', '_eye_calculated.xlsx'), index=False)