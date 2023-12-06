from pyMeow import draw_font, new_color

from script_class import UserScript

class Script(UserScript):
    def __init__(self):
        super().__init__()
        # script_name is used in VakScript GUI
        self.script_name = 'Example Script'

        # script_prefix is used in settings.json where all script settins is stored
        self.script_prefix = 'example'

    def main(self, attr_reader, draw, world, local_player, champions, wards, minions, turrets, game_time):
        # recieving view proj matrix
        view_proj_matrix = world.get_view_proj_matrix()

        # recieving world to screen function
        world_to_screen = world.world_to_screen

        # reading player attributes (name, coords, health, mana etc.)
        player = attr_reader.read_player(local_player)

        # if reading was successful
        if player:
            # converting player game coords to screen coords
            # it's needed to tell the script where to draw
            own_pos = world_to_screen(view_proj_matrix, player.x, player.z, player.y)

            # drawing text on player champion position, own_pos[0] is x, own_pos[1] is y
            # draw_font(fontId: int, text: string, posX, posY, fontSize, spacing: float, tint: Color)
            # fontId is font id from scripts_manager.py
            draw_font(1, f'{self.script_name}', own_pos[0] + 30, own_pos[1] + 20, 20, 2, new_color(255, 203, 0, 255))
            