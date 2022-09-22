#编写者：cwt
#时间：2022/9/7 10:00
#关卡 2



from source.components import box as b


import json
import os
import random

from source.components import info,player,stuff,brick,box,enemy,plagpole
from source import tools,setup,constants,sound
import pygame

class Level2:
    def start(self,game_info,current_time):


        self.game_info=game_info
        self.finished= False
        self.next = 'game_over'
        self.info=info.Info('level1',self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_start_posotions()  # 新建起始位置的方法
        self.setup_player()
        self.setup_ground_items()
        self.setup_brick_and_box()
#        self.setup_enemy()
#        self.setup_checkpoints()  # 初始化检查点
 #       self.setup_flag()
        self.sound = sound.Sound(self)

    def load_map_data(self):
        file_name ='level_2.json'
        file_path = os.path.join('D:/Users/Administrator/PycharmProjects/superMario/source/data/maps/',file_name)
        with open(file_path) as f:
            self.map_data= json.load(f)

    def setup_background(self):
        self.image_name = self.map_data['image_name']  # 获取关卡名称
        self.background = setup.GRAPHICS[self.image_name]  # 按照关卡名取出关卡图
        rect = self.background.get_rect()  # 获取背景图矩形边框
        self.background = pygame.transform.scale(self.background, (int(rect.width * constants.BG_MULTI),
                                                                   int(rect.height * constants.BG_MULTI)))  # 放大
        self.background_rect = self.background.get_rect()
        self.game_window = setup.SCREEN.get_rect()  # 获得显示窗口大小
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))  # 新建一个背景大小般的图层

    def setup_start_posotions(self):
        self.positions=[]
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'],data['end_x'],data['player_x'],data['player_y']))
        self.start_x,self.end_x,self.player_x,self.player_y=self.positions[0]

    def setup_player(self):
        self.player = player.Player('mario')  # 初始化角色精灵
        # self.player.rect.x = 300
        # self.player.rect.y = 490
        self.player.rect.x = self.game_window.x + self.player_x  # 让角色所处矩形的位置为滑动窗口的位置加上角色的x坐标
        #self.player.rect.bottom = self.player_y
        self.player.rect.bottom=500

    def setup_ground_items(self):
        self.ground_items_group = pygame.sprite.Group()  # 创建一个精灵组,把实例化的物品都放到这个组里，方便之后的批量处理
        for name in ['ground', 'pipe', 'step']:  # 大地，管道，楼梯
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def setup_brick_and_box(self):
        self.brick_group = pygame.sprite.Group() #存放砖块
        self.box_group= pygame.sprite.Group()   #存放宝箱
        self.coin_group=pygame.sprite.Group()  #存放开箱出来的金币
        self.powerup_group = pygame.sprite.Group()  #存放开箱的道具

        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x,y=brick_data['x'],brick_data['y']
                brick_type = brick_data['type']
                if brick_type == 0:
                    if 'brick_num' in brick_data:
                        # TODO batch bricks
                        pass
                    else:
                        self.brick_group.add(brick.Brick(x,y,brick_type,None)) #砖块精灵加入砖块组
                        #print('test',brick.Brick(x,y,brick_type))
                elif brick_type == 1:
                    self.brick_group.add(brick.Brick(x,y,brick_type,self.coin_group))
                else:
                    self.brick_group.add(brick.Brick(x,y,brick_type,self.powerup_group))
        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x, y = box_data['x'], box_data['y']
                box_data = box_data['type']
                if box_data == 1:
                    self.box_group.add(box.Box(x, y, box_data,self.coin_group))
                else:
                    self.box_group.add(box.Box(x, y, box_data,self.powerup_group))


    def update(self, surface, keys, current_time):
        print(self.player.rect.x,self.player.image)
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys, self)
        self.info.update(self.game_info)
        # setup.SOUND['big_jump'].play()
        # print( setup.MUSIC)

        if self.player.dead:
            if self.current_time - self.player.death_timer > 3000:
                self.finished = True
                self.update_game_info()  # 当Mario阵亡时更新数据
        elif self.is_frozen():  # 变身状态，场景冻结
            pass
        else:

            #self.text_info_group.update(self)
            #self.update_player_position()
            #self.check_checkpoints()
            #self.check_if_go_die()
            #self.update_game_window()
            self.brick_group.update(self)  # 刷新精灵图，使其相应效果生效
            self.box_group.update(self)
            #self.enemy_group.update(self)  # 需要传入level对象
            #self.dying_group.update(self)
            #self.shell_group.update(self)
           # self.coin_group.update(self)
            #self.powerup_group.update(self)
            #self.pole_group.update()
            #self.flag_group.update()
            #self.finial_group.update()

            #self.is_or_not_finished()

            # for enemy_group in self.enemy_group_dict.values():
            #     enemy_group.update(self) #直接把level这个实例传过去了
            # self.enemy_group.update()
        self.sound.update(self.game_info, self.player)

        # setup.MUSIC['main_theme'].play()
        self.draw(surface)

    def is_or_not_finished(self):
        # print(self.player.baoqi,self.player.rect.y)
        if self.player.baoqi == True and self.player.rect.y > 400:
            self.finished = True
            self.next = 'load_level2'

    def is_frozen(self):
        return self.player.state in ['small2big', 'big2small', 'big2fire', 'fire2small', 'livesAdd1']

    def draw(self, surface):

        self.game_ground.blit(self.background, (self.game_window.x, self.game_window.y), self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        print(self.player.image,self.player.rect.x,self.player.rect.y,self.game_ground,'//11111')

        #self.text_info_group.draw(self.game_ground)
        #self.powerup_group.draw(self.game_ground)

        self.brick_group.draw(self.game_ground)  # 画出精灵组内容
        self.box_group.draw(self.game_ground)  # 画出精灵组内容


        surface.blit(self.game_ground, (0, 0), self.game_window)
        # surface.blit(self.background,(0,0),self.game_window) #blit方法把目标图层的特定部分画到原图层的指定位置，第一个参数为目标图层，第三个参数为特定部分不写则为全部，第二个
        #                                     #参数为目标左上角放在原图层的位置
        # surface.blit(self.player.image, self.player.rect)
        self.info.update(self.game_info)  # 调用信息更新方法，调用金币类更新类更新方法,实现金币闪烁
        self.info.draw(surface)



    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next = 'game_over'
        else:
            self.next = 'load_screen'

