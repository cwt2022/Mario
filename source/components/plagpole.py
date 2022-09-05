#编写者：cwt
#时间：2022/9/5 11:32
#旗子
import pygame
from source import setup,tools,constants
class Flag(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frame_index = 0
        frame_rects = [(128, 32, 16, 16)]
        self.load_frames(frame_rects)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def load_frames(self,frame_rects):
        sheet = setup.GRAPHICS['item_objects']
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(sheet,*frame_rect,(0,0,0),constants.BG_MULTI))  #*frame_rect解包，把该元组放入时分解成四个变量

    # def draw(self, surface):
    #
    #     surface.blit(self.image, (self.rect.x,self.rect.y))

class Pole(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frame_index = 0
        frame_rects = [(263,144,2,16)]
        self.load_frames(frame_rects)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def load_frames(self,frame_rects):
        sheet = setup.GRAPHICS['tile_set']
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(sheet,*frame_rect,(0,0,0),constants.BG_MULTI))  #*frame_rect解包，把该元组放入时分解成四个变量

    # def draw(self, surface):
    #     # surface.blit(self.create_lable('GIVE ME A LITTLE HEATRT~',size=60),(100,400))
    #
    #
    #
    #     surface.blit(self.image, (self.rect.x,self.rect.y))  # 画出金币

class Finial(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frame_index = 0
        frame_rects = [(228,120,8,8)]
        self.load_frames(frame_rects)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def load_frames(self,frame_rects):
        sheet = setup.GRAPHICS['tile_set']
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(sheet,*frame_rect,(0,0,0),constants.BG_MULTI))  #*frame_rect解包，把该元组放入时分解成四个变量
    #
    # def draw(self, surface):
    #     surface.blit(self.image, (self.rect.x, self.rect.y))
