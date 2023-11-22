from config import cal_speed,cal_brake,SPEED_RANGE,BRAKE_RANGE
from hipnuc_module import *
from datetime import datetime
import json
import time
import csv
import socket
import sqlite3

# 01. init a sqlite3 database

t = datetime.now()
filename = t.strftime('%Y-%m-%d-%H-%M-%S')

outfile_path = 'data/%s.csv' %(filename)
print(outfile_path)

file_obj = open(outfile_path, 'w+')
# Record config file data
file_obj.write(json.dumps(SPEED_RANGE)+"\n")
file_obj.write(json.dumps(BRAKE_RANGE)+"\n")

# 02.connect to sensor
# start_get_serial_data()
def start_get_serial_data():
    global file_obj
    hip_gas = hipnuc_module('./config/config_gas.json')
    hip_brake = hipnuc_module('./config/config_brake.json')
    try: 
        while True:
            try:
                gas_data = hip_gas.get_module_data(10)
                brake_data = hip_brake.get_module_data(10)
                # package and send data
                gas_num = gas_data['euler'][0]['Pitch']
                brake_num = brake_data['euler'][0]['Pitch']
                v2 = "%s,%s,%s\n" %(time.time(), cal_speed(gas_num),cal_brake(brake_num))
                print(v2)
                file_obj.write(v2)
            except:
                print("Error")
                gas_data.close()
                brake_data.close()
                file_obj.close()

    except KeyboardInterrupt:
        print("Serial is closed.")
        gas_data.close()
        brake_data.close()
        file_obj.close()


