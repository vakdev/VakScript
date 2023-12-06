#built-in
from gc import collect as del_mem
from math import cos, sin, pi
from glob import glob
import os
import sys
from time import sleep

#ext
from pyMeow import open_process, get_module, load_font, new_color
from pyMeow import overlay_init, overlay_loop, overlay_close, begin_drawing, end_drawing
from pyMeow import draw_line, draw_circle
from pyMeow import r_uint64, r_float
from win32api import GetSystemMetrics

#own
from data import Info, Offsets
from entities import AttributesReader
from world_to_screen import World
from utils import safe_title
from settings import jsonGetter, jsonSetter


"""
TODO:
    - Remove re-writting of Colors and Drawings class. Import from drawings.py instead.
    - Check code.
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

    def entity_range(self, view_proj_matrix, game_pos, radius, thickness=1.0, color=Colors.Cyan, limited=False):
        world_to_screen = self.world_to_screen_limited if limited else self.world_to_screen
        for i in range(self.num_vert):
            vec1 = world_to_screen(
                view_proj_matrix, game_pos[0] + self.cos_values[i] * radius, game_pos[1], game_pos[2] + self.sin_values[i] * radius
            )

            next_index = (i + 1) % self.num_vert

            vec2 = world_to_screen(
                view_proj_matrix, game_pos[0] + self.cos_values[next_index] * radius, game_pos[1], game_pos[2] + self.sin_values[next_index] * radius
            )
            if vec1 and vec2:
                draw_line(vec1[0], vec1[1], vec2[0], vec2[1], color, thickness)
        
    def line_to_enemy(self, own_pos, pos, thickness=1.0, color=Colors.Lime):
        draw_line(own_pos[0], own_pos[1], pos[0], pos[1], color, thickness)
        draw_circle(pos[0], pos[1], 5.0, color)

def load_scripts():
    sys.path.insert(0, './scripts')
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    scripts_folder = os.path.join(application_path, 'scripts')
    python_files = glob(os.path.join(scripts_folder, '*.py'))

    loaded_scripts = []
    for file in python_files:
        module_name = os.path.splitext(os.path.basename(file))[0]
        try:
            module = __import__(module_name)
            module_class = module.Script()
            if module_class.hello():
                print(f'Loaded successfully: {module_name}')
                loaded_scripts.append(module_class)
            else:
                print(f'Error loading {module_name}')
        except Exception as e:
            print(f'Error loading {module_name}: {e}')
            
    return loaded_scripts

def execute_scripts(terminate, user_data, champion_pointers, ward_pointers, minion_pointers, turret_pointers, on_window):
    while not terminate.value:
        if jsonGetter().get_data('scripts_fps'):
            fps = int(jsonGetter().get_data('scripts_fps'))
        else:
            fps = 60
            jsonSetter().set_scripts_data('scripts_fps', fps)
            
        if on_window.value:
            del_mem()
            process = open_process(process=Info.game_name_executable)
            base_address = get_module(process, Info.game_name_executable)['base']
            local_player = r_uint64(process, base_address + Offsets.local_player)
            attr_reader = AttributesReader(process, base_address)

            screen_width = GetSystemMetrics(0)
            screen_height = GetSystemMetrics(1)

            world = World(process, base_address, screen_width, screen_height)
            draw = Draw(world, screen_width, screen_height)

            loaded_scripts = user_data

            overlay_init(title=safe_title(), fps=fps)
            load_font(Info.font_file_name, 1)
            while overlay_loop():
                champions = [attr_reader.read_enemy(pointer) for pointer in champion_pointers]
                wards = [attr_reader.read_minion(pointer) for pointer in ward_pointers]
                minions = [attr_reader.read_minion(pointer) for pointer in minion_pointers]
                turrets = [attr_reader.read_turret(pointer) for pointer in turret_pointers]
                game_time = r_float(process, base_address + Offsets.game_time)

                begin_drawing()
                for script in loaded_scripts:
                    if script.script_terminate.value:
                        continue
                    script.main(attr_reader, draw, world, local_player, champions, wards, minions, turrets, game_time)
                end_drawing()

                if not on_window.value:
                    overlay_close()
                    break

        sleep(0.1)
