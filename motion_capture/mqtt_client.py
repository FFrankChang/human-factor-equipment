import asyncio
import json
import socket
import struct
from datetime import datetime
import time

import paho.mqtt.client as mqtt

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_address = ('localhost', 9763)
udp_socket.bind(local_address)
final_data={
    'data':[]
}
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
    return body

mqtt_host = "139.198.181.66"
mqtt_port = 14563
mqtt_client_id = "python_mqtt"
mqtt_topic = "YHMotionCapture"
client = mqtt.Client(mqtt_client_id)
client.connect(mqtt_host, mqtt_port, 60)

async def send_data():
    while True:
        final_data['data']=json.dumps(parse())
        final_data['timestamp']= int(datetime.now().timestamp() * 1000)
        client.publish(mqtt_topic, json.dumps(final_data).replace(' ',''))
        print(json.dumps(final_data).replace(' ',''))
        time.sleep(0.05)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_data())