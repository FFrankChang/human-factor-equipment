import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

processed_file_path = './data/cushion_test2.csv' 
data = pd.read_csv(processed_file_path)
first_frame_data_str = data.iloc[0]['Pressure Data']
first_frame_data = np.fromstring(first_frame_data_str, sep=',', dtype=float).reshape(32, 32)
plt.figure(figsize=(8, 8))
plt.imshow(first_frame_data, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title('Heatmap of the First Frame')
plt.show()
