#编写者：cwt
#时间：2022/7/4 21:16
#盒子
import pygame
from source import setup,tools,constants

class Box(pygame.sprite.Sprite):
    def __init__(self,x,y,box_type,color=None):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.box_type=box_type
        # self.color=color
        self.frame_rects={
            (384,0,16,16),
            (400,0,16,16),
            (416,0,16,16),
            (432,0,16,16)
        }

        self.frames=[] #存储图像
        for frame_rect in self.frame_rects:
            self.frames.append(tools.get_image(setup.GRAPHICS['tile_set'],*frame_rect,(0,0,0),constants.BRICK_MULTI))

        self.frames_index=0
        self.image = self.frames[self.frames_index]
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y