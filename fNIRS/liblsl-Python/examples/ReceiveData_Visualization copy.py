import matplotlib.pyplot as plt
import numpy as np

def create_plots():
    x_vals = np.linspace(0, 10, 100)  # X轴数据范围
    y1_vals = np.zeros_like(x_vals)  # 初始化第一条曲线的Y轴数据为0
    y2_vals = np.zeros_like(x_vals)  # 初始化第二条曲线的Y轴数据为0
    y3_vals = np.zeros_like(x_vals)  # 初始化第三条曲线的Y轴数据为0
    y4_vals = np.zeros_like(x_vals)  # 初始化第四条曲线的Y轴数据为0
    
    plt.ion()  # 开启交互模式

    fig, axes = plt.subplots(2, 1, figsize=(8, 6))  # 创建两个子图，2行1列
    
    ax1, ax2 = axes  # 分别获取两个子图的句柄

    line1, = ax1.plot(x_vals, y1_vals, label='Curve 1', color='lightcoral')  # 在第一个子图上创建第一条曲线对象
    line2, = ax1.plot(x_vals, y2_vals, label='Curve 2', color='lightblue')  # 在第一个子图上创建第二条曲线对象
    ax1.set_xlim(0, 10)  # 设置第一个子图的X轴范围
    ax1.set_ylim(-100, 100)  # 设置第一个子图的Y轴范围
    ax1.set_title('Graph 1')  # 设置第一个子图的标题
    
    line3, = ax2.plot(x_vals, y3_vals, label='Curve 3', color='lightgreen')  # 在第二个子图上创建第三条曲线对象
    line4, = ax2.plot(x_vals, y4_vals, label='Curve 4', color='lightcoral')  # 在第二个子图上创建第四条曲线对象
    ax2.set_xlim(0, 10)  # 设置第二个子图的X轴范围
    ax2.set_ylim(-100, 100)  # 设置第二个子图的Y轴范围
    ax2.set_title('Graph 2')  # 设置第二个子图的标题
    
    plt.tight_layout()  # 自动调整子图布局
    
    while True:
        global sample
        
        # 更新第一个子图的数据
        y1_vals[:-1] = y1_vals[1:]
        y1_vals[-1] = sample[0]
        
        y2_vals[:-1] = y2_vals[1:]
        y2_vals[-1] = sample[1]
        
        line1.set_ydata(y1_vals)
        line2.set_ydata(y2_vals)
        
        # 更新第二个子图的数据
        y3_vals[:-1] = y3_vals[1:]
        y3_vals[-1] = sample[2]
        
        y4_vals[:-1] = y4_vals[1:]
        y4_vals[-1] = sample[3]
        
        line3.set_ydata(y3_vals)
        line4.set_ydata(y4_vals)
        
        plt.draw()
        plt.pause(0.1)

# 示例数据（用于模拟sample数据）
sample = [0] * 4

# 调用函数启动实时数据可视化
create_plots()
