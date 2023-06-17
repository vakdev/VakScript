#TODO: GET LIMIT FPS to avoid black screen
#TODO: Fix Limit track
#TODO: Add gold tracker

def drawings(terminate, settings, champion_pointers, on_window):
    #verified context and no warnings.
    import requests
    import ssl
    requests.packages.urllib3.disable_warnings()
    ssl._create_default_https_context = ssl._create_unverified_context
    
    #ext
    from pyMeow import open_process, get_module, get_color, load_font, get_monitor_refresh_rate
    from pyMeow import overlay_init, overlay_loop, overlay_close, begin_drawing, end_drawing
    from pyMeow import draw_line, draw_circle, draw_font, gui_progress_bar, gui_text_box
    from pyMeow import r_uint64
    from win32api import GetSystemMetrics
    from gc import collect as del_mem
    from time import sleep

    #own
    from data import Data, Offsets
    from entities import EntityDrawings, ReadAttributes, distance
    from world_to_screen import World
    from settings import jsonGetter

    yellow = get_color('yellow')
    red = get_color('red')
    cyan = get_color('cyan')
    gold = get_color('gold')

    def draw_enemy_line(entity, own_pos, width, height):
        if entity.alive and entity.targetable and entity.visible:
            pos = world_to_screen(get_view_proj_matrix(), entity.x, entity.z, entity.y)
            if pos:
                x, y = pos[0], pos[1]
                if (x < 0 or x > width or y < 0 or y > height) and distance(player, entity) <= 3000:
                        draw_line(own_pos[0], own_pos[1], x, y, red, 1.)
                else:
                    draw_line(own_pos[0], own_pos[1], x, y, cyan, 1.)
                    draw_circle(x, y, 5, cyan)

    while not terminate.value:
        if on_window.value:
            del_mem()
            try:
                process = open_process(process=Data.game_name_executable)
                base_address = get_module(process, Data.game_name_executable)['base']
                local = r_uint64(process, base_address + Offsets.local_player)
                attr = ReadAttributes(process, base_address)

                width = GetSystemMetrics(0)
                height = GetSystemMetrics(1)
                world = World(process, base_address, width, height)
                entity = EntityDrawings(process, base_address, width, height)

                #if is_active_window():
                can_track = settings['position_tracker']
                can_focus = settings['show_focused']
                can_healths = settings['show_healths']
                can_track_spells = settings['spell_tracker']
                limited_draw = settings['screen_track']
                target_prio = jsonGetter().get_data('orbwalk_prio')
                potato_pc = jsonGetter().get_data('ppc')

                target_prio_mode = {'Less Basic Attacks':entity.select_by_health,
                                    'Most Damage':entity.select_by_damage,
                                    'Nearest Enemy':entity.select_by_distance}

                select_target = target_prio_mode.get(target_prio, entity.select_by_health)
                read_player = attr.read_player
                read_enemy = attr.read_enemy
                read_spells = attr.read_spells
                world_to_screen = world.world_to_screen
                world_to_screen_limited = world.world_to_screen_limited
                get_view_proj_matrix = world.get_view_proj_matrix


                fps = 60
                if potato_pc:
                    fps = 30
                if limited_draw:
                    world_to_screen = world.world_to_screen_limited

            except:
                print('Error on drawings.py')
                continue
        
            else:
                overlay_init(fps=fps)
                load_font(Data.font_file_name, 1)
                spells_keys = attr.spells_keys
                while overlay_loop():
                    try:
                        begin_drawing()

                        entities = [read_enemy(pointer) for pointer in champion_pointers]
                        player = read_player(local)
                        own_pos = world_to_screen_limited(get_view_proj_matrix(), player.x, player.z, player.y)
                        if own_pos:
                            draw_circle(own_pos[0], own_pos[1], 5, gold)

                        if not on_window.value:
                            overlay_close()
                            break

                        if can_track:
                            own_pos = world_to_screen(get_view_proj_matrix(), player.x, player.z, player.y)
                            for entity in entities:
                                draw_enemy_line(entity, own_pos, width, height)

                        if can_focus:
                            target = select_target(player, entities)
                            if target:
                                pos = world_to_screen_limited(get_view_proj_matrix(), target.x, target.z, target.y)
                                if pos and own_pos:
                                    draw_circle(pos[0], pos[1], 8, gold)

                        if can_healths:
                            ypos = height
                            for entity in entities:
                                ypos -= 30
                                draw_font(1, entity.name, 5, ypos, 15, 2, yellow)
                                gui_progress_bar(100, ypos, 100, 15, "", "", entity.health, 0, entity.max_health)
                                
                        if can_track_spells:
                            spells = [read_spells(pointer) for pointer in champion_pointers]
                            ypos = height
                            for i, entity in enumerate(entities):
                                ypos -= 30
                                pos = world_to_screen_limited(get_view_proj_matrix(), entity.x, entity.z, entity.y)

                                if pos:
                                    x_space = 0
                                    for slot in spells_keys[:-2]:
                                        gui_text_box(pos[0] - 60 + x_space, pos[1] - 125, 35, 25, '', 1)
                                        draw_font(1, str(spells[i][slot][1]), pos[0] - 50 + x_space, pos[1] - 120, 18, 0, yellow)
                                        draw_font(1, str(spells[i][slot][0]), pos[0] - 50 + x_space, pos[1] - 95, 15, 0, cyan)
                                        x_space += 35
                                    x_space = 100
                                    if can_healths:
                                        x_space = 210

                                    for slot in spells_keys[-2:]:
                                        if not can_healths:
                                            draw_font(1, entity.name, 5, ypos, 15, 2, yellow)
                                        gui_text_box(x_space, ypos-5, 35, 25, '', 1)
                                        draw_font(1, str(spells[i][slot][1]), x_space + 3, ypos, 15, 2, yellow)
                                        x_space += 40
                            # print(f"drawings time: {(end_time - start_time)*1000:.2f} ms")
                            
                            # type in-game chat cooldowns: R, D, F.

                            # if GetAsyncKeyState(0x53):
                            #     cooldowns_list = []
                            #     for i, entity in enumerate(entities):
                            #         champion_name = entity.name.upper()
                            #         skills_cooldowns = []
                            #         for slot in ['R', 'D', 'F']:
                            #             cooldown = spells[i][slot][1]
                            #             skills_cooldowns.append(f"{slot}[ {str(cooldown).center(3)} ]")
                            #         champion_cooldowns = ', '.join(skills_cooldowns)
                            #         cooldowns_list.append(f"{champion_name} = {champion_cooldowns}")
                            #     for cooldown_text in cooldowns_list:
                            #         keyboard.send('enter')
                            #         sleep(0.1)
                            #         keyboard.write(cooldown_text)
                            #         sleep(0.1)
                            #         keyboard.send('enter')
                            #         sleep(0.1)

                        end_drawing()
                    except:
                        overlay_close()
        sleep(.1)
