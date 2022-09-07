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
        self.create_state_lable()  #创某阶段特有的文字
        self.create_info_labels()    #创建各阶段通用性息
        self.flash_coin = coin.FlashingCoin() #初始化金币类
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
        elif self.state =='level2':
            self.state_labels.append((self.create_lable('WELCOME TO LEVEL 2'), (200, 300)))

    def create_info_labels(self):  #创建各阶段通用性息
        self.info_labels = []
        self.info_labels.append((self.create_lable('MARIO'), (75, 30)))
        self.info_labels.append((self.create_lable('WORLD'), (450, 30)))
        self.info_labels.append((self.create_lable('TIME'), (625, 30)))
        self.info_labels.append((self.create_lable('000000'), (75, 55)))
        self.info_labels.append((self.create_lable('X00'), (300, 55)))
        self.info_labels.append((self.create_lable('1 - 1'), (480, 55)))
        self.info_labels.append((self.create_lable('{0}'.format(self.game_info['time'])), (635, 55)))

    def create_lable(self,label,size=40,width_scale=1.25,height_csale=1): #文字生成图片
        font = pygame.font.SysFont(constants.FONT,size) #调用系统字体
        label_image=font.render(label,1,(255,255,255))   #把文字渲染成图片
        # rect=label_image.get_rect()
        # label_image=pygame.transform.scale(label_image,(int(rect.width * width_scale),
        #                                                (int(rect.width * height_csale))))
        # print(label_image, type(label_image))
        return label_image
    def update(self):  #调用金币类更新类更新方法,实现金币闪烁
        self.flash_coin.update()

    def draw(self,surface):
        # surface.blit(self.create_lable('GIVE ME A LITTLE HEATRT~',size=60),(100,400))
        for label in self.state_labels: #画出该状态特有信息
            surface.blit(label[0],label[1])
        for label in self.info_labels:  #画出通用信息
            surface.blit(label[0],label[1])
        surface.blit(self.flash_coin.image,self.flash_coin.rect)    #画出金币

        if self.state == 'load_screen':
            surface.blit(self.play_image,(300,270))



