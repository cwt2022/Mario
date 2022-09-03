#编写者：cwt
#时间：2022/7/4 21:19
#强化
import pygame
from source import setup,tools,constants

def create_powerup(centerx,centery,type):
    """create powerup based on type and mario state"""
    return Mushroom(centerx,centery)

class Powerup(pygame.sprite.Sprite):
    def __init__(self,centerx,centery,frame_rects):
        pygame.sprite.Sprite.__init__(self)
        self.frames=[]
        self.frames_index=0
        for frame_rects in frame_rects:
            self.frames.append(tools.get_image(setup.GRAPHICS['item_objects'],*frame_rects,(0,0,0),2.5))
        self.image=self.frames[self.frames_index]
        self.rect=self.image.get_rect()
        self.rect.centerx=centerx
        self.rect.centery=centery

class Mushroom(Powerup):
    def __init__(self,centerx,centery):
        Powerup.__init__(self,centerx,centery,[(0,0,16,16)])

class Fireball(Powerup):
    pass


class LifeMushroom(Powerup):
   pass


class Star(Powerup):
   pass
