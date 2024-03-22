import pandas as pd

# 指定源CSV文件路径和目标Excel文件路径
csv_file_path = '..\data\Ma_task_calculated.csv'
excel_file_path = '..\data\Ma_task_calculated.xlsx'

# 读取CSV文件（假设源文件是UTF-8编码）
df = pd.read_csv(csv_file_path, encoding='utf-8')

# 将DataFrame保存为Excel文件
df.to_excel(excel_file_path, index=False)

print("转换完成，文件保存为:", excel_file_path)
