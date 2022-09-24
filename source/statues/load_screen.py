#编写者：cwt
#时间：2022/7/4 21:22
#载入页面
from source.components import info
import pygame

class LoadScreen():

    def start(self,game_info,current_time):

        self.game_info=game_info
        self.game_info['statue']='load_screen'
        self.finished= False
        self.next = 'level'
        self.duration=2000 #持续时间
        self.timer = 0
        self.info = info.Info('load_screen',self.game_info)

    def update(self,surface,keys,current_time):
        self.draw(surface)
        if self.timer==0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished =True
            self.timer =0

    def draw(self,surface):
        surface.fill((0,0,0))
        self.info.update(self.game_info)  # 调用信息更新方法，调用金币类更新类更新方法,实现金币闪烁
        self.info.draw(surface)

class GameDver(LoadScreen):
    def start(self,game_info,current_time):
        game_info['lives']=3
        game_info['score']=000000
        game_info['coin']=0
        self.game_info= game_info
        self.game_info['statue'] = 'GameDver'
        self.finished = False
        self.next='main_menu'
        self.duration =4000
        self.timer = 0
        self.info =info.Info('game_over',self.game_info)

class Load_level2(LoadScreen):
    def start(self,game_info,current_time):
        game_info['lives']=3
        self.game_info= game_info
        self.finished = False
        self.next='level2'
        self.duration =4000
        self.timer = 0
        self.info =info.Info('load_screen',self.game_info)

class Load_level3(LoadScreen):
    def start(self,game_info,current_time):
        game_info['lives']=3
        self.game_info= game_info
        self.finished = False
        self.next='level3'
        self.duration =4000
        self.timer = 0
        self.info =info.Info('load_screen',self.game_info)

class Load_level4(LoadScreen):
    def start(self,game_info,current_time):
        game_info['lives']=3
        self.game_info= game_info
        self.finished = False
        self.next='level4'
        self.duration =4000
        self.timer = 0
        self.info =info.Info('load_screen',self.game_info)
