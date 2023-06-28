def spaceglider(terminate, settings, champion_pointers, minion_pointers, on_window):
    #verified context and no warnings.
    import requests
    import ssl
    requests.packages.urllib3.disable_warnings()
    ssl._create_default_https_context = ssl._create_unverified_context
    
    #ext
    from pyMeow import open_process, get_module
    from pyMeow import r_uint64, r_string
    from win32api import GetSystemMetrics, GetAsyncKeyState, mouse_event
    from win32con import MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
    from time import sleep
    from mouse import right_click
    from gc import collect as del_mem

    #own
    from data import Data, Offsets, VK_CODES
    from stats import Stats
    from orbwalk import Orbwalk
    from world_to_screen import World
    from entities import Entity, ReadAttributes
    from utils import press_key, release_key

    #keyboard, mouse funcions (kp=key press, kr= key release, mp= mouse press, mr = mouse release)
    def ppc(_):pass
    def kp_mp_function(range_key): press_key(range_key), mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
    def kr_mr_function(range_key): release_key(range_key), mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
    def kp_function(range_key): press_key(range_key)
    def mr_function(_): mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

    while not terminate.value:
        if on_window.value:
            del_mem()
            try:
                process = open_process(process=Data.game_name_executable)
                base_address = get_module(process, Data.game_name_executable)['base']
                local = r_uint64(process, base_address + Offsets.local_player)
                local_name = r_string(process, local + Offsets.obj_name)
                stats = Stats()
                entity = Entity(stats)
                attr = ReadAttributes(process, base_address)
                orbwalk = Orbwalk(process, base_address)
                width, height = GetSystemMetrics(0), GetSystemMetrics(1)
                world = World(process, base_address, width, height)

                #player stats
                attack_speed_base = stats.get_attack_speed_base(local_name)
                windup, windup_mod = stats.get_windup(local_name)

                #settings
                orbwalk_key = VK_CODES[settings['orbwalk']]
                laneclear_key = VK_CODES[settings['laneclear']]
                lasthit_key = VK_CODES[settings['lasthit']]
                attack_key = settings['attack']
                range_key = VK_CODES[settings['range']]
                kiting_mode = settings['kiting_mode']
                target_prio = settings['orbwalk_prio']
                mode_lasthit = settings['lasthit_mode']
                potato_pc = settings['ppc']

                #
                target_prio_mode = {'Less Basic Attacks':entity.select_by_health,
                                    'Most Damage':entity.select_by_damage,
                                    'Nearest Enemy':entity.select_by_distance}
                walk_mode = {'kalista': orbwalk.walk_kalista}
                select_target = target_prio_mode.get(target_prio, entity.select_by_health)
                walk = walk_mode.get(local_name, orbwalk.walk)
                walk_min = orbwalk.walk
                kp_mp, kr_mr, kp, mr = kp_mp_function, kr_mr_function, kp_function, mr_function
                
                if potato_pc:
                    kp_mp = kr_mr = kp = mr = ppc
                if kiting_mode == 'In-place':
                    walk = orbwalk.walk_inplace

                #method vars
                read_player = attr.read_player
                read_enemy = attr.read_enemy
                read_minion = attr.read_minion
                world_to_screen = world.world_to_screen
                get_view_proj_matrix = world.get_view_proj_matrix
                select_lasthit_minion = entity.select_lasthit_minion
                select_lowest_minion = entity.select_lowest_minion

                def manual_mode():
                    while 1:
                        sleep(0.0001)
                        if GetAsyncKeyState(orbwalk_key):
                            kp_mp(range_key)
                            targets = (read_enemy(pointer) for pointer in champion_pointers)
                            target = select_target(read_player(local), targets)
                            if target:
                                pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                                walk(pos, attack_key, attack_speed_base, windup, windup_mod)
                                continue
                            right_click()
                            sleep(0.03)
                            continue

                        elif GetAsyncKeyState(lasthit_key):
                            kp_mp(range_key)
                            targets = (read_minion(pointer) for pointer in minion_pointers)
                            target = select_lasthit_minion(read_player(local), targets)
                            if target:
                                mr(0)
                                pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                                walk_min(pos, attack_key, attack_speed_base, windup, windup_mod)
                                continue
                            right_click()
                            sleep(0.03)
                            continue

                        elif GetAsyncKeyState(laneclear_key):
                            kp(range_key)
                            targets = (read_minion(pointer) for pointer in minion_pointers)
                            target = select_lowest_minion(read_player(local), targets)
                            if target:
                                pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                                walk(pos, attack_key, attack_speed_base, windup, windup_mod)
                                continue
                            right_click()
                            sleep(0.03)
                            continue
                        
                        orbwalk.can_attack_time = 0
                        kr_mr(range_key)

                        if not on_window.value:
                            break

                def auto_mode():
                    while 1:
                        sleep(0.0001)
                        targets = (read_enemy(pointer) for pointer in champion_pointers)
                        target = select_target(read_player(local), targets)
                        if GetAsyncKeyState(orbwalk_key) and target:
                            kp_mp(range_key)
                            pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                            walk(pos, attack_key, attack_speed_base, windup, windup_mod)
                            continue
                        
                        elif GetAsyncKeyState(orbwalk_key) and not target:
                            kp_mp(range_key)
                            targets = (read_minion(pointer) for pointer in minion_pointers)
                            target = select_lasthit_minion(read_player(local), targets)
                            if target:
                                mr(0)
                                pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                                walk_min(pos, attack_key, attack_speed_base, windup, windup_mod)
                                continue
                            right_click()
                            sleep(0.03)
                            continue
                        
                        elif GetAsyncKeyState(laneclear_key):
                            kp(range_key)
                            targets = (read_minion(pointer) for pointer in minion_pointers)
                            target = select_lowest_minion(read_player(local), targets)
                            if target:
                                pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
                                walk(pos, attack_key, attack_speed_base, windup, windup_mod)
                                continue
                            right_click()
                            sleep(0.03)
                            continue

                        orbwalk.can_attack_time = 0
                        kr_mr(range_key)

                        if not on_window.value:
                            break
                    
                callFunc = {'Manual': manual_mode, 'Auto': auto_mode}
                try:
                    callFunc.get(mode_lasthit, auto_mode)()
                except:
                    kr_mr_function(range_key)

            except:
                sleep(.1)
        sleep(.1)
