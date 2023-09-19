import cv2
from pyzbar.pyzbar import decode

# 读取图片
image_path = 'path_to_your_image.jpg'  # 替换为你的图片路径
image = cv2.imread(image_path)

# 使用pyzbar库解码二维码
decoded_objects = decode(image)

for obj in decoded_objects:
    if obj.type == 'QRCODE':
        # 获取二维码数据
        data = obj.data.decode('utf-8')
        print("二维码数据:", data)

        # 获取二维码的四个角点坐标
        points = obj.polygon
        if len(points) >= 4:
            # 绘制二维码的边框
            for j in range(4):
                cv2.line(image, points[j], points[(j+1) % 4], (0, 255, 0), 3)

# 显示图片和二维码信息
cv2.imshow('QR Code Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
