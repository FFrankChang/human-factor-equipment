import sys; sys.path.append('..')  # make sure that pylsl is found (note: in a normal program you would bundle pylsl with the program)
import pylsl
import socket
import json

# first resolve an EEG stream on the lab network
print("looking for an AudioCaptureWin stream...")
streams = pylsl.resolve_stream('type','NIRS')
print(1)
# create a new inlet to read from the stream
inlet = pylsl.stream_inlet(streams[0])
final_data={
    'type':'fnirs',
    'data':[]
}
sample = pylsl.vectorf()

server_ip = '192.168.31.122'
server_port = 9763  # 服务器的端口号
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	# get a new sample (you can also omit the timestamp part if you're not interested in it)
	timestamp = inlet.pull_sample(sample)	
	final_data['data']=list(sample)
	print(final_data)
	udp_socket.sendto(json.dumps(final_data).encode(), (server_ip, server_port))