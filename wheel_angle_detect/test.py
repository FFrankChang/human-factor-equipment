import cv2
from pyzbar.pyzbar import decode

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
            print("points:", points)
            
            if len(points) >= 4:
                for j in range(4):
                    cv2.line(frame, points[j], points[(j+1) % 4], (0, 255, 0), 3)
                    
    # data, box, rectified = qrcode.detectAndDecode(frame)
    # show_data = str(box)
    # if data:
    #     cv2.putText(frame, show_data, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    #     print(box)
        # cv2.rectangle(frame,(box[0],box[1]),(box[2],box[3]),(0,0,255),5)
    
    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
