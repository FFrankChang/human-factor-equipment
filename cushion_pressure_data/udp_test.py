import socket
import time

HOST = '0.0.0.0'  
PORT = 9763  
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Listening for data on {HOST}:{PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(4096)
        if addr[0] == '192.168.3.3':
            print(data.decode())
        else:
            print(f"Received message from unknown source: {addr}")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    sock.close()
