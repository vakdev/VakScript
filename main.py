#ext
from multiprocessing import Process, Value, Manager, freeze_support
from dearpygui.dearpygui import create_context, destroy_context, create_viewport, setup_dearpygui, show_viewport, is_dearpygui_running, render_dearpygui_frame
from dearpygui.dearpygui import window, tab_bar, tab
from dearpygui.dearpygui import add_text, add_checkbox, add_button, add_combo, add_input_text
from json import load
from random import choice
from string import printable
from webbrowser import open_new_tab
from ctypes import windll
import sys

#own
from spaceglider import spaceglider
from autosmite import autosmite
from drawings import drawings
from autoconfig import start_autoconfig
from data import Data
from settings import jsonSetter
from utils import is_active_window

spaceglider_settings = {}
autosmite_settings = {}
spaceglider_terminate = Value('i', 0)
autosmite_terminate = Value('i', 0)
drawings_terminate = Value('i', 0)

#Getting JSON info and add to settings dict object.
def update_dict_settings():
    with open(Data.settings_file_name, 'r+') as json_file:
        data = load(json_file)

        #keys
        spaceglider_settings['orbwalk'] = data['AutoKite']['Keys']['orbwalk']
        spaceglider_settings['laneclear'] = data['AutoKite']['Keys']['laneclear']
        spaceglider_settings['lasthit'] = data['AutoKite']['Keys']['lasthit']
        spaceglider_settings['attack'] = data['AutoKite']['Keys']['attack']
        spaceglider_settings['range'] = data['AutoKite']['Keys']['range']

        #modes
        spaceglider_settings['kiting'] = data['AutoKite']['Modes']['kiting']
        spaceglider_settings['prio'] = data['AutoKite']['Modes']['orbwalk']
        spaceglider_settings['lhmode'] = data['AutoKite']['Modes']['lasthit']

        #settings
        spaceglider_settings['autoconfig'] = data['AutoKite']['Settings']['autoconfig']
        spaceglider_settings['ppc'] = data['AutoKite']['Settings']['ppc']
        spaceglider_settings['ext_track'] = data['AutoKite']['Settings']['ext_track']
        spaceglider_settings['ext_focus'] = data['AutoKite']['Settings']['ext_focus']
        spaceglider_settings['ext_healths'] = data['AutoKite']['Settings']['ext_healths']
        spaceglider_settings['ext_limited'] = data['AutoKite']['Settings']['ext_limited']
        spaceglider_settings['freeze'] = data['AutoKite']['Settings']['freeze']

        #keys (Auto Smite)
        autosmite_settings['smite'] = data['AutoSmite']['Keys']['smite']
        autosmite_settings['update'] = data['AutoSmite']['Keys']['update']
        autosmite_settings['randb'] = data['AutoSmite']['Keys']['randb']

        #targets (Auto Smite)
        autosmite_settings['targets'] = data['AutoSmite']['Targets']
    
update_dict_settings()

class Functions:

    def game_on_front():
        if is_active_window():
            spaceglider_settings['can_script'] = True
            autosmite_settings['can_script'] = True
        else:
            spaceglider_settings['can_script'] = False
            autosmite_settings['can_script'] = False

    def check_autoconfig():
        if spaceglider_settings['autoconfig']:
            start_autoconfig()

    def use_spaceglider(_, data):
        if data:
            spaceglider_terminate.value = 0
            process = Process(target=spaceglider, args=(spaceglider_terminate, spaceglider_settings))
            process.start()
        else:
            spaceglider_terminate.value = 1

    def use_drawings(_, data):
        if data:
            drawings_terminate.value = 0
            process = Process(target=drawings, args=(drawings_terminate, spaceglider_settings))
            process.start()
        else:
            drawings_terminate.value = 1

    def use_autosmite(_, data):
        if data:
            autosmite_terminate.value = 0
            process = Process(target=autosmite, args=(autosmite_terminate, autosmite_settings))
            process.start()
        else:
            autosmite_terminate.value = 1

    def get_default(id, script=spaceglider_settings):
        return script.get(id, False)

    def set_orbwalk_key(_, data): jsonSetter().setKey('orbwalk', data)
    def set_laneclear_key(_, data): jsonSetter().setKey('laneclear', data)
    def set_lasthit_key(_, data): jsonSetter().setKey('lasthit', data)
    def set_attack_key(_, data): jsonSetter().setKey('attack', data)
    def set_range_key(_, data): jsonSetter().setKey('range', data)
    def set_smite_key(_, data): jsonSetter().setSmiteKey('smite', data)
    def set_update_key(_, data): jsonSetter().setSmiteKey('update', data)
    def set_mode_kiting(_, data): jsonSetter().setMode('kiting', data)
    def set_mode_orbwalk(_, data): jsonSetter().setMode('orbwalk', data)
    def set_mode_lasthit(_, data): jsonSetter().setMode('lasthit', data)
    def set_setting_autoconfig(_, data): jsonSetter().setSetting('autoconfig', data)
    def set_setting_ppc(_, data): jsonSetter().setSetting('ppc', data)
    def set_setting_ext_track(_, data): jsonSetter().setSetting('ext_track', data)
    def set_setting_ext_focus(_, data): jsonSetter().setSetting('ext_focus', data)
    def set_setting_ext_healths(_, data): jsonSetter().setSetting('ext_healths', data)
    def set_setting_ext_limited(_, data): jsonSetter().setSetting('ext_limited', data)
    def set_setting_freeze(_, data): jsonSetter().setSetting('freeze', data)
    def set_randb(_, data): jsonSetter().setSmiteKey('randb', data)

    def safe_title():return "".join(choice(printable) for i in range(11))
    def discord_server():open_new_tab('https://discord.gg/uxvKc4XmNr')
    def github_link():open_new_tab('https://github.com/vakdev/VakScript')
    def youtube_link():open_new_tab('https://www.youtube.com/@vakdev881')



