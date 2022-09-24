#编写者：cwt
#时间：2022/7/4 21:17
#敌人

import pygame
from source import setup,tools,constants
from source.components import box

'''myself'''
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self,x,y,direction,type,color=None):
#         pygame.sprite.Sprite.__init__(self)
#         self.x=x
#         self.y=y
#         self.direction=direction
#         self.type=type
#         self.frame_index=0 #帧图片索引，用来切换帧
#         self.frames=[] #存储将要切换的帧图片
#         frame_rects={
#             (0,16,16,16),
#             (16,16,16,16)
#         }  #循环使用两帧实现相互切换
#         #self.image=tools.get_image(setup.GRAPHICS['enemies'],0,16,16,16,(0,0,0),2.5)
#         self.load_frames(frame_rects)
#
#         self.image=self.frames[self.frame_index]
#
#         self.rect=self.image.get_rect()
#         self.rect.x=self.x
#         self.rect.bottom=self.y
#         self.timer = 0  # 计时器
#
#
#     def load_frames(self, frame_rects):
#         sheet = setup.GRAPHICS['enemies']
#         for frame_rect in frame_rects:
#             self.frames.append(
#                 tools.get_image(sheet, *frame_rect, (0, 0, 0), 2.5))  # *frame_rect解包，把该元组放入时分解成四个变量
#         print(self.frames)
#     def update(self):
#         self.current_time = pygame.time.get_ticks()  # 获取当前时间
#         frame_durations = [125, 125]  # 停留时间
#
#         if self.timer == 0:
#             self.timer = self.current_time
#         elif self.current_time - self.timer > frame_durations[self.frame_index]:
#             self.frame_index += 1
#             self.frame_index %= 2
#             self.timer = self.current_time
#
#         self.image = self.frames[self.frame_index]

def create_enemy(enemy_data):

    enemy_type=enemy_data['type']
    x,y,direction,color = enemy_data['x'],enemy_data['y'],enemy_data['direction'],enemy_data['color']
    #print('11')
    if enemy_type ==0: #Goomba 蘑菇怪
        enemy=Goomba(x,y,direction,"gooba",color)
        #print(enemy)
    elif enemy_type ==1: #Koopa 乌龟
        #print('99')
        enemy=Koopa(x,y,direction,"koopa",color)
    else:
        # print('99')
        enemy = Koopa(x, y, direction, "koopa", color)

    return enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,bottom_y,direction,name,frame_rects):
        pygame.sprite.Sprite.__init__(self)
        #print('33')

        self.direction=direction
        self.name=name
        self.frame_index = 0
        self.left_frames=[]
        self.right_frames=[]
        self.load_frames(frame_rects)
        self.frames=self.left_frames if self.direction ==0 else self.right_frames
       # print(self.frames)
        self.image=self.frames[self.frame_index]
        #print(self.image)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.bottom=bottom_y
        
        self.timer = 0  # 计时器
        self.x_vel = -1 *constants.ENEMY_SPEED if self.direction == 0 else constants.ENEMY_SPEED  #如果野怪面朝左，就让它有一个向左的速度，否则反之
        self.y_vel = 0
        self.gravity = constants.GRAVITY
        self.state = 'walk'

    def load_frames(self,frame_rects):
        for frame_rect in frame_rects:
            left_frame=tools.get_image(setup.GRAPHICS['enemies'],*frame_rect,(0,0,0),constants.ENEMY_MULTI)
            right_frame=pygame.transform.flip(left_frame,True,False) #第一个参数图像，第二个是否水平翻转，第三个是否垂直翻转
            self.left_frames.append(left_frame)
            self.right_frames.append(right_frame)

    def update(self,level):
        '''适用于间隔时间不同'''
        # self.current_time = pygame.time.get_ticks()  # 获取当前时间
        # frame_durations = [125, 125]  # 停留时间
        #
        # if self.timer == 0:
        #     self.timer = self.current_time
        # elif self.current_time - self.timer > frame_durations[self.frame_index]:
        #     self.frame_index += 1
        #     self.frame_index %= 2
        #     self.timer = self.current_time
        #
        # self.image = self.frames[self.frame_index]
        self.current_time=pygame.time.get_ticks()
        self.handle_states(level)
        self.update_position(level) #位置更新


    def handle_states(self,level):   #使用状态机处理野怪状态

        if self.state == 'walk':
            self.walk()
        elif self.state == 'fall':
            self.fall()
        elif self.state == 'die':
            self.die()
        elif self.state == 'trampled': #踩踏
            self.trampled(level)
        elif self.state == 'slide':  # 滑行
            self.slide()
        if self.direction:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    def walk(self):
        if self.current_time - self.timer >125:
            self.frame_index=(self.frame_index+1)%2
            self.image=self.frames[self.frame_index]
            self.timer=self.current_time
    def fall(self):
        # if self.y_vel <10:
            self.y_vel += self.gravity
    def die(self):

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.y_vel += self.gravity
        if self.rect.y > constants.SCREEN_H:
            self.kill()
    def trampled(self,level):
        pass
    def slide(self):
        pass

    def update_position(self,level):
        self.rect.x += self.x_vel
        self.check_x_collisions(level) #x方向碰撞检测
        self.rect.y += self.y_vel
        if self.state != 'die':
            self.check_y_collisions(level)#y方向碰撞检测
    def check_x_collisions(self,level):
        sprite = pygame.sprite.spritecollideany(self,level.ground_items_group)
        if sprite:
            #self.direction =1 if self.direction == 0 else 0
            if self.direction: #向右
                self.direction =0
                self.rect.right = sprite.rect.left
            else:
                self.direction = 1
                self.rect.left = sprite.rect.right
            self.x_vel *=-1

        if self.state =='slide':
            enemy =pygame.sprite.spritecollideany(self,level.enemy_group)
            if enemy:
                enemy.go_die(how='slided',direction=self.direction)
                level.enemy_group.remove(enemy)
                level.dying_group.add(enemy)


    def check_y_collisions(self,level):
        #print('yyys')
        check_group= pygame.sprite.Group(level.ground_items_group,level.brick_group,level.box_group)
        sprite = pygame.sprite.spritecollideany(self,check_group)
        if sprite:
            #print('野怪头部{0}，野怪脚底{2},碰撞物体头部{3}',self.rect.top,self.rect.bottom,sprite.rect.top)
            if self.rect.top < sprite.rect.top: # ??从上往下掉落  已解决：坐标轴原因
                self.rect.bottom =sprite.rect.top
                self.y_vel = 0
                self.state='walk'
        level.check_will_fail(self)

    def go_die(self,how,direction=1):
        #self.kill()
        self.death_time = self.current_time
        if how in ['bumped','slided']: #各种死因
            self.x_vel =constants.ENEMY_SPEED * direction
            self.y_vel=-8
            self.gravity=0.5
            self.state='die'
            self.frame_index=2
        elif how=='trampled':
            self.state='trampled'







