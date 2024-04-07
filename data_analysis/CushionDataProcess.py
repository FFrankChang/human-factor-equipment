import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__))
test_data_dir = join(Example_dir, 'test_data')
modules_dir = join(Example_dir, 'src')
sys.path.append(modules_dir)
from CushionData import CushionData

cushion_data_file_path = join(test_data_dir, 'cushion_test.csv')
save_file_path = join(test_data_dir, 'cushion_cal.csv')
# Set parameters
radio =  7.50062
threshold_kpm2 = 0.43 
unit = 1.0

if __name__ == "__main__":
    cushion = CushionData(cushion_data_file_path)
    cushion.count_pressure_over_threshold(threshold_mmHg=threshold_kpm2*radio,unit=unit)
    cushion.calculate_pressure_sum_change()
    cushion.calculate_centroid_movement()
    print(cushion.data.head())
    
    cushion.show_heatmap()

    # cushion.save_data(save_file_path)
