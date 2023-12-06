from script_class import UserScript
from entities import EntityConditions
from scripts_manager import Colors

from dearpygui.dearpygui import add_checkbox, tree_node

class Script(UserScript):
    def __init__(self):
        super().__init__()
        self.script_name = 'Example Turret Script'
        self.script_prefix = 'example_turret'
        self.limited = False
    
    # rewriting VakScript_draw_menu function from UserScript class
    def VakScript_draw_menu(self):
        with tree_node(label=f'{self.script_name}', default_open=True):
            add_checkbox(
                label=f'Enable {self.script_name}',
                default_value=self.VakScript_get_setting('enabled'),
                callback=self.VakScript_start_process
                )
            add_checkbox(
                label='Limit position on screen',
                default_value=self.VakScript_get_setting('limited'),
                callback=self.set_limit_position
            )


    def set_limit_position(self, _, state):
        self.VakScript_set_setting('limited', state)


    def main(self, attr_reader, draw, world, local_player, champions, wards, minions, turrets, game_time):
        self.limited = self.VakScript_get_setting('limited')
        view_proj_matrix = world.get_view_proj_matrix()
        for turret in turrets:
            if EntityConditions.hurtable(turret):
                draw.entity_range(view_proj_matrix, (turret.x, turret.z, turret.y), 890.0, 1.0, Colors.Red, limited=self.limited)
