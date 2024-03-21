import pandas as pd

processed_data_list = []
file_path = './data/cushion_test.csv'
with open(file_path, 'r') as file:
    lines = file.readlines()
    for i in range(0, len(lines), 33):
        timestamp = float(lines[i].strip().split(',')[1])
        pressure_matrix = [line.strip().split(',')[1:] for line in lines[i+1:i+33]]
        pressure_data = [item for sublist in pressure_matrix for item in sublist]
        pressure_data_str = ','.join(pressure_data)
        processed_data_list.append([timestamp, pressure_data_str])

processed_data = pd.DataFrame(processed_data_list, columns=['timestamp', 'Pressure Data'])

processed_file_path = './data/cushion_test2.csv'
processed_data.to_csv(processed_file_path, index=False)
