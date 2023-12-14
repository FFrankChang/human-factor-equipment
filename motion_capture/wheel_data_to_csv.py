import socket
import time
import struct
import csv
from datetime import datetime
import os
def parse_euler():
    format_string = '>6sIcblbbbbhh'
    segment_format = '>Iffffff'
    data, addr = udp_socket.recvfrom(4096)  # 一次最多接收4096字节的数据
    header = struct.unpack(format_string, data[0:24])
    body = []
    for i in range(24):
        segment_body=[]
        pos = []
        ori = []
        begin_flag = 24+ i*28
        end_flag = 23 + 28 + i*28 + 1
        segment_data = struct.unpack(segment_format,data[begin_flag:end_flag])
        id = segment_data[0]
        for j in range(1,4):
            pos.append(segment_data[j])
        for k in range(4,7):
            ori.append(segment_data[k])
        segment_body.append(id)
        segment_body.append(pos)
        segment_body.append(ori)
        body.append(segment_body)
    return body

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_address = ('localhost', 9763)
udp_socket.bind(local_address)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
data_folder_path = os.path.join(desktop_path, "wheel_angle_data")
formatted_datetime = datetime.now().strftime("%Y%m%d_%H-%M-%S")
filename = 'wheel_'+formatted_datetime.__str__()
csv_file_path = os.path.join(data_folder_path, f"{filename}.csv")

header = ['raw_wheel_data_x','raw_wheel_data_y','raw_wheel_data_z','timestamp']

with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)
    while 1:
        mc_data = parse_euler()
        angle_mea = mc_data[23][2][2]
        # print( mc_data[23][2])
        result = mc_data[23][2][0],mc_data[23][2][1],mc_data[23][2][2],time.time()
        print(result)
        csv_writer.writerow(result)
