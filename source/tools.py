#编写者：cwt
#时间：2022/7/4 21:25
#工具和游戏主控

import pygame
import random
import os


class Game():
    def __init__(self,state_dict,start_state):
        # pygame.init()
        # pygame.display.set_mode((800, 600))
        # pygame.display.set_caption('嘎嘎嘎嘎嘎')
        self.screen=pygame.display.get_surface() #获取当前显示的 Surface 对象,获得屏幕
        self.clock=pygame.time.Clock()#创建一个时钟，控制帧率
        self.keys=pygame.key.get_pressed() #获取按键状态
        self.state_dict=state_dict  #获取主菜单的状态字典
        self.state=self.state_dict[start_state] #保存传入的状态（初始化该状态的类）
        self.current_time = 0.0

    def update(self):
        if self.state.finished: #判断该状态是否结束
            game_info=self.state.game_info
            next_state=self.state.next
            self.state.finished=False
            self.state=self.state_dict[next_state]
            self.state.start(game_info,self.current_time)
        self.state.update(self.screen,self.keys,self.current_time)  #当前状态为结束，调用该状态的更新方法

    def run(self):

        while True:

            for event in pygame.event.get():  # 循环获取事件，监听事件状态
                if event.type == pygame.QUIT:   # 判断用户是否点了"X"关闭按钮,并执行if代码段
                    pygame.display.quit()
                    quit()
                elif event.type == pygame.KEYDOWN: #监听按键是否按下
                    self.keys=pygame.key.get_pressed() #获取所有按键的状态 返回值为bool,通过keys常量作为索引

                elif event.type == pygame.KEYUP:
                    self.keys=pygame.key.get_pressed() #此时返回值为False

            self.update()
            # self.screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            # image=get_image(GRAPHICS['mario_bros'],145,32,16,16,(0,0,0),1)
            # self.screen.blit(image,(300,300))

            pygame.display.update()
            self.clock.tick(60)
def load_graphics(path,accept=('.jpg','.png','.bmp','.gif')):
    graphics={}
    for pic in os.listdir(path):
        name,ext=os.path.splitext(pic)
        # print(name,ext)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path,pic))
            if img.get_alpha(): #判断图片是否是透明底格式，抠完图专用的
                img=img.convert_alpha() #convert_alpha()方法会使用透明的方法绘制前景对象
                # print(img,type(img))
            else:
                img=img.convert()
                # print(img, type(img))
            graphics[name] = img
    return graphics

def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    songs = {}
    for song in os.listdir(directory):
        name, ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs

def load_all_sound(directory, accept=('.wav','.mpe','.ogg','.mdi')):

    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pygame.mixer.Sound(os.path.join(directory, fx))
    return effects

def get_image(sheet,x,y,width,height,colorkey,scale):
    image = pygame.Surface((width,height)) #创建一个和方框一样大的一个图层
    image.blit(sheet,(0,0),(x,y,width,height))#pygame.Surface.blit() 将一个图像（Surface 对象）绘制到另一个图像上  第一个参数为图片，第二个为坐标，第三个为
    image.set_colorkey(colorkey)  #将该颜色设置为透明
    image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
    return image


class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def start(self,persistant,current_time):
        self.persist = persistant
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        pass


if __name__ == '__main__':
    game=Game()
    game.run()

