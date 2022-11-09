#编写者：cwt
#时间：2022/7/4 21:20
#游戏信息
import pygame
from source import constants
from source.components import coin
from source import setup,tools
pygame.font.init()

class Info():
    def __init__(self,state,game_info):
        self.state = state
        self.game_info=game_info
        self.coin_total = game_info['coin']
        self.time = 402 #倒计时401
        self.timer =0 #计时器
        self.current_time =0
        self.special_state = None
        self.lives =game_info['lives']
        self.score=game_info['score']
        self.coin=game_info['coin']
        self.top_score =game_info['top_score']
        self.create_state_lable()  #创某阶段特有的文字
        self.create_info_labels()    #创建各阶段通用性息
        self.create_update_labels()   #创建要更新的内容
        self.create_score_group(self.score)
        self.draw_lives_add()
        self.time_labels=[]
        self.create_countdown_clock()

        self.coin_labels = []
        self.create_coin_counter(self.coin)
        self.flash_coin = coin.FlashingCoin() #初始化金币类



    def create_coin_counter(self,coin):
        """Creates the info that tracks the number of coins Mario collects"""
        if coin == 0:
            self.coin_labels.append((self.create_lable('X00'), (300, 55)))
        elif coin<10 :
            self.coin_labels.clear()
            self.coin_labels.append((self.create_lable('X0{0}'.format(coin)), (300, 55)))
        else :
            self.coin_labels.clear()
            self.coin_labels.append((self.create_lable('X{0}'.format(coin)), (300, 55)))
    def create_countdown_clock(self):
        if self.time == 402:
            self.time_labels.append((self.create_lable('401'), (635, 55)))
        if self.game_info['statue']=='level':
            """Creates the count down clock for the level"""
            self.current_time = pygame.time.get_ticks()  # 获取当前时间
            #print(self.current_time)
            if self.time==402:
                self.time-=1
                self.timer=self.current_time
            elif self.current_time -self.timer >1000:
                self.timer = self.current_time
                print(self.time_labels)
                self.time_labels.clear()
                print(self.time_labels)
                self.time_labels.append((self.create_lable('{0}'.format(self.time)), (635, 55)))
                self.time -= 1


    def create_score_group(self,score):
        """Creates the initial empty score (000000)"""
        if score ==0:
            self.update_labels.append((self.create_lable('000000'), (75, 55)))
        elif score<1000:
            self.update_labels.clear()
            self.update_labels.append((self.create_lable('000{0}'.format(score)), (75, 55)))
        elif score < 10000:
            self.update_labels.clear()
            self.update_labels.append((self.create_lable('00{0}'.format(score)), (75, 55)))
        elif score < 100000:
            self.update_labels.clear()
            self.update_labels.append((self.create_lable('0{0}'.format(score)), (75, 55)))
        else:
            self.update_labels.clear()
            self.update_labels.append((self.create_lable('{0}'.format(score)), (75, 55)))
    def create_state_lable(self):  #创造某阶段特有的文字
        self.state_labels=[]
        if self.state=='main_menu':
            self.state_labels.append((self.create_lable('1 PLAYER GAME'),(272,360)))
            self.state_labels.append((self.create_lable('2 PLAYER GAME'), (272, 405)))
            self.state_labels.append((self.create_lable('TOP   -'), (290, 465)))
            self.state_labels.append((self.create_lable('000000'), (400, 465)))
        elif self.state == 'load_screen':
            self.state_labels.append((self.create_lable('WORLD'), (280, 200)))
            self.state_labels.append((self.create_lable('1 - 1'), (430, 200)))
            self.state_labels.append((self.create_lable('X   {0}'.format(self.game_info['lives'])), (380, 280)))
            self.play_image = tools.get_image(setup.GRAPHICS['mario_bros'],178,32,12,16,(0,0,0),constants.BG_MULTI)
        elif self.state == 'game_over':
            self.state_labels.append((self.create_lable('GAME OVER'), (280, 300)))
        # elif self.state == 'time_out':
        #     self.state_labels.append((self.create_lable('TIME OUT'), (290, 310)))
        elif self.state == 'load_level2':
            self.state_labels.append((self.create_lable('WORLD'), (280, 200)))
            self.state_labels.append((self.create_lable('1 - 1'), (430, 200)))
            self.state_labels.append((self.create_lable('X   {0}'.format(self.game_info['lives'])), (380, 280)))
            self.play_image = tools.get_image(setup.GRAPHICS['mario_bros'], 178, 32, 12, 16, (0, 0, 0),
                                              constants.BG_MULTI)

    def create_info_labels(self):  #创建各阶段通用性息
        self.info_labels = []
        self.info_labels.append((self.create_lable('MARIO'), (75, 30)))
        self.info_labels.append((self.create_lable('WORLD'), (450, 30)))
        self.info_labels.append((self.create_lable('TIME'), (625, 30)))


        self.info_labels.append((self.create_lable('1 - 1'), (480, 55)))

    def create_update_labels(self):
        self.update_labels=[]


    def create_lable(self,label,size=40,width_scale=1.25,height_csale=1): #文字生成图片
        font = pygame.font.SysFont(constants.FONT,size) #调用系统字体
        label_image=font.render(label,1,(255,255,255))   #把文字渲染成图片
        # rect=label_image.get_rect()
        # label_image=pygame.transform.scale(label_image,(int(rect.width * width_scale),
        #                                                (int(rect.width * height_csale))))
        # print(label_image, type(label_image))
        return label_image
    def update(self,level_info):  #调用金币类更新类更新方法,实现金币闪烁
        self.create_countdown_clock()
        self.flash_coin.update()
        self.handle_level_state(level_info)
    def handle_level_state(self, level_info):
        self.create_score_group(level_info['score'])
        self.create_coin_counter(level_info['coin'])
        """Updates info based on what state the game is in"""
    def draw_lives_add(self,):
        self.lives_labels=[]
        #self.lives_labels.append((self.create_lable('lives + 1'), (272, 360)))

    def draw(self,surface):
        # surface.blit(self.create_lable('GIVE ME A LITTLE HEATRT~',size=60),(100,400))
        for label in self.state_labels: #画出该状态特有信息
            surface.blit(label[0],label[1])
        for label in self.info_labels:  #画出通用信息
            surface.blit(label[0],label[1])
        for label in self.update_labels:  #画出更新后分数的信息
            surface.blit(label[0],label[1])
        for label in self.coin_labels:    #画出更新后的金币信息
            surface.blit(label[0], label[1])
        for label in self.time_labels:  # 画出更新后的金币信息
            surface.blit(label[0], label[1])
        if self.lives_labels:
            for label in self.lives_labels:
                surface.blit(label[0], label[1])
            self.lives_labels.clear()
        surface.blit(self.flash_coin.image,self.flash_coin.rect)    #画出金币

        if self.state == 'load_screen':
            surface.blit(self.play_image,(300,270))



