#编写者：cwt
#时间：2022/7/4 21:16
#砖块
import pygame
from source import setup,tools,constants
from source.components.powerup import create_powerup

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
        self.gravity=constants.GRAVITY

        self.state = 'rest'
        self.timer = 0

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_states()

    def handle_states(self):
        if self.state == 'rest':
            # print('rest')
            self.rest()
        elif self.state == 'bumped':
            self.bumped()
        elif self.state == 'open':
            self.open()

    def rest(self):
       pass

    def go_bumped(self):
        self.y_vel = -7
        self.state = 'bumped'

    def bumped(self):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity


        if self.rect.y > self.y + 5:
            self.rect.y = self.y
            self.state = 'rest'

            if self.brick_type==0:
                self.state='rest'
            elif self.brick_type==1:
                self.state='open'
            else:
                self.group.add(create_powerup(self.rect.centerx,self.rect.centery,self.brick_type))
    def open(self):
        self.frames_index=1
        self.image=self.frames[self.frames_index]