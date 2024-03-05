import serial
import binascii
import time
from websocket import create_connection
import json

slave1_query = b'\x01\x03\x00\x00\x00\x01\x84\x0A' #查询左轮转向角度
slave2_query = b'\x02\x03\x00\x00\x00\x01\x84\x39' #查询右轮转向角度
slave1_set2zero = b'\x01\x06\x00\x08\x00\x01\xC9\xC8' #归零左轮转向角度
slave2_set2zero = b'\x02\x06\x00\x08\x00\x01\xC9\xFB' #归零左轮转向角度

def leftQueryAngle():   #查询左轮角度
    ser.write(slave1_query)
    response = ser.read(7)
    response_hex = binascii.hexlify(response[3:5]).upper()
    hex_str = response_hex.decode('utf-8')
    decimal_value = int(hex_str, 16)
    return float(decimal_value*360/4096)

def rightQueryAngle():   #查询右轮角度
    ser.write(slave2_query)
    response = ser.read(7)
    response_hex = binascii.hexlify(response[3:5]).upper()
    hex_str = response_hex.decode('utf-8')
    decimal_value = int(hex_str, 16)
    return float(decimal_value*360/4096)

def leftSetZero():   #置零左轮角度
    ser.write(slave1_set2zero)
    response = ser.read(8)

def rightSetZero():  #置零右轮角度
    ser.write(slave2_set2zero)
    response = ser.read(8)

def adjust_angle(angle):
    if 180 < angle <= 360:
        return angle - 360
    else:
        return angle
    
if __name__ == "__main__":

    com='com23'
    ser = serial.Serial(com, 9600, timeout=1)  
    leftSetZero()
    rightSetZero()

    steer_data=0
    ws = None
    try:
        ws = create_connection("ws://localhost:8886")
        print("Link to socket server")
    except:
        pass

    while(1):
        steer_data=adjust_angle(round(leftQueryAngle(),3))
        v = {"timestamp":time.time(), "steer": steer_data, "action":"steering"}
        ws.send(json.dumps(v))
        print(steer_data)