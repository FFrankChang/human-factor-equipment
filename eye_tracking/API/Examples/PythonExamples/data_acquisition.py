from __future__ import absolute_import
from __future__ import print_function

import json
import socket
import socket_client
import os
import time
import datetime
import keyboard
import paho.mqtt.client as mqtt


def main():
    mqtt_host = "192.168.1.179"
    mqtt_port = 1883
    mqtt_client_id = "python_mqtt_eye"
    mqtt_topic = "YHEYE"
    client = mqtt.Client(mqtt_client_id)
    client.connect(mqtt_host, mqtt_port, 60)

    client = socket_client.SocketClient()
    client.set_output_data_file(r'D:\Frank_Projects\smart_eye_scripts\API\include\data_output.json')
    client.set_data_types_file(r'D:\Frank_Projects\smart_eye_scripts\API\include\data_types.json')
    client.set_output_file(os.path.join(r"D:\Frank_Projects\smart_eye_scripts\API\Log", 'socket_log.json'))
    result = client.init("127.0.0.1", 5001, 'udp')
    
    if result:
        client.set_start_frame(-1)
        client.set_stop_frame(-1)
        client.connect()

        last_time = time.time()
        frame_count = 0
        update_interval = 1 

        while not keyboard.is_pressed('esc'): 
            client.receive()
            current_time = time.time()
            
            if client.frame_number in client.json_data:
                client.json_data[client.frame_number]['FrameNumber'] = client.frame_number
                client.json_data[client.frame_number]['UserTimeStamp'] =time.time()
                eye_data = json.dumps(client.json_data[client.frame_number])
                client.publish(mqtt_topic, eye_data.replace(' ','')) # send MQTT data
                # print(eye_data)
                frame_count += 1

            if current_time - last_time >= update_interval:
                fps = frame_count / (current_time - last_time)
                print(f"Current FPS: {fps:.2f}")
                frame_count = 0
                last_time = current_time

        print("Exiting program.")

if __name__ == "__main__":
    main()
