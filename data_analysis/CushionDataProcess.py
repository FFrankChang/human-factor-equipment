from src.CushionData import CushionData

cushion_data_file_path = './test_data/cushion_test.csv'
save_file_path = './test_data/cushion_cal.csv'
radio =  7.50062
threshold_kpm2 = 0.43 
unit = 1.0

if __name__ == "__main__":
    cushion = CushionData(cushion_data_file_path)
    cushion.count_pressure_over_threshold(threshold_mmHg=threshold_kpm2*radio,unit=unit)
    cushion.calculate_pressure_sum_change()
    cushion.calculate_centroid_movement()
    print(cushion.data.head())
    
    
    
    
    cushion.save_data(save_file_path)
