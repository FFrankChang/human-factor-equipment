from src.SteeringPressureData import SteeringPressureData

steering_pressure_data_file_path = './test_data/steering_test.csv'
save_file_path = './test_data/steering_cal.csv'


if __name__ == "__main__":
    steering = SteeringPressureData(steering_pressure_data_file_path)
    # steering.calculate_pressure_sums()
    # steering.calculate_max_min()
    steering.detect_hand_positions(threshold=2,sigma=3)
    steering.save_data(save_file_path)
    # steering.show_heatmap(sigma=3)
