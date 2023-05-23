def gui(terminate):

    #ext
    from webbrowser import open_new_tab
    from random import choice
    from string import printable
    import dearpygui.dearpygui as dpg
    from json import load

    #own
    from Settings import jsonSetter
    from Data import Data

    def set_kiting_mode(_, data):jsonSetter().setMode('kiting', data)
    def ent_target_prio(_, data):jsonSetter().setMode('orbwalk', data)
    def min_target_prio(_, data):jsonSetter().setMode('lasthit', data)
    def set_potato(_, data):jsonSetter().setSetting('ppc', data)
    def set_autoconfig(_, data):jsonSetter().setSetting('autoconfig', data)
    def set_autokite_key(_, data):jsonSetter().setKey('orbwalk', data)
    def set_laneclear_key(_, data):jsonSetter().setKey('laneclear', data)
    def set_lasthit_key(_, data):jsonSetter().setKey('lasthit', data)
    def set_attack_key(_, data):jsonSetter().setKey('attack', data)
    def set_range_key(_, data):jsonSetter().setKey('range', data)

    def set_can_draw(_, data):jsonSetter().setSetting('ext_drawings', data)
    def set_can_track(_, data):jsonSetter().setSetting('ext_track', data)
    def set_can_focus(_, data):jsonSetter().setSetting('ext_focus', data)
    def set_can_healths(_, data):jsonSetter().setSetting('ext_healths', data)
    def set_restricted(_, data):jsonSetter().setSetting('ext_limited', data)

    def set_freeze(_, data):jsonSetter().setSetting('freeze', data)

    def safe_title():return "".join(choice(printable) for i in range(11))

    def updates_github():open_new_tab("https://github.com/vakdev/VakScript")

    with open(Data.settings_file_name, 'r+') as json_file:
        opt = load(json_file)
        orbwalk_key = opt['AutoKite']['Keys']['orbwalk']
        laneclear_key = opt['AutoKite']['Keys']['laneclear']
        lasthit_key = opt['AutoKite']['Keys']['lasthit']
        attack_key = opt['AutoKite']['Keys']['attack']
        range_key = opt['AutoKite']['Keys']['range']
        mode_kiting = opt['AutoKite']['Modes']['kiting']
        mode_orbwalk = opt['AutoKite']['Modes']['orbwalk']
        mode_lasthit = opt['AutoKite']['Modes']['lasthit']
        autoconfig = opt['AutoKite']['Settings']['autoconfig']
        ppc = opt['AutoKite']['Settings']['ppc']
        can_draw = opt['AutoKite']['Settings']['ext_drawings']
        can_track = opt['AutoKite']['Settings']['ext_track']
        can_focus = opt['AutoKite']['Settings']['ext_focus']
        limited_draw = opt['AutoKite']['Settings']['ext_limited']
    
    width, height = 300, 540

    dpg.create_context()
    dpg.create_viewport(title=safe_title(), width= width, height= height, max_width=width, max_height=height, x_pos=0, y_pos=0, resizable=False, vsync=True, always_on_top=False, decorated=True)
    with dpg.window(label="Example Window", width=width, height=height, no_move=True, no_collapse=True, no_title_bar=True, no_resize=True, no_close=True, autosize=False, no_background=False):
        dpg.add_text("Spaceglider {}".format(Data.script_version), color=(255, 255, 0, 255))
        dpg.add_combo(items=["Normal", "In-place"], label="Kiting mode", default_value=mode_kiting.capitalize(), width=150, callback=set_kiting_mode)
        dpg.add_combo(items=["Less Basic Attacks", "Nearest Enemy", "Most Damage"], label="Target Prio", default_value=mode_orbwalk, width=150, callback=ent_target_prio)
        dpg.add_combo(items=["Auto", "Manual"], label="Last Hit mode", default_value=mode_lasthit.capitalize(), width=150, callback=min_target_prio)
        dpg.add_combo(items=["Lowest Health (LC)"], label="Target Prio", default_value="Lowest Health (LC)", width=150)
        dpg.add_checkbox(label="External drawings (bordless)", default_value=can_draw, callback=set_can_draw)
        dpg.add_checkbox(label="Show enemies position", default_value=can_track, callback=set_can_track)
        dpg.add_checkbox(label="Show target to focus", default_value=can_focus, callback=set_can_focus)
        dpg.add_checkbox(label="Show enemies health", default_value=can_focus, callback=set_can_healths)
        dpg.add_checkbox(label="Restrict Track", default_value=limited_draw, callback=set_restricted)
        dpg.add_checkbox(label="Potato PC", default_value=ppc, callback=set_potato)
        dpg.add_checkbox(label="Autoconfig", default_value=False, callback=set_autoconfig)
        dpg.add_input_text(label="Auto Kite Key", width=50, no_spaces=True, hint=orbwalk_key.upper(), callback=set_autokite_key)
        dpg.add_input_text(label="Laneclear Key", width=50, no_spaces=True, hint=laneclear_key.upper(), callback=set_laneclear_key)
        dpg.add_input_text(label="Last Hit Key", width=50, no_spaces=True, hint=lasthit_key.upper(), callback=set_lasthit_key)
        dpg.add_input_text(label="Attack Key", width=30, no_spaces=True, hint=attack_key.upper(), callback=set_attack_key)
        dpg.add_input_text(label="Range Key", width=30, no_spaces=True, hint=range_key.upper(), callback=set_range_key)
        dpg.add_checkbox(label="Freeze", default_value=False, callback=set_freeze)
        dpg.add_text("Free Software!.", color=(0, 255, 0, 255))
        dpg.add_text("Discord: Vakdev Zet#5964", color=(180, 0, 180, 255))
        dpg.add_button(label="Updates", callback=updates_github)
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    terminate.value = True
