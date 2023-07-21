"""
Modifications in pyMeow source for its use in VakScript:

v13.14 - game / script version.

- Removed MSAA_4X from overlayInit().

- Instead of using overlayLoop, added clearBackground to clear drawings directly. (vakClearBackground) . code:

# proc vakClearBackground {.exportpy: "vak_clear_background".} = 
#   clearBackground(Blank)

"""


#verified context and no warnings.
import requests
import ssl
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

#ext
from pyMeow import open_process, get_module, load_font, new_color
from pyMeow import overlay_init, overlay_close, begin_drawing, end_drawing, vak_clear_background
from pyMeow import draw_line, draw_circle, draw_font, gui_progress_bar, gui_text_box
from pyMeow import r_uint64
from win32api import GetSystemMetrics
from gc import collect as del_mem
from time import sleep
from math import cos, sin, pi

#own
from data import Data, Offsets
from entities import EntityDrawings, ReadAttributes, distance
from world_to_screen import World
from settings import jsonGetter
from utils import safe_title

class Colors:
    Lightgray = new_color(200, 200, 200, 255)
    Gray = new_color(130, 130, 130, 255)
    Darkgray = new_color(80, 80, 80, 255)
    Yellow = new_color(253, 249, 0, 255)
    Gold = new_color(255, 203, 0, 255)
    Orange = new_color(255, 161, 0, 255)
    Pink = new_color(255, 109, 194, 255)
    Red = new_color(230, 41, 55, 255)
    Maroon = new_color(190, 33, 55, 255)
    Green = new_color(0, 228, 48, 255)
    Lime = new_color(0, 158, 47, 255)
    Darkgreen = new_color(0, 117, 44, 255)
    Skyblue = new_color(102, 191, 255, 255)
    Blue = new_color(0, 121, 241, 255)
    Darkblue = new_color(0, 82, 172, 255)
    Purple = new_color(200, 122, 255, 255)
    Violet = new_color(135, 60, 190, 255)
    Darkpurple = new_color(112, 31, 126, 255)
    Beige = new_color(211, 176, 131, 255)
    Brown = new_color(127, 106, 79, 255)
    Darkbrown = new_color(76, 63, 47, 255)
    White = new_color(255, 255, 255, 255)
    Cyan = new_color(0, 255, 167, 255)
    Black = new_color(0, 0, 0, 255)
    Blank = new_color(0, 0, 0, 0)
    Magenta = new_color(255, 0, 255, 255)
    Raywhite = new_color(245, 245, 245, 255)

