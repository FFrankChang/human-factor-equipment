import cv2

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 读取一帧图像
ret, frame = cap.read()

# 检查图像是否成功读取
if not ret:
    print("无法读取图像")
    cap.release()
    exit()

# # 保存图像为文件
# cv2.imwrite("captured_image.jpg", frame)

# 关闭摄像头
cap.release()

# 展示拍摄的图像
cv2.imshow("Captured Image", frame)

# 等待用户按下任意键后关闭窗口
cv2.waitKey(0)

# 关闭所有OpenCV窗口
cv2.destroyAllWindows()
