import cv2
from pyzbar.pyzbar import decode

raw_data={
        1:[0,0],
        2:[0,0],
        3:[0,0],
        4:[0,0],
        }

def  location(raw_data):
    loc = {
        1:[0,0],
        2:[0,0],
        3:[0,0],
        4:[0,0],
    }
    x_avg=0
    y_ayg=0
    sum_x=0
    sum_y=0
    for i in raw_data:
        # print (i)
        sum_x = sum_x + raw_data[i][0]
        sum_y = sum_y + raw_data[i][1] 
    x_avg = sum_x/4
    y_avg = sum_y/4
    for i in raw_data:
        if raw_data[i][0]-x_avg <0 and raw_data[i][1]-y_avg>0:
            loc[1]=raw_data[i]
        elif raw_data[i][0]-x_avg >0 and raw_data[i][1]-y_avg>0:
            loc[2]=raw_data[i]
        elif raw_data[i][0]-x_avg >0 and raw_data[i][1]-y_avg<0:
            loc[3]=raw_data[i]
        elif raw_data[i][0]-x_avg <0 and raw_data[i][1]-y_avg<0:
            loc[4]=raw_data[i]
    return loc

def angle_detect(loc,left,right,r,l):
    mid = (r+l)/2
    angle=0
    if loc[1][0]==0:
        return 0
    if  abs((loc[2][0] +loc[4][0]) -2*mid) <4:
        return 0
    elif ((loc[2][0] +loc[4][0]) -2*mid) <0:
        angle = (loc[4][0]-r)/(mid-left) 
    elif ((loc[2][0] +loc[4][0]) -2*mid) >0:
        angle = (loc[2][0]-l)/(right-mid)
    if 1.76*angle>1:
        return 1
    if 1.76*angle<1:
        return -1
    return 1.76*angle


cap = cv2.VideoCapture(0)
qrcode = cv2.QRCodeDetector()  
if not cap.isOpened():
    print("无法打开摄像头")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取画面")
        break
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            data = obj.data.decode('utf-8')
            points = obj.polygon
            # print("point1:",points[0].x)
            # print("point2:",type(points[1]))
            if len(points) >= 4:
                for j in range(4):
                    raw_data[j+1][0]=points[j].x
                    raw_data[j+1][1]=points[j].y
                    cv2.line(frame, points[j], points[(j+1) % 4], (0, 255, 0), 3)
            loc=location(raw_data)
            print(loc)
            # print(angle_detect(loc,70,608,220,438)) #左极限，右极限，左中，右中
    cv2.imshow('Camera Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()