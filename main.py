#编写者：cwt
#时间：2022/7/4 20:39
#游戏入口
from source import tools,setup
from source.statues import main_menu,level,load_screen,level2
import pygame

def main():
    state_dict = {
        'main_menu' : main_menu.MainMenu(),
        'load_screen' : load_screen.LoadScreen(),
        'level' : level.Level(),
        'game_over': load_screen.GameDver(),
        'level2': level.Level2(),
        'load_level2': load_screen.Load_level2(),
        'level3': level.Level3(),
        'load_level3': load_screen.Load_level3(),
        'level4': level.Level4(),
        'load_level4': load_screen.Load_level4()

    }
    '''test'''
    game=tools.Game(state_dict,'main_menu')   #初始化游戏主控
    # state=main_menu.MainMenu()   #初始化主页面
    # state = level.Level()
    # state = load_screen.LoadScreen()
    game.run()     #运行游戏

if __name__ == '__main__':
    main()