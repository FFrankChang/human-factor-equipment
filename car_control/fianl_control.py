import socket
import time
import struct
import websockets
import json
import pygame
import paho.mqtt.client as mqtt

def parse():
    format_string = '>6sIcblbbbbhh'
    segment_format = '>Ifffffff'
    data, addr = udp_socket.recvfrom(4096)  # 一次最多接收4096字节的数据
    header = struct.unpack(format_string, data[0:24])
    body = []
    for i in range(63):
        segment_body=[]
        pos = []
        ori = []
        begin_flag = 24+ i*32
        end_flag = 23 + 32 + i*32 + 1
        # print(i,': ',begin_flag,end_flag)
        segment_data = struct.unpack(segment_format,data[begin_flag:end_flag])
        id = segment_data[0]
        for j in range(1,4):
            pos.append(segment_data[j])
        for k in range(4,8):
            ori.append(segment_data[k])
        segment_body.append(id)
        segment_body.append(pos)
        segment_body.append(ori)
        body.append(segment_body)

    global r_thumb,r_index,r_middle,r_ring,r_little,l_thumb,l_index,l_middle,l_ring,l_little
    r_thumb = body[46][2][1]
    r_index = body[50][2][0]
    r_middle = body[54][2][0]
    r_ring = body[58][2][0]
    r_little = body[62][2][0]

    if(body[26][2][1]<0): body[26][2][1]=-body[26][2][1]
    l_thumb = body[26][2][1]
    l_index = body[30][2][1]
    l_middle = body[34][2][1]
    l_ring = body[38][2][1]
    l_little = body[42][2][1]
    # print(data)
    return 


def hand_status(r1,r2,r3,r4,r5,l1,l2,l3,l4,l5):

    if(abs(r_thumb-r1)>0.2):
        r_thumb_status=1
    else:
        r_thumb_status=0
    if(abs(r_index-r2)>0.2):
        r_index_status=1
    else:
        r_index_status=0
    if(abs(r_middle-r3)>0.2):
        r_middle_status=1
    else:
        r_middle_status=0
    if(abs(r_ring-r4)>0.2):
        r_ring_status=1
    else:
        r_ring_status=0
    if(abs(r_little-r5)>0.2):
        r_little_status=1
    else:
        r_little_status=0
    if(abs(l_thumb-l1)>0.2):
        l_thumb_status=1
    else:
        l_thumb_status=0
    if(abs(l_index-l2)>0.2):
        l_index_status=1
    else:
        l_index_status=0
    if(abs(l_middle-l3)>0.2):
        l_middle_status=1
    else:
        l_middle_status=0
    if(abs(l_ring-l4)>0.2):
        l_ring_status=1
    else:
        l_ring_status=0
    if(abs(l_little-l5)>0.2):
        l_little_status=1
    else:
        l_little_status=0
    #turn_left
    if(l_thumb_status==0 and l_index_status==0 and l_middle_status==1 and l_ring_status==1 and l_little_status==1 ):
        return 0
    #go
    if(r_thumb_status==1 and r_index_status==1 and r_middle_status==1 and r_ring_status==1 and r_little_status==1 ):
        return 1
    #turn_right
    if(r_thumb_status==0 and r_index_status==0 and r_middle_status==1 and r_ring_status==1 and r_little_status==1 ):
        return 2
    if(l_thumb_status==1 and l_index_status==1 and l_middle_status==1 and l_ring_status==1 and l_little_status==1 ):
        return 3
    else:
        return 4

def print_status():
    # print(f"Right Hand:  Index={round(l_index, 2)}")

    # print(f"Right Hand: Thumb={round(r_thumb, 2)}, Index={round(r_index, 2)}, Middle={round(r_middle, 2)}, Ring={round(r_ring, 2)}, Little={round(r_little, 2)}")
    print(f"Left Hand: Thumb={round(l_thumb, 2)}, Index={round(l_index, 2)}, Middle={round(l_middle, 2)}, Ring={round(l_ring, 2)}, Little={round(l_little, 2)}")

def turn_left():
    final_data={
    'turn_left':1,
    'turn_right':0,
    'go_forward':0,
    'stop':0,
    }
    client.publish(mqtt_topic, json.dumps(final_data))
    print("turn_left")

    pygame.mixer.init()
    pygame.mixer.music.load('./car_control/resource/left.mp3')
    pygame.mixer.music.play()
    for _ in range(5):  # 闪烁5次
        screen.fill((255, 255, 255))  # 白屏
        pygame.display.flip()
        time.sleep(0.5)
        text = font.render('识别到左转意图', True, (0, 0, 0))
        text_rect = text.get_rect(center=(950, 1000))
        screen.blit(text, text_rect)
        image = pygame.image.load('./car_control/resource/left.png')
        screen.blit(image, (700, 200))
        pygame.display.flip()
        time.sleep(0.5)
    
def turn_right():
    final_data={
    'turn_left':0,
    'turn_right':1,
    'go_forward':0,
    'stop':0,
    }
    client.publish(mqtt_topic, json.dumps(final_data))
    print("turn_right")
    
    pygame.mixer.init()
    pygame.mixer.music.load('./car_control/resource/right.mp3')
    pygame.mixer.music.play()
    for _ in range(5):  # 闪烁5次
        screen.fill((255, 255, 255))  # 白屏
        pygame.display.flip()
        time.sleep(0.5)
        text = font.render('识别到右转意图', True, (0, 0, 0))
        text_rect = text.get_rect(center=(950, 1000))
        screen.blit(text, text_rect)
        image = pygame.image.load('./car_control/resource/right.png')
        screen.blit(image, (700, 200))
        pygame.display.flip()
        time.sleep(0.5)