width, height = 290, 525
create_context()
with window(label='', width=width, height=height, no_move=True, no_resize=True, no_title_bar=True):
    with tab_bar():
        #SPACEGLIDER TAB
        with tab(label='Spaceglider'):
            add_checkbox(label='Use Spaceglider', callback=Functions.use_spaceglider)
            add_combo(
                label='Kiting mode', width=150, items=['Normal','In-place'],
                default_value=Functions.get_default('kiting'),
                callback=Functions.set_mode_kiting
            )
            add_combo(
                label='Target Prio', width=150, items=['Less Basic Attacks','Nearest Enemy','Most Damage'],
                default_value=Functions.get_default('prio'),
                callback=Functions.set_mode_orbwalk
            )
            add_combo(
                label='Lasthit mode', width=150, items=['Auto','Manual'],
                default_value=Functions.get_default('lhmode'),
                callback=Functions.set_mode_lasthit
            )
            add_checkbox(
                label='External drawings (borderless)',
                default_value=False,
                callback=Functions.use_drawings
            )
            add_checkbox(
                label='Show enemies position',
                default_value=Functions.get_default('ext_track'),
                callback=Functions.set_setting_ext_track
            )
            add_checkbox(
                label='Show target to focus',
                default_value=Functions.get_default('ext_focus'),
                callback=Functions.set_setting_ext_focus
            )
            add_checkbox(
                label='Show enemies health',
                default_value=Functions.get_default('ext_healths'),
                callback=Functions.set_setting_ext_healths
            )
            add_checkbox(
                label='Limit track',
                default_value=Functions.get_default('ext_limited'),
                callback=Functions.set_setting_ext_limited
            )
            add_checkbox(
                label='Freeze',
                default_value=Functions.get_default('freze'),
                callback=Functions.set_setting_freeze
            )
            
            add_checkbox(
                label='Potato PC',
                default_value=Functions.get_default('ppc'),
                callback=Functions.set_setting_ppc
            )
            add_checkbox(
                label='Autoconfig',
                default_value=False,
                callback=Functions.set_setting_autoconfig
            )

            add_text('Keys to use:', color=(128, 0, 128, 255))

            add_input_text(
                label='Spaceglider Key', width=50, no_spaces=True,
                hint=Functions.get_default('orbwalk').upper(),
                callback=Functions.set_orbwalk_key
            )

            add_input_text(
                label='Laneclear Key', width=50, no_spaces=True,
                hint=Functions.get_default('laneclear').upper(),
                callback=Functions.set_laneclear_key
            )

            add_input_text(
                label='Lasthit Key', width=50, no_spaces=True,
                hint=Functions.get_default('lasthit').upper(),
                callback=Functions.set_lasthit_key
            )

            add_text('Keys In-game:', color=(0, 100, 0, 255))

            add_input_text(
                label='PlayerAttackMoveClick', width=30, no_spaces=True,
                hint=Functions.get_default('attack').upper(),
                callback=Functions.set_attack_key
            )

            add_input_text(
                label='ShowAdvancedPlayerStats', width=30, no_spaces=True,
                hint=Functions.get_default('range').upper(),
                callback=Functions.set_range_key
            )

        #AUTO SMITE TAB
        with tab(label='AutoSmite'):
            add_checkbox(label='Use Auto Smite', callback=Functions.use_autosmite)
                
            add_checkbox(
                label='Consider Blue / Red / Crab',
                default_value=Functions.get_default('randb'),
                callback=Functions.set_randb
            )

            add_input_text(
                label='Smite Key', width=30, no_spaces=True,
                hint=Functions.get_default('smite', autosmite_settings).upper(),
                callback=Functions.set_smite_key
            )
            add_input_text(
                label='Update Key', width=30, no_spaces=True,
                hint=Functions.get_default('update', autosmite_settings).upper(),
                callback=Functions.set_update_key
            )

        #ABOUT TAB
        with tab(label='About'):
            add_text('Vak Script v.{}'.format(Data.script_version), color=(255, 255, 0, 255))
            add_text('Free Software', color=(0, 255, 0, 255))
            add_button(label='Discord Group', callback=Functions.discord_server)
            add_button(label='YouTube', callback=Functions.youtube_link)
            add_button(label='Updates', callback=Functions.github_link)
            add_text('Discord: Vakdev Zet#5964')

def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    freeze_support()

    #start as admin
    if not is_admin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    #create shared dict (settings)
    manager = Manager()
    spaceglider_settings = manager.dict()
    autosmite_settings = manager.dict()

    create_viewport(
        title=Functions.safe_title(),
        width=width, height=height,
        max_width=width, max_height=height,
        x_pos=0, y_pos=0,
        resizable=False
    )

    setup_dearpygui()
    show_viewport()

    lol_focused = Functions.game_on_front
    should_autoconfig = Functions.check_autoconfig

    while is_dearpygui_running():
        update_dict_settings()
        lol_focused()
        should_autoconfig()
        render_dearpygui_frame()

    destroy_context()
    spaceglider_terminate.value = 1
    autosmite_terminate.value = 1
    drawings_terminate.value = 1
