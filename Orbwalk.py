#ext
from orjson import loads
from urllib.request import urlopen
from pyMeow import r_float
from win32api import GetCursorPos
from time import sleep
from keyboard import send
from mouse import right_click
from ctypes import windll

#own
from Data import Offsets


class Orbwalk:
    def __init__(self, process, base_address):
        self.can_attack_time = 0
        self.can_move_time = 0
        self.process = process
        self.base_address = base_address

    def getGameTime(self):
        return r_float(self.process, self.base_address + Offsets.oGameTime)
    
    @staticmethod
    def getAttackTime():
        stats = loads(urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read())
        return 1. / stats["championStats"]["attackSpeed"]

    @staticmethod
    def getWindupTime(attack_speed_base, windup, windup_mod):
        attack_time = Orbwalk.getAttackTime()
        if windup_mod == 0.:
            return (1. / attack_speed_base) * windup + ((attack_time * windup) - (1. / attack_speed_base) * windup) * (1. + windup_mod) 
        return (1. / attack_speed_base) * windup + ((attack_time * windup) - (1. / attack_speed_base) * windup) * windup_mod

    def walk(self, pos, attack_key, attack_speed_base, windup, windup_mod):
        game_time = self.getGameTime()
        if self.can_attack_time < game_time and pos:
            mouse_pos = GetCursorPos()
            windll.user32.SetCursorPos(int(pos[0]),int(pos[1]))
            send(attack_key)
            sleep(0.01)
            windll.user32.SetCursorPos(int(mouse_pos[0]), int(mouse_pos[1]))
            self.can_attack_time = game_time + Orbwalk.getAttackTime()
            self.can_move_time = game_time + Orbwalk.getWindupTime(attack_speed_base, windup, windup_mod)
        elif self.can_move_time < game_time:
            sleep(0.03)
            right_click()

    def walk_inplace(self, pos, attack_key, attack_speed_base, windup, windup_mod):
        game_time = self.getGameTime()
        if self.can_attack_time < game_time and pos:
            send(attack_key)
            self.can_attack_time = game_time + Orbwalk.getAttackTime()
            self.can_move_time = game_time + Orbwalk.getWindupTime(attack_speed_base, windup, windup_mod)
        elif self.can_move_time < game_time:
            sleep(0.03)
            right_click()

    @staticmethod
    def walk_kalista(pos, attack_key, *_):
        if pos:
            mouse_pos = GetCursorPos()
            windll.user32.SetCursorPos(int(pos[0]),int(pos[1]))
            send(attack_key)
            sleep(0.01)
            windll.user32.SetCursorPos(int(mouse_pos[0]), int(mouse_pos[1]))
            sleep(0.01)
            right_click()
            sleep(0.02)
        elif not pos:
            right_click()
            sleep(0.03)