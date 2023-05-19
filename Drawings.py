def drawings(terminate):
    #verified context
    import requests
    import ssl
    requests.packages.urllib3.disable_warnings()
    ssl._create_default_https_context = ssl._create_unverified_context
    
    #ext
    from pyMeow import open_process, get_module, get_color
    from pyMeow import overlay_init, overlay_loop, overlay_close, begin_drawing, end_drawing
    from pyMeow import draw_line, draw_circle, draw_text, gui_progress_bar
    from pyMeow import r_uint64, r_int
    from time import sleep
    from win32api import GetSystemMetrics
    from json import load
    from gc import collect as del_mem

    #own
    from Data import Data, Offsets
    from Stats import Stats
    from Entities import EntityDrawings, ReadAttributes, Entity
    from Manager import ReadManager
    from Utils import isActiveWindow
    from WorldToScreen import World

    #

    violet = get_color('violet')
    orange = get_color('orange')
    yellow = get_color('yellow')
    red = get_color('red')

    def draw_enemy_line(target):
        if target.alive and target.targetable and target.visible:
            pos = world_to_screen(get_view_proj_matrix(), target.x, target.z, target.y)
            if pos and own_pos:
                if (pos[0] < 0 or pos[0] > width or pos[1] < 0 or pos[1] > height) and Entity._distance(player, target) <= 3000:
                        draw_line(own_pos[0], own_pos[1], pos[0], pos[1], red, 1.)
                else:
                    draw_line(own_pos[0], own_pos[1], pos[0], pos[1], violet, 1.)

    while not terminate.value:
        del_mem()
        try:
            if isActiveWindow():
                process = open_process(process=Data.game_name_executable)
                base_address = get_module(process, Data.game_name_executable)['base']
                local = r_uint64(process, base_address + Offsets.oLocalPlayer)
                local_team = r_int(process, local + Offsets.objTeam)
                stats = Stats()
                manager = ReadManager(process, base_address)
                attr = ReadAttributes(process)
                champion_pointers = manager.getChampionPointers(stats.names, local_team)
                width = GetSystemMetrics(0)
                height = GetSystemMetrics(1)
                world = World(process, base_address, width, height)
                entity = EntityDrawings(process, base_address, width, height)
                with open(Data.settings_file_name, 'r+') as json_file:
                    opt = load(json_file)
                    can_draw = opt['AutoKite']['Settings']['ext_drawings']
                    can_track = opt['AutoKite']['Settings']['ext_track']
                    can_focus = opt['AutoKite']['Settings']['ext_focus']
                    can_healths = opt['AutoKite']['Settings']['ext_healths']
                    limited_draw = opt['AutoKite']['Settings']['ext_limited']
                    target_prio = opt['AutoKite']['Modes']['orbwalk']
                    potato_pc = opt['AutoKite']['Settings']['ppc']

            else:
                sleep(0.1) 
                continue

            target_prio_mode = {'Less Basic Attacks':entity.select_by_health,
                                'Most Damage':entity.select_by_damage,
                                'Nearest Enemy':entity.select_by_distance}
            select_target = target_prio_mode.get(target_prio, entity.select_by_health)
            read_player = attr.read_player
            read_enemy = attr.read_enemy
            world_to_screen = world.world_to_screen
            get_view_proj_matrix = world.get_view_proj_matrix
            fps = 60
            if limited_draw:
                world_to_screen = world.world_to_screen_restricted
            if potato_pc:
                fps = 30

        except:
            continue
        
        else:
            if can_draw:
                overlay_init(fps=fps)
                while overlay_loop():
                    try:
                        targets = [read_enemy(pointer) for pointer in champion_pointers]
                        player = read_player(local)
                        target = None
                        begin_drawing()

                        if not isActiveWindow():
                            overlay_close()
                            break

                        if can_focus:
                            target = select_target(player, targets)
                            if target:
                                pos = world.world_to_screen_restricted(get_view_proj_matrix(), target.x, target.z, target.y)
                                own_pos = world.world_to_screen_restricted(get_view_proj_matrix(), player.x, player.z, player.y)
                                if pos and own_pos:
                                    draw_circle(own_pos[0], own_pos[1], 5., orange)
                                    draw_line(own_pos[0], own_pos[1], pos[0], pos[1], orange, 5.) 
                                    draw_circle(pos[0], pos[1], 6, orange)

                        if can_track:
                            own_pos = world_to_screen(get_view_proj_matrix(), player.x, player.z, player.y)
                            for entity in targets:
                                if entity is not target:
                                    draw_enemy_line(entity)

                        if can_healths:
                            ypos = height
                            for entity in targets:
                                ypos -= 30
                                draw_text(entity.name, 5, ypos, 15, yellow)
                                gui_progress_bar(100, ypos, 100, 15, ":", "HP", entity.health, 0, entity.max_health)

                        end_drawing()
                    except:
                        overlay_close()
            else:
                sleep(2)