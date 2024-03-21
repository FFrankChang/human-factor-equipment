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
udp_socket.settimeout(1)  

def time_format(date_str, time_str):
    date_format = "%Y%m%d"
    time_format = "%H:%M:%S.%f"
    datetime_str = f"{date_str} {time_str}"
    datetime_format = f"{date_format} {time_format}"
    dt = datetime.strptime(datetime_str, datetime_format)
    dt += timedelta(hours=8)
    timestamp = dt.timestamp()
    return timestamp

def parse_euler(date=20240320):
    format_string = '>6sIcblbbbbhh'
    try:
        data, addr = udp_socket.recvfrom(4096) 
        header = struct.unpack(format_string, data[0:24])
        time_hour = data[28:].decode('utf-8')
        timestamp = time_format(date, time_hour)
        print(timestamp, header[1])
        data_list.append((timestamp, header[1]))
    except socket.timeout:
        pass

if __name__ == "__main__":
    file_name = 'test_time.csv'
    while not keyboard.is_pressed('esc'):
        parse_euler()
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_list)
