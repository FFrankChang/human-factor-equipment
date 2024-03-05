import sys; sys.path.append('..')  # make sure that pylsl is found (note: in a normal program you would bundle pylsl with the program)
import pylsl
import socket
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# first resolve an EEG stream on the lab network
print("looking for an AudioCaptureWin stream...")
streams = pylsl.resolve_stream('type','NIRS')
print(1)
# create a new inlet to read from the stream
inlet = pylsl.stream_inlet(streams[0])
final_data={
    'data':[]
}
sample = pylsl.vectorf()

mqtt_host = "192.168.1.159"
mqtt_port = 1883
mqtt_client_id = "python_mqtt"
mqtt_topic = "YHFNIRS"
client = mqtt.Client(mqtt_client_id)
client.connect(mqtt_host, mqtt_port, 60)

while True:
	# get a new sample (you can also omit the timestamp part if you're not interested in it)
	timestamp = inlet.pull_sample(sample)	
	final_data['data']=list(sample)
	final_data['timestamp']= int(datetime.now().timestamp() * 1000)
	client.publish(mqtt_topic, json.dumps(final_data).replace(' ',''))
	print(final_data)