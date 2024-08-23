from pylsl import StreamInlet, resolve_stream
import time
import json
import keyboard
from datetime import datetime
import paho.mqtt.client as mqtt

final_data={
    'data':[],
    'timestamp':0
}
last_time = time.time()
frame_count = 0
update_interval = 1 

streams = resolve_stream('name', 'SAGA')
inlet = StreamInlet(streams[0])
frame_count = 0

mqtt_host = "192.168.1.179"
mqtt_port = 1883
mqtt_client_id = "python_mqtt_eeg"
mqtt_topic = "YHEEG"
client = mqtt.Client(mqtt_client_id)
client.connect(mqtt_host, mqtt_port, 60)

while True:
    if keyboard.is_pressed('esc'):
        print("Escape key pressed, exiting loop")
        break
    # Pull sample from the inlet
    sample, timestamp = inlet.pull_sample()
    current_time = time.time()

    if timestamp:
        final_data['data']=json.dumps(sample)
        final_data['timestamp']= int(datetime.now().timestamp() * 1000)
        client.publish(mqtt_topic, json.dumps(final_data).replace(' ',''))
        frame_count += 1

    if current_time - last_time >= update_interval:
        fps = frame_count / (current_time - last_time)
        print(f"Current Sample Rate: {int(fps)}")
        frame_count = 0
        last_time = current_time

