#built-in
from gc import collect as del_mem
from time import sleep
from math import cos, sin, pi

#ext
from pyMeow import open_process, get_module, load_font, new_color, load_texture, draw_texture
from pyMeow import overlay_init, overlay_loop, overlay_close, begin_drawing, end_drawing
from pyMeow import draw_line, draw_circle, draw_font, gui_progress_bar, gui_text_box
from pyMeow import r_uint64
from win32api import GetSystemMetrics

#own
from data import Info, Offsets
from entities import EntityConditions, TargetSelector, AttributesReader
from world_to_screen import World
from settings import jsonGetter
from utils import safe_title, debug_info

"""
TODO:
    - Lower ward tracker thikness.
    - Add draw_texture funtion to Draw class for future implements or imports.
    - Remove try-except in ward tracker. (name reading from entities/read_minion will be removed)
    - Fix black screen.
"""

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

class Draw:

    def __init__(self, world, width, height):
        self.width = width
        self.height = height
        self.world_to_screen = world.world_to_screen
        self.world_to_screen_limited = world.world_to_screen_limited

        #entity_range
        self.num_vert = 24 
        self.angle_increment = 2 * pi / self.num_vert
        self.cos_values = [cos(i * self.angle_increment) for i in range(self.num_vert)]
        self.sin_values = [sin(i * self.angle_increment) for i in range(self.num_vert)]

    @staticmethod
    def spell_level(pos, spell_levels):
        x_space = 0
        for level in spell_levels:
            gui_text_box(pos[0] - 60 + x_space, pos[1] - 125, 35, 25, '', 1)
            draw_font(1, str(level), pos[0] - 50 + x_space, pos[1] - 120, 18, 0, Colors.Gold)
            x_space += 35

    def entity_range(self, view_proj_matrix, game_pos, radius, thickness=1.0, color=Colors.Cyan):
        for i in range(self.num_vert):
            vec1 = self.world_to_screen(
                view_proj_matrix, game_pos[0] + self.cos_values[i] * radius, game_pos[1], game_pos[2] + self.sin_values[i] * radius
            )

            next_index = (i + 1) % self.num_vert

            vec2 = self.world_to_screen(
                view_proj_matrix, game_pos[0] + self.cos_values[next_index] * radius, game_pos[1], game_pos[2] + self.sin_values[next_index] * radius
            )

            draw_line(vec1[0], vec1[1], vec2[0], vec2[1], color, thickness)

    def health(self, entity, own_pos, pos):
        # Draw healthbars around the screen aiming to enemy position in world.

        if own_pos:
            if not (0 <= pos[0] < self.width and 0 <= pos[1] < self.height):
                dx = pos[0] - own_pos[0]
                dy = pos[1] - own_pos[1]

                dx_inv = 1.0 / dx if dx != 0 else float('inf')
                dy_inv = 1.0 / dy if dy != 0 else float('inf')

                t_left = -(own_pos[0] - 30) * dx_inv
                t_right = (self.width - own_pos[0] - 130) * dx_inv
                t_top = -(own_pos[1] - 30) * dy_inv
                t_bottom = (self.height - own_pos[1] - 30) * dy_inv

                valid_t_values = [t for t in [t_left, t_right, t_top, t_bottom] if t >= 0]

                if valid_t_values:
                    t_min = min(valid_t_values)
                    x_intersect = own_pos[0] + t_min * dx
                    y_intersect = own_pos[1] + t_min * dy
                    draw_font(1, entity.name, x_intersect, y_intersect - 20, 20, 2, Colors.Gold)
                    gui_progress_bar(x_intersect, y_intersect, 100, 15, "", "", entity.health, 0, entity.max_health)
        
    def line_to_enemy(self, own_pos, pos, thickness=1.0, color=Colors.Lime):
        draw_line(own_pos[0], own_pos[1], pos[0], pos[1], color, thickness)
        draw_circle(pos[0], pos[1], 5.0, color)


