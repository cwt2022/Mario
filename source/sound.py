#编写者：cwt
#时间：2022/7/4 21:24
#音乐相关

import pygame as pg
from . import setup
from . import constants as c

class Sound(object):
    """Handles all sound for the game"""
    def __init__(self, level):
        """Initialize the class"""
        self.sound_dict = setup.SOUND
        self.music_dict = setup.MUSIC
        self.level =level
        # self.overhead_info = overhead_info
        # self.game_info = overhead_info.game_info
        self.set_music_mixer()



    def set_music_mixer(self):
        """Sets music for level"""
        if self.level.player.dead:
            pg.mixer.music.load(self.music_dict['death'])
            pg.mixer.music.play()
            self.state = c.GAME_OVER
        else:

            pg.mixer.music.load(self.music_dict['main_theme'])
            pg.mixer.music.play()
            self.state = c.NORMAL


    def update(self, game_info, mario):
        """Updates sound object with game info"""
        self.game_info = game_info
        self.mario = mario
        self.handle_state()

    def  handle_state(self):
        """Handles the state of the soundn object"""
        #print('444')
        if self.state == c.NORMAL:

            if self.mario.dead:
                self.play_music('death', c.MARIO_DEAD)


    def play_music(self, key, state):
        """Plays new music"""
        pg.mixer.music.load(self.music_dict[key])
        pg.mixer.music.play()
        self.state = state

    def stop_music(self):
        """Stops playback"""
        pg.mixer.music.stop()



