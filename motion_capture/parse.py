import socket
import time
import struct
import asyncio
import websockets
import json
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_address = ('localhost', 9763)
udp_socket.bind(local_address)

def parse_euler():
    format_string = '>6sIcblbbbbhh'
    segment_format = '>Iffffff'
    # Unpack the binary data using the format string
    # print("等待消息...")
    data, addr = udp_socket.recvfrom(4096)  # 一次最多接收4096字节的数据
    # print(data.__len__())
    header = struct.unpack(format_string, data[0:24])
    body = []
    for i in range(24):
        segment_body=[]
        pos = []
        ori = []
        begin_flag = 24+ i*28
        end_flag = 23 + 28 + i*28 + 1
        # print(i,': ',begin_flag,end_flag)
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
    # print(header)
    # print(round(body[23][2][0],2),round(body[23][2][1],2),round(body[23][2][2],2))
    print(round(body[23][2][1],2))
    # print(data)
    return body