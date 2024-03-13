import serial
import time

serial_port = 'com28' 
baud_rate = 9600  
timeout = 5  

def read_device_config():
    response = "" 
    try:
        with serial.Serial(serial_port, baud_rate, timeout=timeout) as ser:
            ser.write(b'cfgrd\r\n')  # 发送读取配置命令
            time.sleep(1)  # 稍等待一段时间让设备准备回复
            while True:
                chunk = ser.read(64)  # 尝试读取64字节的数据
                if not chunk:
                    break  # 如果没有读到数据，跳出循环
                response += chunk.decode('utf-8', errors='ignore')  # 将读取的数据添加到响应字符串中，忽略解码错误
            print("设备配置信息：")
            print(response)

    except serial.SerialException as e:
        print("无法打开串口：", str(e))

# 执行读取配置函数
read_device_config()
