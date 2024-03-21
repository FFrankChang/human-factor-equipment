import pandas as pd
import os

# 设置你的文件夹路径
folder_path = 'F:\\TEST\\20240320_ET5\\data\\MaBing\\1'

csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
combined_csv = pd.DataFrame()

for file in csv_files:
    df = pd.read_csv(os.path.join(folder_path, file))
    combined_csv = pd.concat([combined_csv, df])
combined_csv.reset_index(drop=True, inplace=True)
combined_csv.to_csv('F:\\TEST\\20240320_ET5\\data\\MaBing\\1\\Ma_motion.csv', index=False)
