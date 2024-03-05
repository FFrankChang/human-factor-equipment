import socket
import struct
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import time
import threading


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_address = ('localhost', 9763)
udp_socket.bind(local_address)
def parse_euler():
    while True:
        format_string = '>6sIcblbbbbhh'
        segment_format = '>Iffffff'

        data, addr = udp_socket.recvfrom(4096)  # 一次最多接收4096字节的数据
        # print(len(data))
        header = struct.unpack(format_string, data[0:24])
        body = []
        for i in range(25):
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
        # print(round(body[23][2][0],2),round(body[23][2][1],2),round(body[23][2][2],2))
        global ele_1,ele_2
        ele_1=body[23][2]
        ele_2=body[24][2]
        print(ele_1[0]-ele_2[0])
        # print(data)

def create_plot():
    x_vals = np.linspace(0, 100, 100) 
    y1_vals = np.zeros_like(x_vals)  
    y2_vals = np.zeros_like(x_vals)  
    y3_vals = np.zeros_like(x_vals)  
    plt.ion()  # 开启交互模式

    fig, ax = plt.subplots()

    line1, = ax.plot(x_vals, y1_vals, label='Curve 1',color='lightblue')   #ele1_y
    line2, = ax.plot(x_vals, y2_vals, label='Curve 2',color='lightcoral')  #plus
    line3, = ax.plot(x_vals, y3_vals, label='Curve 3',color='black') #ele2_y

    ax.set_xlim(0, 100)  # 设置X轴范围
    ax.set_ylim(-360, 360)  # 设置Y轴范围

    while True:
        global ele_1,ele_2
        y1_vals[:-1] = y1_vals[1:]  # 第一条曲线数据左移
        y1_vals[-1] = ele_1[0]  # 获取第一条曲线新数据

        y2_vals[:-1] = y2_vals[1:]  
        y2_vals[-1] = ele_1[0]-ele_2[0] 

        y3_vals[:-1] = y3_vals[1:]  
        y3_vals[-1] = ele_2[0] 

        line1.set_xdata(x_vals)  
        line1.set_ydata(y1_vals)  

        line2.set_xdata(x_vals) 
        line2.set_ydata(y2_vals)  

        line3.set_xdata(x_vals) 
        line3.set_ydata(y3_vals)  

        plt.title('Real-time Data Visualization')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.draw()
        plt.pause(0.1) 

if __name__ == "__main__":
    threading.Thread(target=parse_euler).start()
    time.sleep(1)
    threading.Thread(target=create_plot).start()
