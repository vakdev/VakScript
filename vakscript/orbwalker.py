#built-in
from urllib.request import urlopen
from time import sleep
from ctypes import windll

#ext
from pyMeow import r_float
from orjson import loads
from win32api import GetCursorPos
from mouse import right_click

#own
from data import Offsets
from utils import send_key

"""
TODO:
    - Update windup formula from: https://leagueoflegends.fandom.com/wiki/Basic_attack
      and use GENERAL FORM for walk.Normal v2
    - Fix Kalista disconnect issue. 
"""

class Orbwalk:
    def __init__(self, process, base_address):
        self.process = process
        self.base_address = base_address
        self.can_attack_time = 0
        self.can_move_time = 0
        self.game_time_offset = Offsets.game_time

    def get_game_time(self):
        return r_float(self.process, self.base_address + self.game_time_offset)
    
    @staticmethod
    def get_attack_time():
        stats = loads(urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read())
        return stats["championStats"]["attackSpeed"]
    
    @staticmethod
    def get_windup_time(base_as, windup, windup_mod, c_attack_speed):
        if windup_mod:
            return (1. / base_as) * windup + ((1. / c_attack_speed * windup) - (1. / base_as) * windup) * windup_mod
        return (1. / base_as) * windup + ((1. / c_attack_speed * windup) - (1. / base_as) * windup)
    
    def walk(self, pos, attack_key, base_as, windup, windup_mod):
        game_time = self.get_game_time()
        c_attack_speed = self.get_attack_time()
        mouse_pos = GetCursorPos()
        if self.can_attack_time < game_time and pos:
            self.can_attack_time = game_time + 1. / c_attack_speed
            self.can_move_time = game_time + self.get_windup_time(base_as, windup, windup_mod, c_attack_speed)
            windll.user32.SetCursorPos(pos[0], pos[1])
            send_key(attack_key)
            sleep(0.01)
            windll.user32.SetCursorPos(mouse_pos[0], mouse_pos[1])
        elif self.can_move_time < game_time:
            windll.user32.SetCursorPos(mouse_pos[0], mouse_pos[1])
            sleep(0.1)
            right_click()

    def walk_v2(self, pos, attack_key, base_as, windup, windup_mod):
        # Will try to fix mouse issue. (moves cursor to target instead of walk.)
        game_time = self.get_game_time()
        c_attack_speed = self.get_attack_time()
        mouse_pos = GetCursorPos()
        if self.can_attack_time < game_time and pos:
            self.can_attack_time = game_time + 1. / c_attack_speed
            self.can_move_time = game_time + self.get_windup_time(base_as, windup, windup_mod, c_attack_speed)
            windll.user32.SetCursorPos(pos[0], pos[1])
            send_key(attack_key)
            sleep(0.01)
            windll.user32.SetCursorPos(mouse_pos[0], mouse_pos[1])
        elif self.can_move_time < game_time:
            windll.user32.SetCursorPos(mouse_pos[0], mouse_pos[1])
            sleep(0.1)
            right_click()

    def walk_inplace(self, pos, attack_key, base_as, windup, windup_mod):
        game_time = self.get_game_time()
        c_attack_speed = self.get_attack_time()
        if self.can_attack_time < game_time and pos:
            self.can_attack_time = game_time + 1. / c_attack_speed
            self.can_move_time = game_time + self.get_windup_time(base_as, windup, windup_mod, c_attack_speed)
            send_key(attack_key)
        elif self.can_move_time < game_time:
            sleep(0.1)
            right_click()

    def walk_kalista(self, pos, attack_key, *_):
        if pos:
            mouse_pos = GetCursorPos()
            windll.user32.SetCursorPos(pos[0],pos[1])
            send_key(attack_key)
            sleep(0.01)
            windll.user32.SetCursorPos(mouse_pos[0], mouse_pos[1])
            sleep(0.01)
            right_click()
            sleep(0.02)
        elif not pos:
            right_click()
            sleep(0.1)