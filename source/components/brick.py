#编写者：cwt
#时间：2022/7/4 21:16
#砖块
import pygame
from source import setup,tools,constants
from source.components.powerup import create_powerup
from source.components.box import Creat_coin

class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y,brick_type,group,color=None,name='brick'):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.brick_type=brick_type
        self.name=name
        self.group = group
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
        print('砖块',self.rect)
        self.gravity=constants.GRAVITY

        self.state = 'rest'
        self.timer = 0
        self.count = 0

    def update(self,level):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(level)

    def handle_states(self,level):
        if self.state == 'rest':
            # print('rest')
            self.rest()
        elif self.state == 'bumped':

            self.bumped(level)
        elif self.state == 'open':
            self.open()

    def rest(self):
       pass

    def go_bumped(self):
        self.y_vel = -7
        self.state = 'bumped'

    def bumped(self,level):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity


        if self.rect.y > self.y + 5:
            self.rect.y = self.y
            self.state = 'rest'

            if self.brick_type==0:
                self.state='rest'
            elif self.brick_type==1:
                self.count+=1
                self.group.add(Creat_coin(self.rect.centerx, self.rect.centery))
                if self.count==8:
                    self.state='open'
                    # self.group.add(Creat_coin(self.rect.centerx, self.rect.centery))
            else:
                # if level.player.big:
                #     self.group.add(create_powerup(self.rect.centerx, self.rect.centery, self.brick_type, 0))
                # else:
                #     self.group.add(create_powerup(self.rect.centerx, self.rect.centery, self.brick_type, 1))
                self.group.add(create_powerup(self.rect.centerx, self.rect.centery, self.brick_type, 3))
                self.state='open'
                #print(self.state)
    def open(self):
        self.frames_index=1
        self.image=self.frames[self.frames_index]
    def smashed(self,group):
        #砖块一分为四，x,y,x_vel,y_vel

        debris=[
            (self.rect.x,self.rect.y,-2,-10),
            (self.rect.x, self.rect.y, 2, -10),
            (self.rect.x, self.rect.y, -2, -5),
            (self.rect.x, self.rect.y, 2, -5),
        ]

        for d in debris:
            group.add(Debris(*d))
        self.kill()

class Debris(pygame.sprite.Sprite):
    def __init__(self,x,y,x_vel,y_vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = tools.get_image(setup.GRAPHICS['tile_set'],68,20,8,8,(0,0,0),constants.BRICK_MULTI)
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.x_vel=x_vel
        self.y_vel=y_vel
        self.gravity=constants.GRAVITY

    def update(self,*args):
        self.rect.x +=self.x_vel
        self.rect.y +=self.y_vel
        self.y_vel +=self.gravity
        if self.rect.y > constants.SCREEN_H:
            self.kill()