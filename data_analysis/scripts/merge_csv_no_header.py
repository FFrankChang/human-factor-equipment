import csv

csv_file_path_1 = "F:\\TEST\\20240320_ET5\\data\\MaBing\\001\\20240320_1.csv"
csv_file_path_2 = "F:\\TEST\\20240320_ET5\\data\\MaBing\\002\\20240320_2.csv"
combined_csv_file_path = 'F:\\TEST\\20240320_ET5\\data\\MaBing\\Ma_steering.csv'

with open(csv_file_path_1, 'r', newline='') as csv_file_1, \
     open(csv_file_path_2, 'r', newline='') as csv_file_2, \
     open(combined_csv_file_path, 'w', newline='') as combined_csv:

    csv_writer = csv.writer(combined_csv)
    csv_reader_1 = csv.reader(csv_file_1)
    csv_reader_2 = csv.reader(csv_file_2)
    for row in csv_reader_1:
        csv_writer.writerow(row)
    for row in csv_reader_2:
        csv_writer.writerow(row)
