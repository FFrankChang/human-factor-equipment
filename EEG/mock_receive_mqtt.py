import sys
from os.path import join, dirname, realpath
import random
import paho.mqtt.client as mqtt
from datetime import datetime
import json
import time


def generate_array(size):
    return [random.randint(-99000000, 90000000) for _ in range(size)]
# first resolve an EEG stream on the lab network
print("looking for an AudioCaptureWin stream...")
# streams = pylsl.resolve_stream('type','NIRS')
print('success')
# create a new inlet to read from the stream
# inlet = pylsl.stream_inlet(streams[0])

final_data={
    'data':[],
    'timestamp':0
}

mqtt_host = "139.198.181.66"
mqtt_port = 14563
mqtt_client_id = "python_mqtt_eeg"
mqtt_topic = "YHEEG"
client = mqtt.Client(mqtt_client_id)
client.connect(mqtt_host, mqtt_port, 60)

while True:
	# get a new sample (you can also omit the timestamp part if you're not interested in it)
	# timestamp = inlet.pull_sample(sample)
    data_array=generate_array(24)	
    final_data['data']=json.dumps(data_array)
    final_data['timestamp']= int(datetime.now().timestamp() * 1000)
    client.publish(mqtt_topic, json.dumps(final_data).replace(' ',''))
    print(json.dumps(final_data).replace(' ',''))
