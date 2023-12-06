#built-in
from time import sleep
from gc import collect as del_mem

#ext
from pyMeow import open_process, get_module, r_uint64, r_string
from win32api import GetSystemMetrics, GetAsyncKeyState, mouse_event
from win32con import MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
from mouse import right_click

#own
from data import Info, Offsets, VK_CODES
from stats import Stats
from orbwalker import Orbwalk
from world_to_screen import World
from entities import TargetSelector, AttributesReader
from utils import press_key, release_key, debug_info

"""
TODO:
    - Tests with entities.py and orbwalker.py changes.
"""


def spaceglider(terminate, settings, champion_pointers, minion_pointers, on_window):
    """ Auto kite process."""

    import ssl
    import requests

    requests.packages.urllib3.disable_warnings()
    ssl._create_default_https_context = ssl._create_unverified_context

    # Keyboard - mouse functions.
    # kp= key pres, kr= key release, mp= mouse press, mr= mouse release
    def ppc(_):pass
    def kp_mp_function(range_key): press_key(range_key), mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
    def kr_mr_function(range_key): release_key(range_key), mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
    def kp_function(range_key): press_key(range_key)
    def mp_function(_): mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
    def mr_function(_): mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

    while not terminate.value:
        if on_window.value:
            del_mem()
            try:
                process = open_process(process=Info.game_name_executable)
                base_address = get_module(process, Info.game_name_executable)['base']
                local_player = r_uint64(process, base_address + Offsets.local_player)
                local_player_name = r_string(process, local_player + Offsets.obj_name)
                stats = Stats()
                target_selector = TargetSelector(stats=stats)
                attr_reader = AttributesReader(process, base_address)
                orbwalk = Orbwalk(process, base_address)

                screen_width = GetSystemMetrics(0)
                screen_height = GetSystemMetrics(1)

                world = World(process, base_address, screen_width, screen_height)
                world_to_screen = world.world_to_screen
                get_view_proj_matrix = world.get_view_proj_matrix

                base_attack_speed = stats.get_attack_speed(local_player_name)
                windup, windup_mod = stats.get_windup(local_player_name)

                orbwalk_key = VK_CODES[settings['orbwalk']]
                laneclear_key = VK_CODES[settings['laneclear']]
                lasthit_key = VK_CODES[settings['lasthit']]
                attack_key = VK_CODES[settings['attack']]
                range_key = VK_CODES[settings['range']]
                kiting_mode = settings['kiting_mode']
                target_prio = settings['orbwalk_prio']
                mode_lasthit = settings['lasthit_mode']
                press_range = settings['press_range']
                potato_pc = settings['ppc']

                target_prio_modes = {
                    'Less Basic Attacks' : target_selector.select_by_health,
                    'Most Damage' : target_selector.select_by_damage,
                    'Nearest Enemy' : target_selector.select_by_distance
                }
                
                select_target = target_prio_modes.get(target_prio, target_selector.select_by_health)
                select_minion_target = target_selector.select_by_health
                select_minion_lasthit = target_selector.select_by_lasthit

                walk_modes = {
                    'Normal' : orbwalk.walk,
                    'Normal v2' : orbwalk.walk_v2,
                    'In-place' : orbwalk.walk_inplace,
                    'Kalista' : orbwalk.walk_kalista
                }

                walk = walk_modes.get(local_player_name, walk_modes[kiting_mode])
                walk_min = orbwalk.walk

                # Script will press all keys it needs.
                kp_mp, kr_mr, kp, mr = kp_mp_function, kr_mr_function, kp_function, mr_function

                if not press_range:
                    # Script wont press ShowAdvancedPlayerStats key.
                    kp_mp, kr_mr, kp = mp_function, mr_function, ppc

                if potato_pc:
                    # Script wont press any key.
                    kp_mp = kr_mr = kp = mr = ppc
                
            except Exception as spaceglider_proc_loop:
                debug_info(spaceglider_proc_loop, True)

            else:
                try:
                    while 1:
                        if GetAsyncKeyState(orbwalk_key):
                            kp_mp(range_key)
                            entities = [attr_reader.read_enemy(pointer) for pointer in champion_pointers]
                            target = select_target(attr_reader.read_player(local_player), entities)
                            if target:
                                pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                                walk(pos, attack_key, base_attack_speed, windup, windup_mod)
                            else:
                                sleep(0.1)
                                right_click()
                            
                            continue
                        
                        elif GetAsyncKeyState(lasthit_key):
                            kp_mp(range_key)
                            entities = [attr_reader.read_minion(pointer) for pointer in minion_pointers]
                            target = select_minion_lasthit(attr_reader.read_player(local_player), entities)
                            if target:
                                mr(0)
                                pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                                walk_min(pos, attack_key, base_attack_speed, windup, windup_mod)
                            else:
                                right_click()
                                sleep(0.1)
                            
                            continue
                        
                        elif GetAsyncKeyState(laneclear_key):
                            kp(range_key)
                            entities = [attr_reader.read_minion(pointer) for pointer in minion_pointers]
                            target = select_minion_target(attr_reader.read_player(local_player), entities)
                            if target:
                                pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                                walk_min(pos, attack_key, base_attack_speed, windup, windup_mod)
                            else:
                                right_click()
                                sleep(0.1)
                            
                            continue
                        
                        orbwalk.can_attack_time = 0
                        kr_mr(range_key)

                        if not on_window.value:
                            break

                        sleep(0.1)
                
                except Exception as spaceglider_loop:
                    debug_info(spaceglider_loop, True)
                    kr_mr_function(range_key)

