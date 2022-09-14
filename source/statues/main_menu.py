#编写者：cwt
#时间：2022/7/4 21:21
#第一次加载页面

import pygame
from source import setup
from source import tools
from source import constants
from source.components import info
import source.tools


class MainMenu():
    def __init__(self):
        game_info={
            'statue':'main_menu',
            'score':0,
            'top_score':0,
            'coin':0,
            'current_time':0,
            'lives':1,
            'player_state':'small',
            'time':300
        }
        self.start(game_info,0.0)

    def start(self,game_info,current_time):
        self.current_time=current_time
        self.game_info=game_info
        self.setup_background()   #设置背景底图
        self.setup_cursor()       #设置光标
        self.setup_palyer()        #设置游戏角色
        self.info=info.Info('main_menu',self.game_info)   #初始化该类，设置文字信息
        self.finished=False     #主页面是否结束（状态机）
        self.next = 'load_screen'

    def setup_background(self): #设置背景底图
        self.background=setup.GRAPHICS['level_1'] #取出该图片
        self.background_rect=self.background.get_rect() #获取整个图片的矩形
        self.background=pygame.transform.scale(self.background,(int(self.background_rect.width*constants.BG_MULTI),
                                                                int(self.background_rect.height*constants.BG_MULTI))) #对图片进行缩放
        self.viewport=setup.SCREEN.get_rect()  #滑动窗口设置成屏幕大小

        self.title=setup.GRAPHICS['title_screen']   #背景上的标题
        self.title_image=tools.get_image(self.title,1,60,176,88,(255,0,220),constants.BG_MULTI)
    def setup_palyer(self):
        self.play=setup.GRAPHICS['mario_bros'] #取出Mario大图
        self.play_image=tools.get_image(self.play,178,32,12,16,(0,0,0),constants.BG_MULTI) #扣除Mario
    def setup_cursor(self):  #设置光标
        self.cursor=pygame.sprite.Sprite()  #创建一个精灵
        self.cursor.image = tools.get_image(setup.GRAPHICS['item_objects'], 24, 160, 8, 8, (0, 0, 0), constants.BG_MULTI) #加载光标图片，并扣出
        rect=self.cursor.image.get_rect()  #得到光标一般的矩形大小
        rect.x,rect.y=(220,360)  #设置矩形坐标
        self.cursor.rect=rect #把矩形的配置给光标
        self.cursor.state='1P' #状态机
    def update_cursor(self,keys):
        if keys[pygame.K_UP]: #按下PgUp按钮
            self.cursor.state='1P'
            self.cursor.rect.y=360
        elif keys[pygame.K_DOWN]: #按下PgDn按钮
            self.cursor.state='2P'
            self.cursor.rect.y=405
        elif keys[pygame.K_RETURN]: #按下回车建
            if self.cursor.state=='1P':
                #setup.SOUND['one_up'].play()
                self.finished = True
            elif self.cursor.state=='2P':
                #setup.SOUND['one_up'].play()
                self.finished = True

    def update(self,surface,keys,current_time):
        import random
        # surface.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        self.current_time =current_time
        self.game_info['current_time'] =self.current_time

        self.update_cursor(keys)  #调用更新光标方法

        surface.blit(self.background, self.viewport)  #在可见屏幕上画出背景
        surface.blit(self.title_image,(170,100))  #画上标题
        surface.blit(self.play_image,(110,490))    #画上角色
        surface.blit(self.cursor.image,self.cursor.rect)    #画上光标

        self.info.update(self.game_info)    #调用信息更新方法，调用金币类更新类更新方法,实现金币闪烁
        self.info.draw(surface) ##画出文字信息，金币。当state='load_screen',画出马里奥



if __name__ == '__main__':
    menu=MainMenu()
    pygame.init()
    pygame.display.set_mode((800,600))
    surface=pygame.display.get_surface()


    image=pygame.image.load('D:/Users/Administrator/PycharmProjects/superMario/resources/graphics/mario_bros.png')
    box1 = pygame.Surface((16, 16))
    box1.blit(image,(0,0),(145,32,16,16))
    while True:
        menu.update(surface)

        surface.blit(box1, (300, 500))
        pygame.display.update()