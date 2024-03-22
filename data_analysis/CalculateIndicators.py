from src.TaskManager import TaskManager
from src.CushionData import CushionData
from src.MotionData import MotionData
from src.EyeData import EyeData
from src.ScanerData import ScanerData
from src.SteeringPressureData import SteeringPressureData

# 导入其他需要的数据类

subject = 'Guo'
task_file_path = f'./data/{subject}_task.csv'


data_classes = {
    'cushion': {
        'class': CushionData,
        'initial_period': 10,
        'file_path': f'./data/{subject}_cushion.csv',
        'metrics': {
            '坐垫匹配': 'count',
            '坐垫压力重心偏移': 'calculate_centroid_shift'
        },
        'metrics_params': {
            'calculate_centroid_shift': {'initial_period': 10} 
        }
    },
    'eye': {
        'class': EyeData,
        'file_path': f'./data/{subject}_eye.csv',
        'metrics': {
            '眼动匹配': 'count',
            '中控注视点个数': 'calculate_fixation_points',
            '视线离路时间': 'calculate_total_gaze_time',
            '瞳孔直径标准差': 'calculate_pupil_diameter_std',
            '眨眼频率': 'calculate_blinks'
        },
        'metrics_params': {
            'calculate_fixation_points':{'rect_coords':(50, 800, 100, 1000)},
            'calculate_total_gaze_time':{'rect_coords':(50, 800, 100, 1000)},
            # 'calculate_pupil_diameter_std':{'':},
            'calculate_blinks':{'blink_threshold':0.0035},
        }  
    },
    'motion':{
        'class': MotionData,
        'file_path': f'./data/{subject}_motion.csv',
        'metrics': {
            '动捕匹配': 'count',
            '右手拇指累计位移': 'calculate_total_movement',
        },
        'metrics_params': {
            'calculate_total_movement':{'finger':'RightSecondDP'},
        }  
    },
    'scaner':{
        'class': ScanerData,
        'file_path': f'./data/{subject}_scaner.csv',
        'metrics': {
            'scaner匹配': 'count',
            '车速偏移标准差': 'calculate_speed_std',
            '车道偏移标准差': 'calculate_lateral_shift_std',
            '踏板响应时间': 'calculate_break_pedal_reaction_time',
            '方向盘响应时间': 'calculate_steering_reaction_time',
        },
        'metrics_params': {
            'calculate_break_pedal_reaction_time':{'threshold':0.5},
            'calculate_steering_reaction_time':{'threshold':10},
        }  
    },
    'steering_pressure':{
        'class': SteeringPressureData,
        'file_path': f'./data/{subject}_steering.txt',
        'metrics': {
            '方向盘握力匹配': 'count',
            '方向盘握力极差': 'calculate_pressure_range',
        },
        'metrics_params': {
        }  
    }
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
