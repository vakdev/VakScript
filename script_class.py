from multiprocessing import Value
from dearpygui.dearpygui import add_checkbox, tree_node

class UserScript:
    def __init__(self):
        self.script_terminate = Value('i', 1)
        self.script_name = __name__

    def hello(self):
        return True

    def VakScript_start_process(self, _, state):
        if state:
            self.script_terminate.value = 0
            print(f'{self.script_name} enabled')
        else:
            self.script_terminate.value = 1
            print(f'{self.script_name} disabled')

    def VakScript_draw_menu(self):
        with tree_node(label=f'{self.script_name}', default_open=True):
            add_checkbox(
                label=f'Enable {self.script_name}',
                default_value=False,
                callback=self.VakScript_start_process
                )