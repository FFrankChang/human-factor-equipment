"""
罗技G29数据读取
各个轴和按钮的序号请根据官方的demo查看或者根据此程序尝试
各个轴的取值范围是【-1,1】
按钮按下即为1.否则为0
"""
import pygame
import time

class JSManager:
    def __init__(self):
        pygame.init()
        try:
            self.js = pygame.joystick.Joystick(0)
        except:
            print('could not find joystick')
            exit()
        self.js.init()
        self.axes = self.js.get_numaxes()
        self.buttons = self.js.get_numbuttons()   
        self.vel=0.0

    def update_axes(self):
        # get joystick values
        # pygame.event.get is needed to update axis values
        pygame.event.get()
        axes_values = []
        # self.js.init()
        for a in range(self.axes):
            axis = self.js.get_axis(a)
            axes_values.append(axis)
        return axes_values

    def update_single_button(self, b):
        button = self.js.get_button(b)
        print(button)
        return button

    def update_buttons(self):
        # get button presses
        pygame.event.get()
        button_presses = []
        for b in range(self.buttons):
            button = self.js.get_button(b)
            button_presses.append(button)
        return button_presses

    def directionToSendNum(self,num):
        return int(90-55*num)

    def velToSendNum(self,acc,deacc):
        self.vel = abs(deacc-acc)*150
        if self.vel<1:
            self.vel = 0
        if self.vel>255:
            self.vel=255
        return int(self.vel)

# if __name__ == "__main__":
#     '''testing code'''
#     js = JSManager()
#     while True:
#         vals = js.update_axes()
#         buts = js.update_buttons()
#         print('vals: ',*vals)
#         print('buttons: ',*buts)
#         time.sleep(1)
