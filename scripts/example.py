from pyMeow import draw_font, new_color

from script_class import UserScript

class Script(UserScript):
    def __init__(self):
        super().__init__()
        self.script_name = 'Example Script'

    def main(self, attr_reader, draw, world, local_player, champions, wards, minions, turrets):
        view_proj_matrix = world.get_view_proj_matrix()
        world_to_screen = world.world_to_screen
        player = attr_reader.read_player(local_player)
        if player:
            own_pos = world_to_screen(view_proj_matrix, player.x, player.z, player.y)
            draw_font(1, f'{self.script_name}', own_pos[0] + 30, own_pos[1] + 20, 20, 2, new_color(255, 203, 0, 255))

'''def main():
    print(f'Hello from example.py. On_window: {main_instance.on_window.value}')
    while not script_terminate.value:
        draw_font(1, 'Example Script', 777, 666, 20, 2, new_color(255, 203, 0, 255))

    sleep(0.013)'''
            