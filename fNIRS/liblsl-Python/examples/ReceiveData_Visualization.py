import sys; sys.path.append('..')  # make sure that pylsl is found (note: in a normal program you would bundle pylsl with the program)
import pylsl
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import threading
import time

def create_plot():
    x_vals = np.linspace(0, 10, 100)  # X轴数据范围
    y1_vals = np.zeros_like(x_vals)  # 初始化第一条曲线的Y轴数据为0
    y2_vals = np.zeros_like(x_vals)  # 初始化第二条曲线的Y轴数据为0
    plt.ion()  # 开启交互模式

    fig, ax = plt.subplots()

    line1, = ax.plot(x_vals, y1_vals, label='Curve 1',color='lightcoral')  # 创建第一条曲线对象
    line2, = ax.plot(x_vals, y2_vals, label='Curve 2',color='lightblue')  # 创建第二条曲线对象

    ax.set_xlim(0, 10)  # 设置X轴范围
    ax.set_ylim(-100, 100)  # 设置Y轴范围


    while True:
        global sample
        y1_vals[:-1] = y1_vals[1:]  # 第一条曲线数据左移
        y1_vals[-1] = sample[32]  # 获取第一条曲线新数据

        y2_vals[:-1] = y2_vals[1:]  # 第二条曲线数据左移
        y2_vals[-1] = sample[33] # 获取第二条曲线新数据

        # 样条插值
        x_smooth = np.linspace(x_vals.min(), x_vals.max(), 1000)  
        spline1 = make_interp_spline(x_vals, y1_vals)
        y1_smooth = spline1(x_smooth)

        spline2 = make_interp_spline(x_vals, y2_vals)
        y2_smooth = spline2(x_smooth)

        line1.set_xdata(x_smooth)  # 更新第一条曲线X轴数据
        line1.set_ydata(y1_smooth)  # 更新第一条曲线Y轴数据

        line2.set_xdata(x_smooth)  # 更新第二条曲线X轴数据
        line2.set_ydata(y2_smooth)  # 更新第二条曲线Y轴数据

        plt.title('Real-time Data Visualization')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.draw()  # 绘制图形
        plt.pause(0.1)  # 暂停一段时间

def receive():
    # first resolve an EEG stream on the lab network
    print("looking for an AudioCaptureWin stream...")
    streams = pylsl.resolve_stream('type','NIRS')
    # create a new inlet to read from the stream
    inlet = pylsl.stream_inlet(streams[0])
    global sample
    sample = pylsl.vectorf()
    while True:
        # get a new sample (you can also omit the timestamp part if you're not interested in it)
        timestamp = inlet.pull_sample(sample)
        print(sample)
        print(type(sample))
        # time.sleep(10)


def main():
    threading.Thread(target=receive).start()
    threading.Thread(target=create_plot).start()

main()