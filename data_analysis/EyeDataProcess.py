import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__))
test_data_dir = join(Example_dir, 'test_data')
modules_dir = join(Example_dir, 'src')
sys.path.append(modules_dir)
from EyeData import EyeData

eye_data_file_path = join(test_data_dir, 'eye_test.csv')
save_file_path = join(test_data_dir, 'eye_cal.csv')
# except_roads_coords = (50, 800, 100, 1000)

if __name__ == "__main__":
    
    eye = EyeData(eye_data_file_path)
    eye.calculate_max_head_movement()
    eye.calculate_head_movement_differences()
    eye.calculate_pupil_diameter_std_rolling(min_periods=1)
    eye.save_data(save_file_path)