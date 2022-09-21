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


    def update(self,level):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(level)

    def handle_states(self,level):
        if self.state =='rest':
           # print('rest')
            self.rest()
        elif self.state == 'bumped':
            self.bumped(level)
        elif self.state =='open':
            self.open()

    def rest(self): #好好呆着状态，实现金币闪烁
        if self.box_type == 5:
            self.image=pygame.Surface((1,1))

        else:
            frame_durtions =[400,100,100,50]
            if self.current_time - self.timer > frame_durtions[self.frames_index]:
                self.frames_index=(self.frames_index+1)%4

                self.timer = self.current_time
            self.image =self.frames[self.frames_index]

        #print('look here')
    def go_bumped(self):
        self.y_vel=-7
        self.state='bumped'
    def bumped(self,level):
        self.rect.y +=self.y_vel
        self.y_vel +=self.gravity
        self.frames_index=1
        self.image=self.frames[self.frames_index]

        if self.rect.y >self.y+5:
            self.rect.y=self.y
            self.state='open'

            #box_type 0,1,2,3对应 空，金币，星星，蘑菇
            if self.box_type == 1:
                self.group.add(Creat_coin(self.rect.centerx,self.rect.centery))
                self.group.add(Text_info(self.rect.centerx,self.rect.centery,'+ 200'))
            elif self.box_type==3:
                if level.player.big:
                    self.group.add(create_powerup(self.rect.centerx,self.rect.centery,self.box_type,1))
                else:
                    self.group.add(create_powerup(self.rect.centerx,self.rect.centery,self.box_type,0))
                print(self.group)
            elif self.box_type==4:
                self.group.add(create_powerup(self.rect.centerx, self.rect.centery, self.box_type, 3))
            elif self.box_type==5:
                self.group.add(create_powerup(self.rect.centerx, self.rect.centery, self.box_type, 2))


    def open(self):
        pass

class Creat_coin(pygame.sprite.Sprite):
    def __init__(self,centerx,centery):
        pygame.sprite.Sprite.__init__(self)
        self.name='coin'
        frame_rects=[(0, 112, 16, 16),(16,112,16,16),(32,112,16,16),(48,112,16,16)]
        self.frames=[]
        self.frame_index=0
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(setup.GRAPHICS['item_objects'], *frame_rect, (0, 0, 0), 2.5))
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_rect()
        self.rect.centerx=centerx
        self.rect.centery=centery
        self.origin_y = centery - self.rect.height / 2
        self.x_vel = 0
        self.y_vel = -10
        self.gravity = 1
        self.max_y_vel = 8
        self.state = 'grow'

        self.timer = 0  # 计时器



    def check_y_collisions(self, level):


        level.check_will_fail(self)

    def update(self,level):
        self.current_time = pygame.time.get_ticks()  # 获取当前时间
        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > 100:
            self.frame_index += 1
            self.frame_index %= 4
            self.timer = self.current_time
        self.image = self.frames[self.frame_index]


        if self.state == 'grow':
            self.rect.y += self.y_vel
            if self.rect.bottom < self.origin_y-200:
                self.state = 'fall'  # 傻了傻了。。用俩等报bug了


        elif self.state == 'fall':
            if self.y_vel < self.max_y_vel:
                self.y_vel += self.gravity

        self.rect.y += self.y_vel
        self.check_y_collisions(level)  # y方向碰撞检测
        print( self.rect.y,self.rect.bottom)
        if self.rect.y > self.origin_y:

            self.kill()

       # self.update_position(self,level)


class Text_info(pygame.sprite.Sprite):
    def __init__(self, centerx, centery,text):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'text_info'
        font = pygame.font.SysFont(constants.FONT, 40)  # 调用系统字体
        label_image = font.render(text, 1, (255, 255, 255))  # 把文字渲染成图片
        self.image = label_image
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx+50
        self.rect.centery = centery
        self.origin_y = centery - self.rect.height / 2
        self.x_vel = 0
        self.y_vel = -5
        self.gravity = 1
        self.max_y_vel = 8
        self.state = 'grow'

    def update_position(self, level):

        self.rect.y += self.y_vel
        self.check_y_collisions(level)  # y方向碰撞检测
        if self.rect.y > self.rect.bottom:
            self.kill()

    def check_y_collisions(self, level):

        level.check_will_fail(self)

    def update(self, level):


        if self.state == 'grow':
            self.rect.y += self.y_vel
            if self.rect.bottom < self.origin_y - 200:
                self.state = 'fall'  # 傻了傻了。。用俩等报bug了


        elif self.state == 'fall':
            if self.y_vel < self.max_y_vel:
                self.y_vel += self.gravity

        self.rect.y += self.y_vel
        self.check_y_collisions(level)  # y方向碰撞检测
        print(self.rect.y, self.rect.bottom)
        if self.rect.y > self.origin_y:
            self.kill()

    # self.update_position(self,level)
