#编写者：cwt
#时间：2022/7/4 21:24
#常量

SCREEN_W,SCREEN_H=800,600
SCREEN_SIZE=(SCREEN_W,SCREEN_H)
GROUND_HEIGHT=SCREEN_H-62 #地板高度

ENEMY_MULTI = 2.5
BG_MULTI = 2.68
PLAYER_MULTI = 2.9
BRICK_MULTI = 2.69 #砖块放大倍数
ENEMY_SPEED = 1

GRAVITY = 1.0 #重力加速度
ANYI_GRAVITY = 0.3 #上升加速度，Mario可以反重力能力

FONT='FixedSys.ttf'

#Mario States

STAND = 'standing'
WALK = 'walk'
JUMP = 'jump'
FALL = 'fall'
SMALL_TO_BIG = 'small to big'
BIG_TO_FIRE = 'big to fire'
BIG_TO_SMALL = 'big to small'
FLAGPOLE = 'flag pole'
WALKING_TO_CASTLE = 'walking to castle'
END_OF_LEVEL_FALL = 'end of level fall'


#GAME INFO DICTIONARY KEYS
COIN_TOTAL = 'coin total'
SCORE = 'score'
TOP_SCORE = 'top score'
LIVES = 'lives'
CURRENT_TIME = 'current time'
LEVEL_STATE = 'level state'
CAMERA_START_X = 'camera start x'
MARIO_DEAD = 'mario dead'

#OVERHEAD INFO STATES
MAIN_MENU = 'main menu'
LOAD_SCREEN = 'loading screen'
LEVEL = 'level'
GAME_OVER = 'game_over'
FAST_COUNT_DOWN = 'fast count down'
END_OF_LEVEL = 'end of level'

#SOUND STATEZ
NORMAL = 'normal'
STAGE_CLEAR = 'stage clear'
WORLD_CLEAR = 'world clear'
TIME_WARNING = 'time warning'
SPED_UP_NORMAL = 'sped up normal'
MARIO_INVINCIBLE = 'mario invincible'
