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
        self.origin_y=centery-self.rect.height/2  #记录出生时的顶部的Y

        self.x_vel =0
        self.direction=1 #facing rinht 一出生就朝右
        self.y_vel=-1
        self.gravity =1
        self.max_y_vel=8

    def update_position(self, level):
        self.rect.x += self.x_vel
        self.check_x_collisions(level)  # x方向碰撞检测
        self.rect.y += self.y_vel
        self.check_y_collisions(level)  # y方向碰撞检测
        if self.rect.x< 0 or self.rect.y>constants.SCREEN_H:
            self.kill()

    def check_x_collisions(self, level):
        sprite = pygame.sprite.spritecollideany(self, level.ground_items_group)
        if sprite:
            # self.direction =1 if self.direction == 0 else 0
            if self.direction:  # 向右
                self.direction = 0
                self.rect.right = sprite.rect.left
            else:
                self.direction = 1
                self.rect.left = sprite.rect.right
            self.x_vel *= -1



    def check_y_collisions(self, level):
        # print('yyys')
        check_group = pygame.sprite.Group(level.ground_items_group, level.brick_group, level.box_group)
        sprite = pygame.sprite.spritecollideany(self, check_group)
        if sprite:
            # print('野怪头部{0}，野怪脚底{2},碰撞物体头部{3}',self.rect.top,self.rect.bottom,sprite.rect.top)
            if self.rect.top < sprite.rect.top:  # ??从上往下掉落  已解决：坐标轴原因
                self.rect.bottom = sprite.rect.top
                self.y_vel = 0
                self.state = 'walk'
        #print('下落检测')
        level.check_will_fail(self)


class Mushroom(Powerup):
    def __init__(self,centerx,centery):
        Powerup.__init__(self,centerx,centery,[(0,0,16,16)])
        self.x_vel = 2
        self.state = 'grow'
        self.name='mushroom'

    def update(self,level):#目的是在自己的更新方法中完成对物体的碰撞检测

        if self.state =='grow':
            self.rect.y += self.y_vel
            if self.rect.bottom < self.origin_y:

                self.state='walk' #傻了傻了。。用俩等报bug了

        elif self.state=='walk':
            pass
        elif self.state == 'fall':
            if self.y_vel < self.max_y_vel:
                self.y_vel +=self.gravity

        if self.state !='grow':
            self.update_position(level)


class Fireball(Powerup):
    pass


class LifeMushroom(Powerup):
   pass


class Star(Powerup):
   pass
