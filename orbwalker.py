#ext
from orjson import loads
from urllib.request import urlopen
from pyMeow import r_float
from win32api import GetCursorPos
from time import sleep
from mouse import right_click
from ctypes import windll

#own
from data import Offsets
from utils import send_key

#
SetCursorPos = windll.user32.SetCursorPos

class Orbwalk:
    def __init__(self, process, base_address):
        self.can_attack_time = 0
        self.can_move_time = 0
        self.process = process
        self.base_address = base_address
        self.game_time = Offsets.game_time

    def get_game_time(self):
        return r_float(self.process, self.base_address + self.game_time)
    
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
        c_attack_speed = Orbwalk.get_attack_time()
        if self.can_attack_time < game_time and pos:
            mouse_pos = GetCursorPos()
            self.can_attack_time = game_time + 1. / c_attack_speed
            self.can_move_time = game_time + Orbwalk.get_windup_time(base_as, windup, windup_mod, c_attack_speed)
            SetCursorPos(int(pos[0]),int(pos[1]))
            send_key(attack_key)
            sleep(0.01)
            SetCursorPos(int(mouse_pos[0]), int(mouse_pos[1]))
        elif self.can_move_time < game_time:
            sleep(0.03)
            right_click()
        
    def walk_v2(self, pos, attack_key, base_as, windup, windup_mod):
        game_time = self.get_game_time()
        c_attack_speed = Orbwalk.get_attack_time()
        if self.can_attack_time < game_time and pos:
            self.can_attack_time = game_time + 1. / c_attack_speed
            mouse_pos = GetCursorPos()
            SetCursorPos(int(pos[0]),int(pos[1]))
            send_key(attack_key)
            sleep(0.01)
            SetCursorPos(int(mouse_pos[0]), int(mouse_pos[1]))
            sleep(Orbwalk.get_windup_time(base_as, windup, windup_mod, c_attack_speed))
        else:
            sleep(0.03)
            right_click()

    def walk_inplace(self, pos, attack_key, base_as, windup, windup_mod):
        game_time = self.get_game_time()
        c_attack_speed = Orbwalk.get_attack_time()
        if self.can_attack_time < game_time and pos:
            send_key(attack_key)
            self.can_attack_time = game_time + 1. / c_attack_speed
            sleep(Orbwalk.get_windup_time(base_as, windup, windup_mod, c_attack_speed))
        else:
            sleep(.1 / c_attack_speed)
            right_click()

    def walk_kalista(self, pos, attack_key, *_):
        if pos:
            mouse_pos = GetCursorPos()
            SetCursorPos(int(pos[0]),int(pos[1]))
            send_key(attack_key)
            sleep(0.01)
            SetCursorPos(int(mouse_pos[0]), int(mouse_pos[1]))
            sleep(0.01)
            right_click()
            sleep(0.02)
        elif not pos:
            right_click()
            sleep(0.03)
