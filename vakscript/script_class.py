from multiprocessing import Value
from dearpygui.dearpygui import add_checkbox, tree_node
from settings import jsonSetter, jsonGetter

"""
TODO:
    - Check code.
"""

class UserScript:
    def __init__(self):
        self.script_name = __name__
        self.script_prefix = 'unnamed'
        self.script_terminate = Value('i', 1)

    def hello(self):
        self.script_terminate = Value('i', 0 if self.VakScript_get_setting('enabled') == True else 1)
        return True

    def VakScript_start_process(self, _, state):
        if state:
            self.script_terminate.value = 0
            self.VakScript_set_setting('enabled', True)
        else:
            self.script_terminate.value = 1
            self.VakScript_set_setting('enabled', False)

    def VakScript_draw_menu(self):
        with tree_node(label=f'{self.script_name}', default_open=True):
            add_checkbox(
                label=f'Enable {self.script_name}',
                default_value=True if self.script_terminate.value == 0 else False,
                callback=self.VakScript_start_process
                )
            
    def VakScript_set_setting(self, key, value):
        jsonSetter().set_scripts_data(f'{self.script_prefix}_{key}', value)
        
    def VakScript_get_setting(self, key):
        return jsonGetter().get_data(f'{self.script_prefix}_{key}') if jsonGetter().get_data(f'{self.script_prefix}_{key}') != None else False