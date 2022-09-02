#编写者：cwt
#时间：2022/7/4 20:39
#游戏入口
from source import tools,setup
from source.statues import main_menu,level,load_screen
import pygame

def main():
    state_dict = {
        'main_menu' : main_menu.MainMenu(),
        'load_screen' : load_screen.LoadScreen(),
        'level' : level.Level(),
        'game_over': load_screen.GameDver()

    }

    game=tools.Game(state_dict,'main_menu')   #初始化游戏主控
    # state=main_menu.MainMenu()   #初始化主页面
    # state = level.Level()
    # state = load_screen.LoadScreen()
    game.run()     #运行游戏

if __name__ == '__main__':
    main()