def go():
    final_data={
    'turn_left':0,
    'turn_right':0,
    'go_forward':1,
    'stop':0,
    }
    client.publish(mqtt_topic, json.dumps(final_data))
    print("go_forward")
    
    pygame.mixer.init()
    pygame.mixer.music.load('./car_control/resource/go.mp3')
    pygame.mixer.music.play()
    for _ in range(5):  # 闪烁5次
        screen.fill((255, 255, 255))  # 白屏
        pygame.display.flip()
        time.sleep(0.5)
        text = font.render('识别到直行意图', True, (0, 0, 0))
        text_rect = text.get_rect(center=(950, 1000))
        screen.blit(text, text_rect)
        image = pygame.image.load('./car_control/resource/go.png')
        screen.blit(image, (700, 200))
        pygame.display.flip()
        time.sleep(0.5)

def stop():
    final_data={
    'turn_left':0,
    'turn_right':0,
    'go_forward':0,
    'stop':1,
    }
    client.publish(mqtt_topic, json.dumps(final_data))
    print("stop")
    
    pygame.mixer.init()
    pygame.mixer.music.load('./car_control/resource/stop.mp3')
    pygame.mixer.music.play()
    for _ in range(5):  # 闪烁5次
        screen.fill((255, 255, 255))  # 白屏
        pygame.display.flip()
        time.sleep(0.5)
        text = font.render('疲劳驾驶，靠边停车', True, (0, 0, 0))
        text_rect = text.get_rect(center=(950, 1000))
        screen.blit(text, text_rect)
        image = pygame.image.load('./car_control/resource/stop.png')
        screen.blit(image, (700, 200))
        pygame.display.flip()
        time.sleep(0.5)


# #eye_track
# def receive():
#     p_status = 1
#     status = 1 
#     flag=0
#     if(status==1 and p_status==status):
#         flag+=1
#     else:
#         flag=0

#     if(flag>20):
#         print('stop')
#         flag = 0
#     stop()

r_thumb = -0.93
r_index = -0.2
r_middle = -0.1
r_ring = -0.15
r_little = -0.17
l_thumb = 0.94
l_index = -0.49
l_middle = -0.46
l_ring = -0.43
l_little = -0.42

r_thumb_r = 0.1
r_index_r = 0.8
r_middle_r = 0.8
r_ring_r = 0.8
r_little_r = 0.7
l_thumb_r = 0.1
l_index_r = 0.1
l_middle_r = 0.
l_ring_r = 0.0
l_little_r = 0.1

r_thumb_status = 0
r_index_status = 0
r_middle_status = 0
r_ring_status = 0
r_little_status = 0
l_thumb_status = 0
l_index_status = 0
l_middle_status = 0
l_ring_status = 0
l_little_status = 0

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_address = ('localhost', 9763)
udp_socket.bind(local_address)
server_address = ('192.168.31.122', 9763)
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mqtt_host = "139.198.181.66"
mqtt_port = 14563
mqtt_client_id = "human_factor_control"
mqtt_topic = "human_factor"
client = mqtt.Client(mqtt_client_id)
client.connect(mqtt_host, mqtt_port, 60)

pygame.init()
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
font = pygame.font.Font('./car_control/resource/1.ttf', 36)

p_status = 4

while 1:
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        parse()
        # print_status()
        # time.sleep(3)
        # hand_status(r_thumb_r,r_index_r,r_middle_r,r_ring_r,r_little_r,l_thumb_r ,l_index_r,l_middle_r,l_ring_r,l_little_r)


        if(hand_status(r_thumb_r,r_index_r,r_middle_r,r_ring_r,r_little_r,l_thumb_r ,l_index_r,l_middle_r,l_ring_r,l_little_r)!=p_status):
            
            if(hand_status(r_thumb_r,r_index_r,r_middle_r,r_ring_r,r_little_r,l_thumb_r ,l_index_r,l_middle_r,l_ring_r,l_little_r)==0):
                turn_right()
            elif(hand_status(r_thumb_r,r_index_r,r_middle_r,r_ring_r,r_little_r,l_thumb_r ,l_index_r,l_middle_r,l_ring_r,l_little_r)==1):
                go()
            elif(hand_status(r_thumb_r,r_index_r,r_middle_r,r_ring_r,r_little_r,l_thumb_r ,l_index_r,l_middle_r,l_ring_r,l_little_r)==2):
                turn_left()
            elif(hand_status(r_thumb_r,r_index_r,r_middle_r,r_ring_r,r_little_r,l_thumb_r ,l_index_r,l_middle_r,l_ring_r,l_little_r)==3):
                stop()
        p_status=hand_status(r_thumb_r,r_index_r,r_middle_r,r_ring_r,r_little_r,l_thumb_r ,l_index_r,l_middle_r,l_ring_r,l_little_r)
        screen.fill((255, 255, 255))
        pygame.display.flip()


    # print(hand_status(r_thumb_r,r_index_r,r_middle_r,r_ring_r,r_little_r,l_thumb_r ,l_index_r,l_middle_r,l_ring_r,l_little_r))
    screen.fill((255, 255, 255))
    pygame.display.flip()