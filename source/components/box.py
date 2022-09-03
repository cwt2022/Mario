#编写者：cwt
#时间：2022/7/4 21:16
#盒子
import pygame
from source import setup,tools,constants
from source.components.powerup import create_powerup

class Box(pygame.sprite.Sprite):
    def __init__(self,x,y,box_type,group,name='box',color=None):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.box_type=box_type
        self.name=name
        self.group=group  #相当于一个篮子
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
        self.gravity=constants.GRAVITY

        self.state = 'rest'
        self.timer = 0


    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_states()

    def handle_states(self):
        if self.state =='rest':
           # print('rest')
            self.rest()
        elif self.state == 'bumped':
            self.bumped()
        elif self.state =='open':
            self.open()

    def rest(self): #好好呆着状态，实现金币闪烁
        frame_durtions =[400,100,100,50]
        if self.current_time - self.timer > frame_durtions[self.frames_index]:
            self.frames_index=(self.frames_index+1)%4

            self.timer = self.current_time
        self.image =self.frames[self.frames_index]

        #print('look here')
    def go_bumped(self):
        self.y_vel=-7
        self.state='bumped'
    def bumped(self):
        self.rect.y +=self.y_vel
        self.y_vel +=self.gravity
        self.frames_index=1
        self.image=self.frames[self.frames_index]

        if self.rect.y >self.y+5:
            self.rect.y=self.y
            self.state='open'

            #box_type 0,1,2,3对应 空，金币，星星，蘑菇
            if self.box_type == 1:
                pass
            else:
                self.group.add(create_powerup(self.rect.centerx,self.rect.centery,self.box_type))
                print(self.group)

    def open(self):
        pass