class Goomba(Enemy):
    def __init__(self,x,y,direction,name,color):
        #print('22')

        bright_rect_frames = [(0, 16, 16, 16), (16, 16, 16, 16),(32,16,16,16)]
        daek_rect_frames = [(0, 48, 16, 16), (16, 48, 16, 16),(32,48,16,16)]

        if not color:
            frame_rects = bright_rect_frames
        else:
            frame_rects = daek_rect_frames
        Enemy.__init__(self,x,y,direction,name,frame_rects)

    def trampled(self,level):
        self.x_vel = 0
        self.frame_index = 2
        if self.death_time == 0 :
            self.death_time == self.current_time
        if self.current_time - self.death_time >500: #野怪死亡500毫秒
            self.kill()


class Koopa(Enemy):
    def __init__(self, x, y, direction, name, color):
        #print('44')

        bright_rect_frames = [(96, 9, 16, 22), (112, 9, 16, 22), (160, 9, 16, 22)]
        daek_rect_frames = [(96, 9, 16, 22), (112, 9, 16, 22), (160, 9, 16, 22)]

        if not color:
            frame_rects = bright_rect_frames
        else:
            frame_rects = daek_rect_frames
        Enemy.__init__(self,x, y, direction, name, frame_rects)

        '''龟壳长时间不去撞击，乌龟会重新钻出来'''
        self.shell_timer = 0


    def trampled(self,level):
        self.x_vel = 0
        self.frame_index = 2
        # if self.death_time == 0 :
        #     self.death_time == self.current_time
        # if self.current_time - self.death_time >500: #野怪死亡500毫秒
        #     self.kill()

        if self.shell_timer ==0:
            self.shell_timer =self.current_time
        if self.current_time -self.shell_timer >5000:
            self.state='walk'
            self.x_vel = -constants.ENEMY_SPEED if self.direction ==0 else constants.ENEMY_SPEED
            level.enemy_group.add(self) #加入乌龟组
            level.shell_group.remove(self)
            self.shell_timer =0
    def slide(self):
        pass

