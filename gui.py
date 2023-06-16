from dearpygui.dearpygui import window, child_window, tab_bar, tab
from dearpygui.dearpygui import add_checkbox, add_text, add_combo, add_input_text
from webbrowser import open_new_tab

#own
from settings import jsonSetter, jsonGetter
from autoconfig import start_autoconfig

class Functions:

    def set_spaceglider_data(key, value):
        jsonSetter().set_spaceglider_data(key, value)

    def set_autosmite_data(key, value):
        jsonSetter().set_autosmite_data(key, value)

    def set_drawings_data(key, value):
        jsonSetter().set_drawings_data(key, value)

    def set_autoconfig(data):
        if data:
            start_autoconfig()

    def open_link(url):
        open_new_tab(url)

def gui(main_instance, width, height):
    with window(label='', width=width, height=height, no_move=True, no_resize=True, no_title_bar=True):
        with tab_bar():
            with tab(label='Spaceglider'):
                add_checkbox(label='Use Spaceglider', callback=main_instance.start_spaceglider_process)
                with child_window(width=260, height=300):
                    add_combo(
                        label='Kiting mode', width=150, items=['Normal','In-place'],
                        default_value=jsonGetter().get_data('kiting_mode'),
                        callback=lambda _, data: Functions.set_spaceglider_data('kiting_mode', data)
                    )
                    add_combo(
                        label='Target Prio', width=150, items=['Less Basic Attacks','Nearest Enemy','Most Damage'],
                        default_value=jsonGetter().get_data('orbwalk_prio'),
                        callback=lambda _, data: Functions.set_spaceglider_data('orbwalk_prio', data)
                    )
                    add_combo(
                        label='Lasthit mode', width=150, items=['Auto','Manual'],
                        default_value=jsonGetter().get_data('lasthit_mode'),
                        callback=lambda _, data: Functions.set_spaceglider_data('lasthit_mode', data)
                    )
                    add_checkbox(
                        label='Potato PC',
                        default_value=jsonGetter().get_data('ppc'),
                        callback=lambda _, data: Functions.set_spaceglider_data('ppc', data)
                    )
                    add_checkbox(
                        label='Autoconfig',
                        default_value=False,
                        callback=Functions.set_autoconfig
                    )
                    add_text('Keys to use:', color=(128, 0, 128, 255))
                    add_input_text(
                        label='Spaceglider Key', width=50, no_spaces=True,
                        hint=jsonGetter().get_data('orbwalk').upper(),
                        callback=lambda _, data: Functions.set_spaceglider_data('orbwalk', data)
                    )
                    add_input_text(
                        label='Laneclear Key', width=50, no_spaces=True,
                        hint=jsonGetter().get_data('laneclear').upper(),
                        callback=lambda _, data: Functions.set_spaceglider_data('laneclear', data)
                    )
                    add_input_text(
                        label='Lasthit Key', width=50, no_spaces=True,
                        hint=jsonGetter().get_data('lasthit').upper(),
                        callback=lambda _, data: Functions.set_spaceglider_data('lasthit', data)
                    )
                    add_text('Keys In-game:', color=(0, 100, 0, 255))
                    add_input_text(
                        label='PlayerAttackMoveClick', width=30, no_spaces=True,
                        hint=jsonGetter().get_data('attack').upper(),
                        callback=lambda _, data: Functions.set_spaceglider_data('attack', data)
                    )
                    add_input_text(
                        label='ShowAdvancedPlayerStats', width=30, no_spaces=True,
                        hint=jsonGetter().get_data('range').upper(),
                        callback=lambda _, data: Functions.set_spaceglider_data('range', data)
                    )
            
            with tab(label='Drawings'):
                add_checkbox(label='Enemy Info (borderless)', callback=main_instance.start_drawings_process)
                with child_window(width=260, height=150):
                    add_checkbox(
                        label='Position',
                        default_value=jsonGetter().get_data('position_tracker'),
                        callback=lambda _, data: Functions.set_drawings_data('position_tracker', data)
                    )
                    add_checkbox(
                        label='Prioritized',
                        default_value=jsonGetter().get_data('show_focused'),
                        callback=lambda _, data: Functions.set_drawings_data('show_focused', data)
                    )
                    add_checkbox(
                        label='Health',
                        default_value=jsonGetter().get_data('show_healths'),
                        callback=lambda _, data: Functions.set_drawings_data('show_healths', data)
                    )
                    add_checkbox(
                        label='Gold',
                        default_value=jsonGetter().get_data('show_gold'),
                        callback=lambda _, data: Functions.set_drawings_data('show_gold', data)
                    )
                    add_checkbox(
                        label='Cooldowns',
                        default_value=jsonGetter().get_data('spell_tracker'),
                        callback=lambda _, data: Functions.set_drawings_data('spell_tracker', data)
                    )
                    add_checkbox(
                        label='Limit position',
                        default_value=jsonGetter().get_data('screen_track'),
                        callback=lambda _, data: Functions.set_drawings_data('screen_track', data)
                    )
                    
            with tab(label='AutoSmite'):
                add_checkbox(label='Use Auto Smite', callback=main_instance.start_autosmite_process)
                with child_window(width=260, height=83):    
                    add_checkbox(
                        label='Consider Blue / Red / Crab',
                        default_value=jsonGetter().get_data('randb'),
                        callback=lambda _, data: Functions.set_autosmite_data('randb', data)
                    )
                    add_input_text(
                        label='Smite Key', width=30, no_spaces=True,
                        hint=jsonGetter().get_data('smite').upper(),
                        callback=lambda _, data: Functions.set_autosmite_data('smite', data)
                    )
                    add_input_text(
                        label='Update Key', width=30, no_spaces=True,
                        hint=jsonGetter().get_data('update').upper(),
                        callback=lambda _, data: Functions.set_autosmite_data('update', data)
                    )
