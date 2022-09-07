#编写者：cwt
#时间：2022/9/7 10:00
#关卡 2
import json
import os
import random

from source.components import info,player,stuff,brick,box,enemy,plagpole
from source import tools,setup,constants,sound
import pygame

class Level2:
    def start(self,game_info):


        self.game_info=game_info
        self.finished= False
        self.next = 'game_over'
        self.info=info.Info('level2',self.game_info)







    def update(self,surface,keys):
        self.current_time = pygame.time.get_ticks()

        #setup.MUSIC['main_theme'].play()
        self.draw(surface)


    def draw(self,surface):
        surface.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        self.info.update()  # 调用信息更新方法，调用金币类更新类更新方法,实现金币闪烁
        self.info.draw(surface)