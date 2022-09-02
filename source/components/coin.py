#编写者：cwt
#时间：2022/7/4 21:17
#金币

import pygame
from source import setup,tools,constants




class FlashingCoin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  #金币类继承精灵类，与主角有千丝万缕的联系，例如发生碰撞消失等
        self.frames = []
        self.frame_index = 0
        frame_rects = [(1,160,5,8),(9,160,5,8),(17,160,5,8),(9,160,5,8)]
        self.load_frames(frame_rects)
        self.image=self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x=280
        self.rect.y=58
        self.timer = 0 #计时器

    def load_frames(self,frame_rects):
        sheet = setup.GRAPHICS['item_objects']
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(sheet,*frame_rect,(0,0,0),constants.BG_MULTI))  #*frame_rect解包，把该元组放入时分解成四个变量

    def update(self):
        self.current_time = pygame.time.get_ticks() #获取当前时间
        frame_durations = [375,125,125,125] #停留时间

        if self.timer == 0:
            self.timer =self.current_time
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index +=1
            self.frame_index %=4
            self.timer =self.current_time

        self.image=self.frames[self.frame_index]