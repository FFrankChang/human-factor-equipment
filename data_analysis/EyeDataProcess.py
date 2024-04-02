from src.EyeData import EyeData

eye_data_file_path = './test_data/eye_test.csv'
save_file_path = './test_data/eye_cal.csv'

if __name__ == "__main__":
    
    eye = EyeData(eye_data_file_path)
    eye.calculate_max_head_movement()
    eye.calculate_head_movement_differences()
    eye.calculate_pupil_diameter_std_rolling(min_periods=1)
    eye.save_data(save_file_path)