#编写者：cwt
#时间：2022/7/4 21:18
#主角
import pygame
import os
import json
from source import setup,tools,constants
from source.components import powerup


class Player(pygame.sprite.Sprite):
    def __init__(self,name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()  #加载角色数据，各种造型帧即其各种状态的速度
        self.setup_states()  #初始化角色各种状态
        self.setup_velocities()
        self.setup_timers()
        self.load_images()
        #print(self.rect)


    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('D:/Users/Administrator/PycharmProjects/superMario/source/data/player/',file_name)  #使用该项目绝对定位
        with open(file_path) as f:
            self.palyer_data=json.load(f)

            #return  self.palyer_data
    def test(self):
        print(self.palyer_data)

    def setup_states(self):  #给主角套buf,套各种状态
        self.state='stand'  #初始状态为站立
        self.face_rigth = True #面朝右
        self.dead = False #没有死亡
        self.big =False #没有变大
        self.fire = False #不能发火球
        self.can_jump=True #目的让其松开跳跃按键，才能再次跳跃
        self.hurt_imune =False #是否为无敌状态
        self.can_shoot =True #可以发射火球
        self.baoqi=False  #是否抱旗子
        self.last_squat = True


    def setup_velocities(self):  #设置速率
        print('111')
        speed=self.palyer_data["speed"]  #加载角色速度
        print(speed)
        self.x_vel = 0 #初始水平方向速度为0
        self.y_vel = 0 #初始垂直方向速度为0

        self.max_walk_vel= speed['max_walk_speed']
        self.max_run_speed =  speed['max_run_speed']
        self.max_y_velocity =  speed['max_y_velocity'] #垂直方向最大速度
        self.walk_accel= speed['walk_accel']
        self.run_accel =  speed['run_accel']
        self.turn_accel = speed['turn_accel'] #转身时的加速度，或者说减速度
        self.jump_velocity = speed['jump_velocity']

        self.gravity=constants.GRAVITY #全局的重力加速度
        self.anti_gravity=constants.ANYI_GRAVITY

        self.max_x_vel=self.max_walk_vel #设置初始最大速度，为最大步行速度
        self.x_accel=self.walk_accel #设置加速度为步行加速度


    def setup_timers(self):  #创建计时器
        self.walking_timer = 0
        self.transtion_timer = 0  ##？？
        self.last_time = 0
        self.death_timer = 0
        self.hurt_imune_timer=0 #记录伤害免疫的时间
        self.last_fireball_timer=0 #控制子弹发射间隔
        self.levies_add_time=0

    def load_images(self):   #载入主角的各种帧造型
        sheet =setup.GRAPHICS['mario_bros']
        frame_rects=self.palyer_data['image_frames']#加载帧

        self.rigth_small_normal_frames = []
        self.rigth_big_normal_frames = []
        self.rigth_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []

        self.small_normal_frames = [self.rigth_small_normal_frames,self.left_small_normal_frames] #小形态各种帧造型
        self.big_normal_frames = [self.rigth_big_normal_frames,self.left_big_normal_frames] #大号正常
        self.big_fire_frames = [self.rigth_big_fire_frames,self.left_big_fire_frames]#大号喷火

        self.all_frames = [
            self.rigth_small_normal_frames,
            self.rigth_big_normal_frames,
            self.rigth_big_fire_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.left_big_fire_frames

        ]

        self.right_frames = self.rigth_small_normal_frames  #刚开始用的是小号帧
        self.left_frames=self.left_small_normal_frames

        # self.right_frames =[]
        # self.left_frames = []
        # self.up_frames = []
        # self.down_frames = []

        # frame_rects = [
        #     (178,32,12,16),
        #     (80,32,15,16),
        #     (96,32,16,16),
        #     (112,32,16,16)
        # ]
        for group,group_frames_rects in frame_rects.items(): #可遍历建值和建值对
            for frame_rect in group_frames_rects:
                right_image = tools.get_image(sheet,frame_rect['x'],frame_rect['y'],frame_rect['width'],frame_rect['height'],(0,0,0),constants.PLAYER_MULTI)
                left_image = pygame.transform.flip(right_image,True,False)  #翻转
                if group == 'right_small_normal':
                    self.rigth_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)

                if group == 'right_big_normal':
                    self.rigth_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)

                if group == 'right_big_fire':
                    self.rigth_big_fire_frames.append(right_image)
                    self.left_big_fire_frames.append(left_image)
                # up_image =pygame.transform.rotate(right_image,90) #逆时针旋转90°
                # down_image = pygame.transform.rotate(right_image,-90)
                # self.right_frames.append(right_image)
                # self.left_frames.append(left_image)
                # self.up_frames.append(up_image)
                # self.down_frames.append(down_image)
        # self.frames=[]
        # self.frames.append(tools.get_image(sheet,178,32,12,16,(0,0,0),constants.BG_MULTI))

        self.frame_index = 0  #取出造型是用到的索引
        self.frames = self.right_frames   #刚开始是脸朝右
        self.image = self.frames[self.frame_index]  #取出第一帧，小号脸朝右
        self.rect = self.image.get_rect() #获取其边框矩形
    def update(self,keys,level):
        self.current_time = pygame.time.get_ticks()  #以毫秒为单位获取时间
        self.handle_states(keys,level) #处理各种状态
        self.is_hurt_immune() #判断是否为无敌模式
       # print(self.rect.x)
        # if keys[pygame.K_RIGHT]:
        #     self.x_vel = 5
        #     self.y_vel = 0
        #     self.frames = self.right_frames
        # if keys[pygame.K_LEFT]:
        #     self.x_vel = -5
        #     self.y_vel = 0
        #     self.frames = self.left_frames
        # if keys[pygame.K_SPACE]:
        #     self.state='jump'
        #     self.y_vel =5

        # if keys[pygame.K_UP]:
        #     self.x_vel = 0
        #     self.y_vel = -5
        #     self.frames = self.up_frames
        # if keys[pygame.K_DOWN]:
        #     self.x_vel = 0
        #     self.y_vel = 5
        #     self.frames = self.down_frames
        # if self.state == 'walk':
        #     if self.current_time -self.walking_timer >100:
        #         self.walking_timer =self.current_time
        #         self.frame_index +=1
        #         self.frame_index %=4
        # if self.state== 'jump':
        #     self.frame_index = 4
        # self.image =self.frames[self.frame_index]


    def handle_states(self,keys,level):
        self.can_jump_or_not(keys) #判断是否可以跳跃
        self.cans_shoot_or_not(keys)  #判断是否可以补充子弹
        if self.state == 'stand':
            self.stand(keys,level)
        elif self.state == 'walk':
            self.walk(keys,level)
            print('lookme')
        elif self.state == 'squat':
            self.squat(keys,level)
        elif self.state == 'jump':
            self.jump(keys,level)
        elif self.state == 'fall':
            self.fall(keys,level)
        elif self.state == 'die':
            self.die(keys)
        elif self.state == 'small2big':
            self.small2big(keys)
        elif self.state == 'big2small':
            self.big2small(keys)
        elif self.state == 'big2fire':
            self.big2fire(keys)
        elif self.state == 'livesAdd1':
            self.livesAdd1(level)



        if self.face_rigth:
            self.image =self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    def can_jump_or_not(self,keys):
        if not keys[pygame.K_a]:
            self.can_jump=True

    def cans_shoot_or_not(self,keys): #补子弹
        if not keys[pygame.K_d]:
            self.can_shoot=True

    def can_squat_or_not(self, keys):
        if not keys[pygame.K_DOWN]:

           self.last_squat=False



    def stand(self,keys,level):
        self.frame_index =0
        self.x_vel=0
        self.y_vel=0
        if keys[pygame.K_RIGHT]:
            self.face_rigth =True
            self.state ='walk'
        elif keys[pygame.K_LEFT]:
            self.face_rigth =False
            self.state = 'walk'
        elif keys[pygame.K_a] and self.can_jump :
            self.state='jump'
            self.y_vel=self.jump_velocity

            setup.SOUND['small_jump'].play()


        elif keys[pygame.K_d] and self.fire  and self.can_shoot:
            self.shot_fireball(level)

        # elif keys[pygame.K_DOWN] and self.big:
        #     if self.last_squat:
        #
        #         self.state='squat'


    # def squat(self,keys,level):
    #     last_frame_bottom = self.rect.bottom
    #     self.frame_index=7
    #     self.rect = self.image.get_rect()
    #     self.rect.bottom=last_frame_bottom
    #     if keys[pygame.K_RIGHT]:
    #         self.face_rigth = True
    #         self.state = 'walk'
    #     elif keys[pygame.K_LEFT]:
    #         self.face_rigth = False
    #         self.state = 'walk'
    #     elif keys[pygame.K_a] and self.can_jump:
    #         self.state = 'jump'
    #         self.y_vel = self.jump_velocity
    #
    #         setup.SOUND['small_jump'].play()
    #
    #
    #     elif keys[pygame.K_d] and self.fire and self.can_shoot:
    #         self.shot_fireball(level)
    #
    #     self.can_squat_or_not(keys)
    def walk(self,keys,level):
        if keys[pygame.K_s]:  #按s超级加速
            self.max_x_vel=self.max_run_speed
            self.x_accel =self.run_accel
            if keys[pygame.K_d] and self.fire and self.can_shoot:
                self.shot_fireball(level)
        else:
            self.max_x_vel =self.max_walk_vel #设置最大速度
            self.x_accel=self.walk_accel #加速度

        if keys[pygame.K_d] and self.fire and self.can_shoot:
            self.shot_fireball(level)
        '''让行走支持跳跃'''
        if keys[pygame.K_a] and self.can_jump:
            self.state='jump'
            self.y_vel=self.jump_velocity #给一个初始的跳跃速度
            setup.SOUND['small_jump'].play()
            if  keys[pygame.K_d] and self.fire and self.can_shoot:
                self.shot_fireball(level)

        shijiancha=self.current_time-self.last_time
        self.last_time=self.current_time
       # print('时间差：',shijiancha)   #一直按着按键的时间差，33-34毫秒
        if self.current_time - self.walking_timer > self.calc_frame_duration():        #当时间差大于100是，切换Mario帧，速度越快摆臂也要越快.calc_frame_duration帧持久
            if self.frame_index < 3:
                self.frame_index+=1
            else:
                self.frame_index = 1
            self.walking_timer =self.current_time
        if keys[pygame.K_RIGHT]:
            self.face_rigth =True
            if self.x_vel <0:
                self.frame_index =5
                self.x_accel =self.turn_accel
            #print(self.x_vel)
            self.x_vel=self.calc_vel(self.x_vel,self.x_accel,self.max_x_vel,True)
           # print(self.x_vel,self.x_accel,self.max_x_vel)
        elif keys[pygame.K_LEFT]:
            self.face_rigth = False
            if self.x_vel > 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        else:
            if self.face_rigth:
                self.x_vel-=self.x_accel
                if self.x_vel<0:
                    self.x_vel=0
                    self.state ='stand'
            else:
                self.x_vel += self.x_accel
                if self.x_vel > 0:
                    self.x_vel = 0
                    self.state = 'stand'

    def jump(self, keys,level):
        self.frame_index =4 #Mario起跳用的是第四帧
       # print(self.y_vel,self.anti_gravity)
        self.y_vel+=self.anti_gravity
        self.can_jump=False

        if self.y_vel>=0:  #往上为负方向，往下为正
            self.state='fall'

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel,self.x_accel,self.max_x_vel,True)
            if keys[pygame.K_d] and self.fire and self.can_shoot:
                self.shot_fireball(level)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
            if keys[pygame.K_d] and self.fire and self.can_shoot:
                self.shot_fireball(level)
        elif keys[pygame.K_d] and self.fire and self.can_shoot:
            self.shot_fireball(level)

        '''实现大小跳，一旦你没有按跳跃键，立刻变为下落状态'''
        if not keys[pygame.K_a]:
            self.state='fall'
    def fall(self,keys,level):
        self.y_vel=self.calc_vel(self.y_vel,self.gravity,self.max_y_velocity)
        #临时代码，便于记忆
        # TODO workaround , will move to level.py for collision detection
        # if self.rect.bottom>constants.GROUND_HEIGHT:
        #     self.rect.bottom = constants.GROUND_HEIGHT
        #     self.y_vel=0
        #     self.state='walk'
        if self.baoqi:
            self.frame_index=10

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        elif keys[pygame.K_d] and self.fire and self.can_shoot:
            self.shot_fireball(level)

    def play_basketball(self, keys):
        pass

    def die(self,keys):
        self.rect.y +=self.y_vel
        self.y_vel+=self.anti_gravity  #为了避免死亡状态下可能触发的碰撞检测

    def go_die(self):
        self.dead= True
        self.y_vel = self.jump_velocity
        self.frame_index = 6
        self.state = 'die'
        self.death_timer = self.current_time

    def small2big(self,keys):
        frame_dur=65
        sizes = [1,0,1,0,1,2,0,1,2,0,2] #0 small 1 medium 2 big
        frames_and_idx=[(self.small_normal_frames,0),(self.small_normal_frames,7),(self.big_normal_frames,0)]
        if self.transtion_timer ==0:
            self.big=True
            self.transtion_timer=self.current_time
            self.changing_index=0
        elif self.current_time -self.transtion_timer > frame_dur:
            self.transtion_timer = self.current_time
            frames,index = frames_and_idx[sizes[self.changing_index]]
            self.change_player_image(frames,index)
            self.changing_index+=1
            if self.changing_index == len(sizes):
                self.transtion_timer = 0
                self.state = 'walk'
                self.right_frames = self.rigth_big_normal_frames
                self.left_frames = self.left_big_normal_frames

    def big2small(self,keys):
        frame_dur=65
        sizes = [2,1,0,1,0,1,0,1,0,1,0] #0 small 1 medium 2 big
        frames_and_idx=[(self.small_normal_frames,8),(self.big_normal_frames,8),(self.big_normal_frames,4)]#帧库及其对应帧索引
        if self.transtion_timer ==0:
            self.big=False
            self.fire=False
            self.transtion_timer=self.current_time
            self.changing_index=0
        elif self.current_time -self.transtion_timer > frame_dur:
            self.transtion_timer = self.current_time
            frames,index = frames_and_idx[sizes[self.changing_index]]
            self.change_player_image(frames,index)
            self.changing_index+=1
            if self.changing_index == len(sizes):
                self.transtion_timer = 0
                self.state = 'walk'
                self.right_frames = self.rigth_small_normal_frames
                self.left_frames = self.left_small_normal_frames

    def big2fire(self,keys):

        frame_dur = 65
        sizes = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 0 small 1 medium 2 big
        frames_and_idx = [(self.big_fire_frames, 3), (self.big_normal_frames, 3)]  # 帧库及其对应帧索引
        if self.transtion_timer == 0:
            self.fire = True
            self.transtion_timer = self.current_time
            self.changing_index = 0
        elif self.current_time - self.transtion_timer > frame_dur:
            self.transtion_timer = self.current_time
            frames, index = frames_and_idx[sizes[self.changing_index]]
            self.change_player_image(frames, index)
            self.changing_index += 1
            if self.changing_index == len(sizes):
                self.transtion_timer = 0
                self.state = 'walk'
                self.right_frames = self.rigth_big_fire_frames
                self.left_frames = self.left_big_fire_frames

    def livesAdd1(self,level):
        if self.levies_add_time==0:
            print('我来了1')
            self.levies_add_time=self.current_time
        elif self.current_time-self.levies_add_time >100:
            self.levies_add_time = self.current_time
            level.info.lives_labels.clear()
            self.state='walk'
            print('我来了2')
            #xiaobug 第二次进来不。。。
        else:
            y=self.rect.top-50
            level.info.lives_labels.append((level.info.create_lable('lives + 1'),(252,y)))
            print('我来了3')



    def change_player_image(self,frames,index):
        self.frame_index=index
        if self.face_rigth:
            self.right_frames =frames[0]  #获取self.rigth_small_normal_frames,rigth_big_normal_frames
            self.image=self.right_frames[self.frame_index] #按照传入的参数取出小mario，中Mario，大mario
        else:
            self.left_frames=frames[1]
            self.image =self.left_frames[self.frame_index]
        last_frame_bottom = self.rect.bottom
        last_frame_centerx=self.rect.centerx
        self.rect=self.image.get_rect()
        self.rect.bottom =last_frame_bottom
        self.rect.centerx =last_frame_centerx
        #print(self.rect)
        #print(self.rect.bottom)


    def calc_vel(self,vel,accle,max_vel,is_positive=True):#计算速度
        if is_positive:
            return min(vel +accle,max_vel)
        else:
            return max(vel-accle,-max_vel)
    def calc_frame_duration(self):
        duration=-60/self.max_run_speed+abs(self.x_vel)+80 # abs() 函数返回数字的绝对值
        return duration

    def is_hurt_immune(self):#判断是否为无敌模式
        if self.hurt_imune:
            if self.hurt_imune_timer == 0:
                self.hurt_imune_timer =self.current_time

                '''无敌时间内添加特效,创建空白帧，在每100毫秒的前50毫秒显示，后50毫秒显示实体'''
                self.blank_image =pygame.Surface((1,1)) ##??
            elif self.current_time -self.hurt_imune_timer <2000:
                if (self.current_time- self.hurt_imune_timer)%100 <50:
                    self.image=self.blank_image
            else:
                self.hurt_imune=False
                self.hurt_imune_timer=0

    def shot_fireball(self,level):
        setup.SOUND['fireball'].play()
        if self.current_time-self.last_fireball_timer>300:
            self.frame_index =6
            fireball=powerup.Fireball(self.rect.centerx,self.rect.centery,self.face_rigth,level.game_info)
            level.powerup_group.add(fireball) #加入精灵组，在level里直接调用update和draw即可显示
            self.can_shoot=False
            self.last_fireball_timer=self.current_time

if __name__ == '__main__':
    play=Player('mario')
    play.load_data()
    print(play.load_data(),type(play.load_data()),'\n',play.load_data()['speed'])
    play.test()