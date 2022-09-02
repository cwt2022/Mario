#编写者：cwt
#时间：2022/7/4 21:16
#砖块
import pygame
from source import setup,tools,constants

class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y,brick_type,color=None):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.brick_type=brick_type
        # self.color=color
        bright_rect_frames=[(16,0,16,16),(48,0,16,16)]
        daek_rect_frames=[(16,32,16,16),(48,32,16,16)]

        if not color:
            self.frame_rects=bright_rect_frames
        else:
            self.frame_rects=daek_rect_frames

        self.frames=[] #存储图像
        for frame_rect in self.frame_rects:
            self.frames.append(tools.get_image(setup.GRAPHICS['tile_set'],*frame_rect,(0,0,0),constants.BRICK_MULTI))

        self.frames_index=0
        self.image = self.frames[self.frames_index]
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y