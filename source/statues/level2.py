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
        self.setup_enemy()
        self.setup_checkpoints()  # 初始化检查点
 #       self.setup_flag()
        self.sound = sound.Sound(self)

    def load_map_data(self):
        file_name ='level_4.json'
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
        # print(self.player_y)
        #test
        self.player.rect.bottom=300

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

    def setup_enemy(self):
        self.dying_group = pygame.sprite.Group() #野怪死亡后加入该组
        self.shell_group= pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.text_info_group=pygame.sprite.Group()
        self.enemy_group_dict = {}
        if 'enemy' in self.map_data:
             for enemy_group_data in self.map_data['enemy']:
                group = pygame.sprite.Group()#放置所有野怪
                for enemy_group_id, enemy_list in enemy_group_data.items():
                    for enemy_data in enemy_list:
                        print(enemy_data)
                        group.add(enemy.create_enemy(enemy_data))
                        print('55555555555555',group)
                    self.enemy_group_dict[enemy_group_id]=group

    def setup_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x, y, w, h = item['x'], item['y'], item['width'], item['height']
            checkpoint_type = item['type']
            enemy_groupid = item.get('enemy_groupid')  # 组号并不是每个都有，为了避免报错
            self.checkpoint_group.add(stuff.Checkpoint(x, y, w, h, checkpoint_type, enemy_groupid))

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

            self.text_info_group.update(self)
            self.update_player_position()
            self.check_checkpoints()
            #self.check_if_go_die()
            self.update_game_window()
            self.brick_group.update(self)  # 刷新精灵图，使其相应效果生效
            self.box_group.update(self)
            self.enemy_group.update(self)  # 需要传入level对象
            self.dying_group.update(self)
            self.shell_group.update(self)
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

    def check_checkpoints(self):
        checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)
        if checkpoint:
            if checkpoint.checkpoint_type == 0:  # checkpoint for enemy appearance
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])
            checkpoint.kill()

    def update_player_position(self):  # 更新人物位置

        '''x direction'''
        # print(self.player.rect.x,self.player.x_vel)
        self.player.rect.x += self.player.x_vel  # 得数会向下取整
        #
        # '''让人物不会超出屏幕'''
        # if self.player.rect.x-self.game_window.x<0:
        #     self.player.rect.x=self.game_window.x

        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        # if self.player.rect.x >constants.SCREEN_W-16*constants.PLAYER_MULTI:
        #     self.player.rect.x=constants.SCREEN_W-16*constants.PLAYER_MULTI
        '''TOOP'''
        self.check_x_collisions()  # x方向撞到敌人

        '''y diretion'''
        if not self.player.dead:  # 如果mario没有死亡，则继续，死亡了就不需要进行y方向碰撞检测了
            self.player.rect.y += self.player.y_vel
            '''TOOP'''
            self.check_y_collisions()  # y方向为顶起了砖块，或者踩到了龟壳
        # print("水平坐标",self.player.rect.x,self.player.rect.y)

    def check_x_collisions(self):
        '''检查一个精灵是否与精灵组里任意一个精灵有碰撞，会返回第一个Mario碰撞的精灵，没有碰撞则为空'''
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)  # 两个精灵组的精灵都加进新的精灵组
        ground_item = pygame.sprite.spritecollideany(self.player, check_group)

        #player_colided_flag = pygame.sprite.spritecollideany(self.player, self.pole_group)


        # self.player.baoqi = False
        # if player_colided_flag:
        #     #print('发生碰撞')
        #     self.player.baoqi = True
        #     self.game_info['score'] += 1000
        #     self.adjust_player_x(player_colided_flag)
        if ground_item:

            self.adjust_player_x(ground_item)

        if self.player.hurt_imune:
            return

        # enemy=pygame.sprite.spritecollideany(self.player,self.enemy_group)
        # if enemy:
        #     if self.player.big:
        #         self.player.state ='big2small'
        #         self.player.hurt_imune =True #伤害免疫
        #     else:
        #         self.player.go_die()

        # shell=pygame.sprite.spritecollideany(self.player,self.shell_group)
        # if shell:
        #     if shell.state =='slide': #虽然乌龟变成龟壳加入龟壳组了，但它本质上还是乌龟
        #         if self.player.big:
        #             self.player.state = 'big2small'
        #             self.player.hurt_imune = True  # 伤害免疫
        #         else:
        #             self.player.go_die()
        #     else:
        #         if self.player.rect.x < shell.rect.x:
        #             shell.x_vel = 10
        #             shell.rect.x += 40
        #             shell.direction =1
        #         else:
        #             shell.x_vel = -10
        #             shell.rect.x -=40
        #             shell.direction=0
        #         shell.state = 'slide'
        # powerup=pygame.sprite.spritecollideany(self.player,self.powerup_group)
        # if powerup:
        #
        #     if powerup.name=='fireball':
        #         pass
        #         #print(powerup.rect.x,powerup.rect.y)
        #         #print('发球')
        #
        #     elif powerup.name=='mushroom' :
        #         self.game_info['score'] += 1000
        #         setup.SOUND['pipe'].play()#变身
        #         self.player.state = 'small2big'
        #         powerup.kill()
        #     elif powerup.name=='fireflower':
        #         self.game_info['score'] += 1000
        #         setup.SOUND['powerup'].play()
        #         self.player.state ='big2fire'
        #         powerup.kill()
        #     elif powerup.name == 'lifemushroom':
        #         self.game_info['score'] += 1000
        #         setup.SOUND['powerup'].play()
        #        #可以给人物加一个状态，头上显示生命+1
        #         self.player.state='livesAdd1'
        #         self.game_info['lives'] +=1
        #         powerup.kill()
        #     elif powerup.name == 'star':
        #         self.game_info['score'] += 1000
        #         setup.SOUND['powerup'].play()
        #         self.player.hurt_imune = True  # 伤害免疫
        #         powerup.kill()
        #print(self.player.state)

    def check_y_collisions(self):
        # check_group = pygame.sprite.Group( self.ground_items_group,self.brick_group,self.box_group)
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        brick = pygame.sprite.spritecollideany(self.player, self.brick_group)
        box = pygame.sprite.spritecollideany(self.player, self.box_group)
        print(ground_item,'dadi')
        #enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        # ground_item = pygame.sprite.spritecollideany(self.player, self.brick_group)
        #
        # if ground_item:
        #     self.adjust_player_y(ground_item)
        if brick and box:
            to_brick = abs(self.player.rect.centerx - brick.rect.centerx)
            to_box = abs(self.player.rect.centerx - box.rect.centerx)
            if to_brick > to_box:
                brick = None
            else:
                box = None
        if ground_item:
            self.adjust_player_y(ground_item)
        elif brick:
            self.adjust_player_y(brick)

        elif box:
            self.adjust_player_y(box)
        # elif enemy and not self.is_frozen():
        #     if self.player.hurt_imune:
        #         return
        #     self.text_info_group.add(b.Text_info(enemy.rect.x, enemy.rect.y, '+ 100'))
        #
        #     self.enemy_group.remove(enemy)  # 移出野怪组  ??
        #     # print(self.game_info['score'])
        #     self.game_info['score'] += 100
        #     # (self.game_info['score'])
        #     if enemy.name == 'koopa':
        #         self.shell_group.add(enemy)
        #
        #     else:
        #         self.dying_group.add(enemy)  # 进入死亡组
        #
        #     if self.player.y_vel < 0:
        #         how = 'bumped'  # bumped凸起的，速度小于0往上的
        #     else:
        #         setup.SOUND['stomp'].play()  # 踩死小野怪的声音
        #         how = 'trampled'  # trampled践踏，从上往下
        #         self.player.state == 'jump'
        #         self.player.rect.bottom = enemy.rect.top
        #         self.player.y_vel = self.player.jump_velocity * 0.8
        #     enemy.go_die(how, 1 if self.player.face_rigth else -1)
        #     # print(self.dying_group)

        self.check_will_fail(self.player)

    def adjust_player_x(self,sprite):
        if self.player.rect.x< sprite.rect.x: #如果Mario从右边撞到了物体的最左边
            self.player.rect.right=sprite.rect.left #让Mario的最右边等于物体最左边
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel=0

    def adjust_player_y(self, sprite):
        # downwards
        print('调整y')
        if self.player.rect.bottom < sprite.rect.bottom:  # 从上往下撞击
            print(self.player.rect.bottom, sprite.rect.bottom, '第二关')
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'
        # upwards
        else:
            self.player.y_vel = 7
            self.player.rect.top = sprite.rect.bottom
            self.player.state = 'fall'

            # 判断上方是否有敌人
            #self.is_enemy_on(sprite)

            if sprite.name == 'box':
                if sprite.state == 'rest':
                    sprite.go_bumped()
                    setup.SOUND['coin'].play()
                    self.game_info['coin'] += 1
                    self.game_info['score'] += 200
            if sprite.name == 'brick':
                if sprite.brick_type == 1 and sprite.state == 'rest':
                    #self.text_info_group.add(b.Text_info(sprite.rect.x, sprite.rect.y, '+ 100'))
                    self.game_info['score'] += 100
                    self.game_info['coin'] += 1
                if self.player.big and sprite.brick_type == 0:  # when mario is big and brick contains nothing
                    setup.SOUND['brick_smash'].play()  # 大mario撞碎砖块声音
                    sprite.smashed(self.dying_group)
                if sprite.state == 'rest':
                    sprite.go_bumped()  # 小mario撞击砖块声音
                    setup.SOUND['bump'].play()

    def check_will_fail(self,sprite):#坠落检测
        '''让该精灵下坠1px,没有发生碰撞则为设置为下坠状态'''
        sprite.rect.y+=1
        check_ground=pygame.sprite.Group(self.ground_items_group,self.brick_group,self.box_group)
        collided=pygame.sprite.spritecollideany(sprite,check_ground)
        if not collided and sprite.state !='jump' and not self.is_frozen():
            sprite.state='fall'
        sprite.rect.y-=1
        #print('掉落检测')

    def is_or_not_finished(self):
        # print(self.player.baoqi,self.player.rect.y)
        if self.player.baoqi == True and self.player.rect.y > 400:
            self.finished = True
            self.next = 'load_level2'

    def is_frozen(self):
        return self.player.state in ['small2big', 'big2small', 'big2fire', 'fire2small', 'livesAdd1']

    def update_game_window(self):

        third = self.game_window.x + self.game_window.width / 3  # 先计算出窗口的三分之一
        if self.player.x_vel > 0 and self.player.rect.x > third and self.game_window.right < self.end_x:  # ?为何要用centerx
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x

    def draw(self, surface):

        self.game_ground.blit(self.background, (self.game_window.x, self.game_window.y), self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        #print(self.player.image,self.player.rect.x,self.player.rect.y,self.game_ground,'//11111')

        self.text_info_group.draw(self.game_ground)
        #self.powerup_group.draw(self.game_ground)

        self.brick_group.draw(self.game_ground)  # 画出精灵组内容
        self.box_group.draw(self.game_ground)  # 画出精灵组内容

        self.enemy_group.draw(self.game_ground)
        self.dying_group.draw(self.game_ground)
        self.shell_group.draw(self.game_ground)

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

