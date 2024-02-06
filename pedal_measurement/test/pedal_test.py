import serial
import binascii
import csv
import time
import keyboard
from datetime import datetime

ser = serial.Serial('COM5', 9600, timeout=0.1)

data_to_send1 = b'\x01\x03\x00\x04\x00\x01\xC5\xCB'
data_to_send2 = b'\x02\x03\x00\x04\x00\x01\xC5\xF8'

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"pedal_{current_time}.csv"

with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp','pedal1', 'pedal2'])

    while True:
        if keyboard.is_pressed('q'):
            print("Exiting and saving file...")
            break

        ser.write(data_to_send1)
        response1 = ser.read(8)
        response1_dec = int(binascii.hexlify(response1[3:5]).upper(), 16)

        ser.write(data_to_send2)
        response2 = ser.read(8)
        response2_dec = int(binascii.hexlify(response2[3:5]).upper(), 16)
        print("Received data:", response1_dec, response2_dec)
        writer.writerow([time.time(),response1_dec, response2_dec])
ser.close()
