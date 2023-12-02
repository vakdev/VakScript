#built-in
from ctypes import windll
from urllib.request import urlopen
from urllib.parse import quote
from collections import namedtuple
from gc import collect as del_mem
from time import sleep

#ext
from pyMeow import open_process, get_module
from pyMeow import r_int, r_float
from orjson import loads
from win32api import GetSystemMetrics, GetAsyncKeyState


#own
from data import Offsets, Info, VK_CODES
from world_to_screen import World
from utils import send_key, debug_info

"""
TODO:
    - Fix Username API Request or read in memory instead.

"""

class Asmite:

    def __init__(self, settings):
        self.settings = settings
        self.raw_names = Info.asmite_raw_names
        self.url_active_player_name = Info.url_activeplayer_name
        self.url_request = Info.asmite_url_request

        self.obj_health = Offsets.obj_health
        self.obj_spawn_count = Offsets.obj_spawn_count
        self.obj_x = Offsets.obj_x
        self.obj_y = Offsets.obj_y
        self.obj_z = Offsets.obj_z

    def get_username(self):
        return loads(urlopen(self.url_active_player_name).read())
    
    def get_settings(self):
        return VK_CODES[self.settings['smite']], VK_CODES[self.settings['update']]
    
    def get_damage(self, username):
        spells = loads(urlopen(self.url_request.format(username=username)).read())
        sp1, sp2 = spells["summonerSpellOne"], spells["summonerSpellTwo"]
        for v, v2 in zip(sp1.values(), sp2.values()):
            if v in self.raw_names:
                return self.raw_names[v]
            if v2 in self.raw_names:
                return self.raw_names[v2]
            
    def _read_attr(self, process, address, nt):
        attributes = nt(
            health  = r_float(process, address + self.obj_health),
            alive   = r_int(process, address + self.obj_spawn_count) % 2 == 0,
            x       = r_float(process, address + self.obj_x),
            y       = r_float(process, address + self.obj_y),
            z       = r_float(process, address + self.obj_z)
        )

        return attributes

def autosmite(terminate, settings, jungle_pointers, on_window):
    import ssl
    import requests

    requests.packages.urllib3.disable_warnings()
    ssl._create_default_https_context = ssl._create_unverified_context

    while not terminate.value:
        if on_window.value:
            del_mem()
            try:
                process = open_process(process=Info.game_name_executable)
                base_address = get_module(process, Info.game_name_executable)['base']
                asmite = Asmite(settings)
                username = quote(asmite.get_username())
                smite_key, update_key = asmite.get_settings()
                damage = asmite.get_damage(username)
                width, height = GetSystemMetrics(0), GetSystemMetrics(1)
                world = World(process, base_address, width, height)
                set_cursor_pos = windll.user32.SetCursorPos
                nt = namedtuple('Attributes', 'health alive x y z')

            except Exception as asmite_proc_loop:
                debug_info(asmite_proc_loop, True)
                sleep(0.1)
                
            else:
                try:
                    while 1:
                        entities = [asmite._read_attr(process, pointer, nt) for pointer in jungle_pointers]
                        target = [entity for entity in entities if entity.health <= damage and entity.alive]

                        if target:
                            pos = world.world_to_screen(world.get_view_proj_matrix(), target[0].x, target[0].z, target[0].y)
                            if pos:
                                set_cursor_pos(pos[0], pos[1])
                                send_key(smite_key)
                                sleep(0.03)

                        elif GetAsyncKeyState(update_key):
                            damage = asmite.get_damage(username)
                except Exception as asmite_loop:
                    debug_info(asmite_loop, True)
                    sleep(0.1)

