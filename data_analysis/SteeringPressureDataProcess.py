import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__))
test_data_dir = join(Example_dir, 'test_data')
modules_dir = join(Example_dir, 'src')
sys.path.append(modules_dir)
from SteeringPressureData import SteeringPressureData

steering_pressure_data = join(test_data_dir, 'steering_test.csv')
save_file_path = join(test_data_dir, 'steering_cal.csv')

if __name__ == "__main__":
    steering = SteeringPressureData(steering_pressure_data)
    # Perform the desired operations on the steering data
    steering.detect_hand_positions(threshold=2, sigma=3)
    steering.save_data(save_file_path)
    # Optionally, perform additional operations like showing a heatmap
    # steering.show_heatmap(sigma=3)
