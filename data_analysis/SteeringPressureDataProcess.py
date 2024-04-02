from src.SteeringPressureData import SteeringPressureData

steering_pressure_data_file_path = './test_data/steering_test.txt'
save_file_path = './test_data/steering_cal.csv'


if __name__ == "__main__":
    steering = SteeringPressureData(steering_pressure_data_file_path)
    steering.calculate_pressure_sums()
    steering.calculate_max_min()
    steering.save_data(save_file_path)
    steering.show_heatmap()