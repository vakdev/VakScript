#built-in
from ctypes import windll
from collections import namedtuple
from gc import collect as del_mem
from time import sleep

#ext
from pyMeow import open_process, get_module
from pyMeow import r_int, r_float, r_uint64
from win32api import GetSystemMetrics, GetCursorPos


#own
from data import Offsets, Info, VK_CODES
from world_to_screen import World
from utils import send_key, debug_info
from entities import AttributesReader

"""
TODO:
    - Fix Username API Request or read in memory instead.

"""

class Asmite:

    def __init__(self, settings):
        self.settings = settings

        self.obj_health = Offsets.obj_health
        self.obj_spawn_count = Offsets.obj_spawn_count
        self.obj_x = Offsets.obj_x
        self.obj_y = Offsets.obj_y
        self.obj_z = Offsets.obj_z
    
    def get_settings(self):
        return VK_CODES[self.settings['smite']]
            
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
    while not terminate.value:
        if on_window.value:
            del_mem()
            try:
                process = open_process(process=Info.game_name_executable)
                base_address = get_module(process, Info.game_name_executable)['base']
                local_player = r_uint64(process, base_address + Offsets.local_player)
                attr_reader = AttributesReader(process, base_address)
                asmite = Asmite(settings)
                smite_key = asmite.get_settings()

                damage = 0
                smite_charges = 0

                width, height = GetSystemMetrics(0), GetSystemMetrics(1)
                world = World(process, base_address, width, height)
                set_cursor_pos = windll.user32.SetCursorPos
                nt = namedtuple('Attributes', 'health alive x y z')

            except Exception as asmite_proc_loop:
                debug_info(asmite_proc_loop, True)
                sleep(0.1)
                
            else:
                try:
                    while 1 and on_window.value:
                        player = attr_reader.read_player(local_player)

                        for buff in player.buffs:
                            if 'smitedamagetracker' in str(buff.name).lower():
                                damage = buff.count2

                        entities = [asmite._read_attr(process, pointer, nt) for pointer in jungle_pointers]
                        target = [entity for entity in entities if entity.health <= damage and entity.alive]
                        
                        spells = attr_reader.read_spells(local_player)
                        if 'smite' in spells[4]['name'].lower():
                            smite_charges = spells[4]['charges']
                        elif 'smite' in spells[5]['name'].lower():
                            smite_charges = spells[5]['charges']

                        if target and smite_charges > 0:
                            pos = world.world_to_screen(world.get_view_proj_matrix(), target[0].x, target[0].z, target[0].y)
                            mouse_pos = GetCursorPos()
                            if pos:
                                set_cursor_pos(pos[0], pos[1])
                                send_key(smite_key)
                                sleep(0.01)
                                set_cursor_pos(mouse_pos[0], mouse_pos[1])

                        sleep(0.03)
                except Exception as asmite_loop:
                    debug_info(asmite_loop, True)
                    sleep(0.1)


