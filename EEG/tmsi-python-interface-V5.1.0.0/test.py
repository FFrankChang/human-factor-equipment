import socket

# 创建一个TCP/IP套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定套接字到本地地址和端口
server_address = ('localhost', 1234)
server_socket.bind(server_address)

# 开始监听传入的连接
server_socket.listen(5)  # 最多允许5个等待连接的客户端

print("等待连接...")
client_socket, client_address = server_socket.accept()
print("已连接到：", client_address)

while True:
    data = client_socket.recv(4096)  
    if not data:
        break  # 如果没有数据，退出循环
    print("接收到的数据：", data.decode('utf-8'))  # 假定数据是UTF-8编码的

# finally:
#     # 清理工作
#     client_socket.close()
#     server_socket.close()