def drawings(terminate, settings, champion_pointers, ward_pointers, turret_pointers, on_window):
    """ External drawings process."""

    while not terminate.value:
        if on_window.value:
            del_mem()
            try:
                process = open_process(process=Info.game_name_executable)
                base_address = get_module(process, Info.game_name_executable)['base']
                local_player = r_uint64(process, base_address + Offsets.local_player)
                attr_reader = AttributesReader(process, base_address)

                screen_width = GetSystemMetrics(0)
                screen_height = GetSystemMetrics(1)

                world = World(process, base_address, screen_width, screen_height)
                draw = Draw(world, screen_width, screen_height)
                world_to_screen = world.world_to_screen
                world_to_screen_limited = world.world_to_screen_limited
                get_view_proj_matrix = world.get_view_proj_matrix
                

                target_selector = TargetSelector(world)

                show_position = settings['show_position']
                show_focused = settings['show_focused']
                show_healths = settings['show_healths']
                show_spells = settings['show_spells']
                show_player_range = settings['show_player_range']
                show_enemy_range = settings['show_enemy_range']
                show_turret_range = settings['show_turret_range']
                show_hits = settings['show_hits']
                vision_tracker = settings['vision_tracker']
                screen_track = settings['screen_track']
                fps = settings['fps']
                target_prio = jsonGetter().get_data('orbwalk_prio')
                
                target_prio_modes = {
                    'Less Basic Attacks' : target_selector.select_by_health,
                    'Most Damage' : target_selector.select_by_damage,
                    'Nearest Enemy' : target_selector.select_by_distance
                }

                select_target = target_prio_modes.get(target_prio, target_selector.select_by_health)

                if screen_track:
                    world_to_screen = world.world_to_screen_limited

            except Exception as drawings_proc_loop:
                debug_info(drawings_proc_loop, True)
            else:
                try:
                    if not fps.isdecimal() or fps == '0':
                        fps = 60
                    
                    overlay_init(title=safe_title(), fps=int(fps))
                    load_font(Info.font_file_name, 1)
                    wards_texture = {
                        'yellowtrinket': load_texture('wards/yellowtrinket.png'),
                        'sightward': load_texture('wards/sightward.png'),
                        'visionward': load_texture('wards/yellowtrinket.png'),
                        'bluetrinket': load_texture('wards/bluetrinket.png'),
                        'jammerdevice': load_texture('wards/pinkward.png'),
                        'perkszombieward': load_texture('wards/sightward.png')
                    }

                    while overlay_loop():
                        entities = [attr_reader.read_enemy(pointer) for pointer in champion_pointers]
                        wards = [attr_reader.read_minion(pointer) for pointer in ward_pointers]
                        player = attr_reader.read_player(local_player)
                        view_proj_matrix = get_view_proj_matrix()
                        own_pos = world_to_screen(view_proj_matrix, player.x, player.z, player.y)

                        begin_drawing()

                        if show_player_range:
                            draw.entity_range(view_proj_matrix, (player.x, player.z, player.y), player.attack_range + 65.0, color=Colors.Orange)

                        if show_turret_range:
                            turrets = [attr_reader.read_turret(pointer) for pointer in turret_pointers]
                            for turret in turrets:
                                if EntityConditions.hurtable(turret):
                                    draw.entity_range(view_proj_matrix, (turret.x, turret.z, turret.y), 890.0, 1.0, Colors.Red)

                        for entity in entities:
                            if EntityConditions.hurtable(entity):
                                pos = world_to_screen(view_proj_matrix, entity.x, entity.z, entity.y)
                                if pos:
                                    if show_enemy_range:
                                        draw.entity_range(view_proj_matrix, (entity.x, entity.z, entity.y), entity.attack_range + 65.0, color=Colors.Cyan)
                                    
                                    if show_position:
                                        draw.line_to_enemy(own_pos, pos, color=Colors.Gray)

                                    if show_hits:
                                        min_attacks = entity.health / EntityConditions.effective_damage(player.basic_attack + player.bonus_attack, entity.armor)
                                        draw_font(1, str(round(min_attacks)), pos[0], pos[1] + 50, 20, 2, Colors.Raywhite)

                                    if show_healths:
                                        draw.health(entity, own_pos, pos)
                                    
                                    # Removed, because of changes to read_spells() and to the game itself.
                                    '''if show_spells:
                                        spell_levels = attr_reader.read_spells(entity.pointer)
                                        draw.spell_level(pos, spell_levels)'''
                        
                        if vision_tracker:
                            for ward in wards:
                                try:
                                    texture = wards_texture[ward.name.lower()]
                                    pos = world_to_screen(view_proj_matrix, ward.x, ward.z, ward.y)
                                    draw_texture(texture, pos[0], pos[1] + 10, Colors.White, 0, scale=0.5)
                                    draw.entity_range(view_proj_matrix, (ward.x, ward.z, ward.y), 900.0, 1.7, Colors.Magenta)
                                    draw.entity_range(view_proj_matrix, (ward.x, ward.z, ward.y), 8.0, 2, Colors.Purple)
                                except:
                                    pass

                        if show_focused:
                            target = select_target(player, entities)
                            if target:
                                pos = world_to_screen_limited(view_proj_matrix, target.x, target.z, target.y)
                                if pos:
                                    draw.line_to_enemy(own_pos, pos, 2.0, Colors.Magenta)
                        
                        end_drawing()

                        if not on_window.value:
                            overlay_close()
                            break

                except Exception as drawings_loop:
                    debug_info(drawings_loop, True)
                    overlay_close()



