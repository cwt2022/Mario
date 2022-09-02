#编写者：cwt
#时间：2022/7/4 21:23
#关卡
import json
import os

from source.components import info,player,stuff,brick,box,enemy
from source import tools,setup,constants
import pygame

class Level:
    def start(self,game_info):
        self.game_info=game_info
        self.finished= False
        self.next = 'game_over'
        self.info=info.Info('level',self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_start_posotions()#新建起始位置的方法
        self.setup_player()
        self.setup_ground_items()
        self.setup_brick_and_box()
        self.setup_enemy()
        self.setup_checkpoints()    #初始化检查点


    def load_map_data(self):
        file_name ='level_1.json'
        file_path = os.path.join('D:/Users/Administrator/PycharmProjects/superMario/source/data/maps/',file_name)
        with open(file_path) as f:
            self.map_data= json.load(f)
    def setup_background(self):
        self.image_name=self.map_data['image_name']
        self.background = setup.GRAPHICS[self.image_name]
        rect =self.background.get_rect()
        self.background = pygame.transform.scale(self.background,(int(rect.width*constants.BG_MULTI),
                                                             int(rect.height*constants.BG_MULTI)))
        self.background_rect = self.background.get_rect()
        self.game_window=setup.SCREEN.get_rect()  #获得窗口大小
        self.game_ground= pygame.Surface((self.background_rect.width,self.background_rect.height))#新建一个背景大小般的图层

    def setup_start_posotions(self):
        self.positions=[]
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'],data['end_x'],data['player_x'],data['player_y']))
        self.start_x,self.end_x,self.player_x,self.player_y=self.positions[0]
    def setup_ground_items(self):
        self.ground_items_group=pygame.sprite.Group() #创建一个精灵组,把实例化的物品都放到这个组里，方便之后的批量处理
        for name in ['ground','pipe','step']:  #大地，管道，楼梯
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'],item['y'],item['width'],item['height'],name))

    def setup_player(self):
        self.player =player.Player('mario')
        # self.player.rect.x = 300
        # self.player.rect.y = 490
        self.player.rect.x=self.game_window.x+self.player_x
        self.player.rect.bottom=self.player_y

    def setup_brick_and_box(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group= pygame.sprite.Group()
        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x,y=brick_data['x'],brick_data['y']
                brick_type = brick_data['type']
                if 'brick_num' in brick_data:
                    # TODO batch bricks
                    pass
                else:
                    self.brick_group.add(brick.Brick(x,y,brick_type))
                    #print('test',brick.Brick(x,y,brick_type))

        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x, y = box_data['x'], box_data['y']
                box_data = box_data['type']
                self.box_group.add(box.Box(x, y, box_data))

    '''myself'''
    # def setup_enemy(self):
    #     self.enemy_group = pygame.sprite.Group()
    #     list_test=[]
    #     if 'enemy' in self.map_data:
    #         #print(self.map_data['enemy'])
    #         for enemy_data in self.map_data['enemy']:
    #            # print(enemy_data,type(enemy_data))
    #             for key,values in enemy_data.items():
    #                 #print(key,values)
    #             # if enemy_data['0']:
    #             #     test=enemy_data['0']
    #             #     #print(test)
    #                 for index in values:
    #                     x,y=index['x'],index['y']
    #                     direction=index['direction']
    #                     type=index['direction']
    #                     color=index['color']
    #                     self.enemy_group.add(enemy.Enemy(x,y,direction,type))
    #                     #print(x,y,color,type,direction)
    #
    #     print(self.enemy_group)
    #                 #     pass

    def setup_enemy(self):
        self.dying_group = pygame.sprite.Group() #野怪死亡后加入该组
        self.shell_group= pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group_dict = {}
        if 'enemy' in self.map_data:
             for enemy_group_data in self.map_data['enemy']:
                group = pygame.sprite.Group()#放置所有野怪
                for enemy_group_id, enemy_list in enemy_group_data.items():
                    for enemy_data in enemy_list:
                        #print(enemy_data)
                        group.add(enemy.create_enemy(enemy_data))
                       # print('55555555555555',group)
                    self.enemy_group_dict[enemy_group_id]=group


    def setup_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x,y,w,h=item['x'],item['y'],item['width'],item['height']
            checkpoint_type =item['type']
            enemy_groupid=item.get('enemy_groupid') #组号并不是每个都有，为了避免报错
            self.checkpoint_group.add(stuff.Checkpoint(x,y,w,h,checkpoint_type,enemy_groupid))

    def update(self,surface,keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys)

        if self.player.dead:
            if self.current_time - self.player.death_timer >3000:
                self.finished =True
                self.update_game_info() #当Mario阵亡时更新数据
        else:

            self.update_player_position()
            self.check_checkpoints()
            self.check_if_go_die()
            self.update_game_window()
            self.brick_group.update() #刷新精灵图，使其相应效果生效
            self.box_group.update()
            self.enemy_group.update(self)
            self.dying_group.update(self)
            self.shell_group.update(self)
            # for enemy_group in self.enemy_group_dict.values():
            #     enemy_group.update(self) #直接把level这个实例传过去了
            #self.enemy_group.update()
        self.draw(surface)

    def update_player_position(self): #更新人物位置

        '''x direction'''
        # print(self.player.rect.x,self.player.x_vel)
        self.player.rect.x +=self.player.x_vel  #得数会向下取整
        #
        # '''让人物不会超出屏幕'''
        # if self.player.rect.x-self.game_window.x<0:
        #     self.player.rect.x=self.game_window.x


        if self.player.rect.x < self.start_x:
            self.player.rect.x =self.start_x
        elif self.player.rect.right>self.end_x:
            self.player.rect.right=self.end_x
        # if self.player.rect.x >constants.SCREEN_W-16*constants.PLAYER_MULTI:
        #     self.player.rect.x=constants.SCREEN_W-16*constants.PLAYER_MULTI

        self.check_x_collisions() #x方向撞到敌人

        '''y diretion'''
        if not self.player.dead:  #如果mario没有死亡，则继续，死亡了就不需要进行y方向碰撞检测了
            self.player.rect.y +=self.player.y_vel
            self.check_y_collisions()  #y方向为顶起了砖块，或者踩到了龟壳
           # print("水平坐标",self.player.rect.x,self.player.rect.y)

    def check_x_collisions(self):
        '''检查一个精灵是否与精灵组里任意一个精灵有碰撞，会返回第一个Mario碰撞的精灵，没有碰撞则为空'''
        check_group=pygame.sprite.Group(self.ground_items_group,self.brick_group,self.box_group)#两个精灵组的精灵都加进新的精灵组
        ground_item =pygame.sprite.spritecollideany(self.player,check_group)

        if ground_item:
            self.adjust_player_x(ground_item)
        enemy=pygame.sprite.spritecollideany(self.player,self.enemy_group)
        if enemy:
            self.player.go_die()

        shell=pygame.sprite.spritecollideany(self.player,self.shell_group)
        if shell:
            if shell.state =='slide': #虽然乌龟变成龟壳加入龟壳组了，但它本质上还是乌龟
                self.player.go_die()
            else:
                if self.player.rect.x < shell.rect.x:
                    shell.x_vel = 10
                    shell.rect.x += 40
                    shell.direction =1
                else:
                    shell.x_vel = -10
                    shell.rect.x -=40
                    shell.direction=0
                shell.state = 'slide'

    def check_y_collisions(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group,self.box_group)
        ground_item = pygame.sprite.spritecollideany(self.player, check_group)

        if ground_item:
            self.adjust_player_y(ground_item)


        enemy =pygame.sprite.spritecollideany(self.player,self.enemy_group)
        if enemy:

            self.enemy_group.remove(enemy)#移出野怪组
            if enemy.name == 'koopa':
                self.shell_group.add(enemy)
            else:
                self.dying_group.add(enemy)#进入死亡组

            if self.player.y_vel<0:
                how = 'bumped'  #bumped凸起的，速度小于0往上的
            else:
                how = 'trampled' #trampled践踏，从上往下
                self.player.state == 'jump'
                self.player.rect.bottom =enemy.rect.top
                self.player.y_vel =self.player.jump_velocity *0.8
            enemy.go_die(how)
            print(self.dying_group)

        self.check_will_fail(self.player)
    def adjust_player_x(self,sprite):
        if self.player.rect.x< sprite.rect.x: #如果Mario从右边撞到了物体的最左边
            self.player.rect.right=sprite.rect.left #让Mario的最右边等于物体最左边
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel=0
    def adjust_player_y(self,sprite):
        if self.player.rect.bottom<sprite.rect.bottom:  #从上往下撞击
            self.player.y_vel =0
            self.player.rect.bottom =sprite.rect.top
            self.player.state='walk'
        else:
            self.player.y_vel=7
            self.player.rect.top=sprite.rect.bottom
            self.player.state='fall'
    def check_will_fail(self,sprite):#坠落检测
        '''让该精灵下坠1px,没有发生碰撞则为设置为下坠状态'''
        sprite.rect.y+=1
        check_ground=pygame.sprite.Group(self.ground_items_group,self.brick_group,self.box_group)
        collided=pygame.sprite.spritecollideany(sprite,check_ground)
        if not collided and sprite.state !='jump':
            sprite.state='fall'
        sprite.rect.y-=1
    def update_game_window(self):

        third=self.game_window.x+self.game_window.width/3 #先计算出窗口的三分之一
        if self.player.x_vel > 0 and self.player.rect.x > third and self.game_window.right<self.end_x: #?为何要用centerx
            self.game_window.x +=self.player.x_vel
            self.start_x=self.game_window.x


    def draw(self,surface):
        self.game_ground.blit(self.background,(self.game_window.x,self.game_window.y),self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        self.brick_group.draw(self.game_ground)  #画出精灵组内容
        self.box_group.draw(self.game_ground)  # 画出精灵组内容
        #self.enemy_group.draw((self.game_ground))

        self.enemy_group.draw(self.game_ground)
        self.dying_group.draw(self.game_ground)
        self.shell_group.draw(self.game_ground)
        # for enemy_group in self.enemy_group_dict.values():
        #     enemy_group.draw(self.game_ground)


        surface.blit(self.game_ground, (0, 0),self.game_window)
        # surface.blit(self.background,(0,0),self.game_window) #blit方法把目标图层的特定部分画到原图层的指定位置，第一个参数为目标图层，第三个参数为特定部分不写则为全部，第二个
        #                                     #参数为目标左上角放在原图层的位置
        # surface.blit(self.player.image, self.player.rect)
        self.info.update()  # 调用信息更新方法，调用金币类更新类更新方法,实现金币闪烁
        self.info.draw(surface)

    def check_checkpoints(self):
        checkpoint = pygame.sprite.spritecollideany(self.player,self.checkpoint_group)
        if checkpoint:
            if checkpoint.checkpoint_type == 0 : #checkpoint for enemy appearance
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])
            checkpoint.kill()

    def check_if_go_die(self):
        if self.player.rect.y > constants.SCREEN_H:
            self.player.go_die()
    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -=1
        if self.game_info['lives'] ==0:
            self.next='game_over'
        else:
            self.next='load_screen'