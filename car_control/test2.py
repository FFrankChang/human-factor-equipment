import pygame
import time

# 初始化pygame
pygame.init()

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
font = pygame.font.Font('./car_control/1.ttf', 36)



a = 0

# 设置B的操作
def perform_B():
    pygame.mixer.init()
    pygame.mixer.music.load('./car_control/left.mp3')
    pygame.mixer.music.play()
    for _ in range(5):  # 闪烁5次
        screen.fill((255, 255, 255))  # 白屏
        pygame.display.flip()
        time.sleep(0.5)
        text = font.render('识别到左转意图', True, (0, 0, 0))
        text_rect = text.get_rect(center=(950, 1000))
        screen.blit(text, text_rect)
        image = pygame.image.load('./car_control/left.png')
        screen.blit(image, (700, 200))
        pygame.display.flip()
        time.sleep(0.5)


# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 在这里检查a的值
    if a == 10:
        perform_B()


    # 更新屏幕
    screen.fill((255, 255, 255))
    pygame.display.flip()

    # 模拟a的变化
    a += 1

# 退出pygame
pygame.quit()