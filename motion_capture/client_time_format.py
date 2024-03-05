import socket
import time
import struct
import asyncio
import keyboard
import csv
from datetime import datetime, timedelta

data_list = []
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_address = ('localhost', 9763)
udp_socket.bind(local_address)
udp_socket.settimeout(10)  

def time_format(date_str, time_str):
    # ... 时间格式化函数保持不变 ...

def parse_euler(date=20240131):
    format_string = '>6sIcblbbbbhh'
    try:
        data, addr = udp_socket.recvfrom(4096) 
        header = struct.unpack(format_string, data[0:24])
        time_hour = data[28:].decode('utf-8')
        timestamp = time_format(date, time_hour)
        print(timestamp, header[1])
        data_list.append((timestamp, header[1]))
    except socket.timeout:
        pass  # 当超时时，不执行任何操作

def send_data():
    file_name = '022.csv'
    while not keyboard.is_pressed('esc'):
        parse_euler()
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_list)

if __name__ == "__main__":
    send_data()