def drawings(terminate, settings, champion_pointers, turret_pointers, on_window):

    def draw_enemy_line(own_pos, pos, width, height):
        x, y = pos[0], pos[1]
        if (x < 0 or x > width or y < 0 or y > height) and distance(player, entity) <= 3000:
                draw_line(own_pos[0], own_pos[1], x, y, Colors.Red, 2.)
        else:
            draw_line(own_pos[0], own_pos[1], x, y, Colors.Lime, 2.)
            draw_circle(x, y, 5, Colors.Lime)

    def draw_health(entity, own_pos, pos, width, height):
        if not (0 <= pos[0] < width and 0 <= pos[1] < height):
            dx = pos[0] - own_pos[0]
            dy = pos[1] - own_pos[1]

            dx_inv = 1.0 / dx if dx != 0 else float('inf')
            dy_inv = 1.0 / dy if dy != 0 else float('inf')

            t_left = -(own_pos[0] - 30) * dx_inv
            t_right = (width - own_pos[0] - 130) * dx_inv
            t_top = -(own_pos[1] - 30) * dy_inv
            t_bottom = (height - own_pos[1] - 30) * dy_inv

            valid_t_values = [t for t in [t_left, t_right, t_top, t_bottom] if t >= 0]

            if valid_t_values:
                t_min = min(valid_t_values)
                x_intersect = own_pos[0] + t_min * dx
                y_intersect = own_pos[1] + t_min * dy
                draw_font(1, entity.name, x_intersect, y_intersect - 20, 20, 2, Colors.Gold)
                gui_progress_bar(x_intersect, y_intersect, 100, 15, "", "", entity.health, 0, entity.max_health)

    #for draw_range
    num_vert = 24
    angle_increment = 2 * pi / num_vert
    cos_values = [cos(i * angle_increment) for i in range(num_vert)]
    sin_values = [sin(i * angle_increment) for i in range(num_vert)]
            
    def draw_range(view_proj_matrix, game_pos, radius, thickness, color):
        for i in range(num_vert):
            vec1 = world_to_screen(
                view_proj_matrix, game_pos[0] + cos_values[i] * radius, game_pos[1], game_pos[2] + sin_values[i] * radius
            )
            next_index = (i + 1) % num_vert
            vec2 = world_to_screen(
                view_proj_matrix, game_pos[0] + cos_values[next_index] * radius, game_pos[1], game_pos[2] + sin_values[next_index] * radius
            )

            draw_line(vec1[0], vec1[1], vec2[0], vec2[1], color, thickness)

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
                min_attacks = entity.min_attacks

                #if is_active_window():
                show_position = settings['show_position']
                show_focused = settings['show_focused']
                show_healths = settings['show_healths']
                #show_gold = settings['show_gold']
                show_spells = settings['show_spells']
                show_player_range = settings['show_player_range']
                show_enemy_range = settings['show_enemy_range']
                show_turret_range = settings['show_turret_range']
                show_hits = settings['show_hits']
                screen_track = settings['screen_track']
                fps = settings['fps']

                #spells_keys = attr.spells_keys

                target_prio = jsonGetter().get_data('orbwalk_prio')

                target_prio_mode = {'Less Basic Attacks':entity.select_by_health,
                                    'Most Damage':entity.select_by_damage,
                                    'Nearest Enemy':entity.select_by_distance}

                select_target = target_prio_mode.get(target_prio, entity.select_by_health)

                read_player = attr.read_player
                read_enemy = attr.read_enemy
                read_turret = attr.read_turret
                read_spells = attr.read_spells
                world_to_screen = world.world_to_screen
                world_to_screen_limited = world.world_to_screen_limited
                get_view_proj_matrix = world.get_view_proj_matrix


                if screen_track:
                    world_to_screen = world.world_to_screen_limited

            except:
                continue
        
            else:
                try:
                    if not fps.isdecimal():
                        fps = 0
                    overlay_init(title=safe_title(), fps=int(fps))
                    load_font(Data.font_file_name, 1)
                
                    while 1:
                        begin_drawing()

                        entities = [read_enemy(pointer) for pointer in champion_pointers]
                        player = read_player(local)
                        view_proj_matrix = get_view_proj_matrix()
                        own_pos = world_to_screen(view_proj_matrix, player.x, player.z, player.y)

                        if show_player_range:
                            draw_range(view_proj_matrix, (player.x, player.z, player.y), player.attack_range + 65.0, 4, Colors.Gold)

                        if show_turret_range:
                            turrets = [read_turret(pointer) for pointer in turret_pointers]
                            for turret in turrets:
                                draw_range(view_proj_matrix, (turret.x, turret.z, turret.y), 890.0, 2, Colors.Red)

                        for entity in entities:
                            pos = world_to_screen(view_proj_matrix, entity.x, entity.z, entity.y)

                            if entity.alive and entity.visible:
                                if show_enemy_range:
                                    draw_range(view_proj_matrix, (entity.x, entity.z, entity.y), entity.attack_range + 65.0, 2, Colors.Cyan)
                                
                                if show_position and pos:
                                    draw_enemy_line(own_pos, pos, width, height)

                                if show_hits and pos:
                                    draw_font(1, str(round(min_attacks(player, entity))), pos[0], pos[1] + 50, 20, 2, Colors.Raywhite)
                                
                                if show_healths and pos:
                                    draw_health(entity, own_pos, pos, width, height)
                                
                                if show_spells and pos:
                                    spells_levels = read_spells(entity.pointer)
                                    x_space = 0
                                    for level in spells_levels:
                                        gui_text_box(pos[0] - 60 + x_space, pos[1] - 125, 35, 25, '', 1)
                                        draw_font(1, str(level), pos[0] - 50 + x_space, pos[1] - 120, 18, 0, Colors.Gold)
                                        x_space += 35

                            if show_focused:
                                target = select_target(player, entities)
                                if target:
                                    pos_limited = world_to_screen_limited(view_proj_matrix, target.x, target.z, target.y)
                                    if pos_limited:
                                        draw_line(own_pos[0], own_pos[1], pos_limited[0], pos_limited[1], Colors.Gold, 3)
                                        draw_circle(pos_limited[0], pos_limited[1], 8, Colors.Gold)
                                        draw_range(view_proj_matrix, (target.x, target.z, target.y), target.attack_range + 65.0, 3, Colors.Pink)

                        if not on_window.value:
                            overlay_close()
                            break

                        end_drawing()
                        vak_clear_background()
                except:
                    overlay_close()
        sleep(.1)