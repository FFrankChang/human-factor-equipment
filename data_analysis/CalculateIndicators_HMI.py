import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__))
data_dir = join(Example_dir, 'data')
modules_dir = join(Example_dir, 'src')
sys.path.append(modules_dir)
from TaskManager import TaskManager
from CushionData import CushionData
from EyeData import EyeData
from EEGData import EEGData
from SteeringPressureData import SteeringPressureData

# The subject for the data files
subject = 'ZGY'
speed = '50'
task_file_path = join(data_dir, f'{subject}_{speed}.csv')

data_classes = {
    'cushion': {
        'class': CushionData,
        'initial_period': 10,
        'file_path': join(data_dir, f'{subject}_cushion.csv'),
        'metrics': {
            '坐垫匹配': 'count',
            '坐垫压力重心偏移': 'calculate_centroid_shift',
            '平均接触面积': 'count_pressure_over_threshold_mean'
        },
        'metrics_params': {
            'calculate_centroid_shift': {'initial_period': 10} 
        }
    },
    'eye': {
        'class': EyeData,
        'file_path': join(data_dir, f'{subject}_eye.csv'),
        'metrics': {
            '眼动匹配': 'count',
            '中控注视点个数': 'calculate_fixation_points',
            '视线离路时间': 'calculate_total_gaze_time',
            '瞳孔直径标准差': 'calculate_pupil_diameter_std',
            '眨眼频率': 'calculate_blinks',
            # '闭眼时长比例': 'calculate_relative_beta_power'
        },
        'metrics_params': {
            'calculate_fixation_points':{'rect_coords':(50, 800, 100, 1000)},
            'calculate_total_gaze_time':{'rect_coords':(50, 800, 100, 1000)},
            # 'calculate_pupil_diameter_std':{'':},
            'calculate_blinks':{'blink_threshold':0.0035},
        }  
    },
    'steering_pressure': {
        'class': SteeringPressureData,
        'file_path': join(data_dir, f'{subject}_steering.csv'),
        'metrics': {
            '方向盘握力匹配': 'count',
            '方向盘握力极差': 'calculate_pressure_range',
        },
        'metrics_params': {}  
    },
    'EEG': {
        'class': EEGData,
        'file_path': join(data_dir, f'{subject}_eeg.csv'),
        'metrics': {
            'EEG匹配': 'count',
            '平均心率': 'get_average_heart_rate',
            'RMSSD': 'get_average_rmssd',
            'β波相对功率': 'calculate_relative_beta_power',
        },
        'metrics_params': {}  
    }
    # Add additional data classes as needed
}

def main():
    task_manager = TaskManager(task_file_path)
    tasks = task_manager.get_tasks()
    
    for key, config in data_classes.items():
        data_instance = config['class'](config['file_path'])
        
        # 针对坐垫数据进行特殊处理
        initial_period = 0
        if key == 'cushion' and 'initial_period' in config:
            initial_period = config['initial_period']
        
        for index, row in tasks.iterrows():
            task_name, start_time, end_time = row['任务名称'], row['开始时间'], row['结束时间']
            adjusted_start_time = start_time - initial_period if key == 'cushion' else start_time
            extracted_data = data_instance.extract_data_for_task(adjusted_start_time, end_time, task_name)
            
            if extracted_data is not None:
                for metric, method_name in config['metrics'].items():
                    method = getattr(data_instance, method_name)
                    method_params = config['metrics_params'].get(method_name, {})
                    tasks.loc[index, metric] = method(extracted_data, **method_params)
            else:
                for metric, method_name in config['metrics'].items():
                    tasks.loc[index, metric] = 0
    
    tasks.to_excel(task_file_path.replace('.csv', '_calculated.xlsx'), index=False)
if __name__ == "__main__":
    main()
