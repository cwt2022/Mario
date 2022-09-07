#编写者：cwt
#时间：2022/7/4 21:25
#启动代码

import pygame
from . import constants as C
from . import tools
import os

pygame.init()
pygame.mixer.init()
print('执行了')
SCREEN=pygame.display.set_mode((C.SCREEN_W,C.SCREEN_H)) #屏幕
pygame.display.set_caption('嘎嘎嘎嘎嘎')

GRAPHICS=tools.load_graphics('D:\\Users\\Administrator\\PycharmProjects\\superMario\\resources\\graphics')
MUSIC = tools.load_all_music(os.path.join("resources","music"))
SOUND   = tools.load_all_sound(os.path.join("resources","sound"))