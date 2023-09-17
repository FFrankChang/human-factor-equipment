import socket
import time
import struct
import asyncio
import websockets
import json

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_address = ('localhost', 9763)
udp_socket.bind(local_address)
final_data={
    'type':'motion_capture',
    'data':[]
}
server_address = ('192.168.31.122', 9763)
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def parse():
    format_string = '>6sIcblbbbbhh'
    segment_format = '>Ifffffff'
    # Unpack the binary data using the format string
    # print("等待消息...")
    data, addr = udp_socket.recvfrom(4096)  # 一次最多接收4096字节的数据
    # print(data.__len__())
    header = struct.unpack(format_string, data[0:24])
    body = []
    for i in range(23):
        segment_body=[]
        pos = []
        ori = []
        begin_flag = 24+ i*32
        end_flag = 23 + 32 + i*32 + 1
        # print(i,': ',begin_flag,end_flag)
        segment_data = struct.unpack(segment_format,data[begin_flag:end_flag])
        id = segment_data[0]
        for j in range(1,4):
            pos.append(segment_data[j])
        for k in range(4,8):
            ori.append(segment_data[k])
        segment_body.append(id)
        segment_body.append(pos)
        segment_body.append(ori)
        body.append(segment_body)
    # print(header)
    # print(body)
    # print(data)
    return body

async def send_data():
    uri = "ws://192.168.31.122:9763" 
    while True:
        final_data['data']=parse()
        print(final_data)
        socket.sendto(json.dumps(final_data).encode(), server_address)
        # await asyncio.sleep(1)
    # async with websockets.connect(uri) as websocket:
    #     while True:
    #         await websocket.send(str(parse()))
    #         print("Sent Successfully")
    #         await asyncio.sleep(1)  # 每秒发送一次消息
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_data())
