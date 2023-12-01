from pyMeow import draw_font, new_color

from multiprocessing import Value

from script_class import UserScript
from entities import EntityConditions
from script_manager import Colors

class Script(UserScript):
    def __init__(self):
        super().__init__()
        self.script_name = 'Example Turret Script'

    def main(self, attr_reader, draw, world, local_player, champions, wards, minions, turrets):
        view_proj_matrix = world.get_view_proj_matrix()
        for turret in turrets:
            if EntityConditions.hurtable(turret):
                draw.entity_range(view_proj_matrix, (turret.x, turret.z, turret.y), 890.0, 1.0, Colors.Red)