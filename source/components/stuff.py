#编写者：cwt
#时间：2022/7/4 21:20
#物品，大杂项
import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h,name):
        '''每个物品都有了隐形的轮廓，方便使用，方便进行碰撞检测'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h)).convert()
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.name = name

class Checkpoint(Item):
    def __init__(self, x, y, w, h, checkint_type, enemy_groupid=None, name='checkpoint'):
        Item.__init__(self,x,y,w,h,name)
        self.checkpoint_type = checkint_type
        self.enemy_groupid = enemy_groupid

