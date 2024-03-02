#ext
from dearpygui.dearpygui import create_context, destroy_context, create_viewport, setup_dearpygui, show_viewport, is_dearpygui_running, render_dearpygui_frame, set_primary_window
from dearpygui.dearpygui import window, child_window, tab_bar, tab, font_registry, add_font, bind_font, show_style_editor
from dearpygui.dearpygui import add_checkbox, add_text, add_combo, add_input_text, add_image
from dearpygui.dearpygui import theme, bind_theme, add_theme_style, add_theme_component, add_theme_color, theme_component, configure_item
from dearpygui.dearpygui import texture_registry, add_static_texture, load_image, draw_image, add_viewport_drawlist, get_viewport_height, get_viewport_width,bind_item_font
from dearpygui.dearpygui import mvAll, mvThemeCol_FrameBg, mvThemeCat_Core, mvStyleVar_FrameRounding, mvInputInt, mvInputText, mvThemeCol_ChildBg, mvThemeCol_Border,mvThemeCol_ScrollbarGrab
#own
from settings import jsonSetter, jsonGetter
from autoconfig import start_autoconfig

GUI_WIDTH = 340
GUI_HEIGHT = 480

background_image_path = "image.png"

class GUIFunctions:

    def set_spaceglider_data(key, value):
        jsonSetter().set_spaceglider_data(key, value)

    def set_autosmite_data(key, value):
        jsonSetter().set_autosmite_data(key, value)

    def set_drawings_data(key, value):
        jsonSetter().set_drawings_data(key, value)

    def set_autoconfig(data):
        if data:
            start_autoconfig()

def show_gui(main_instance, scripts_tabs, loaded_scripts):
    global GUI_WIDTH

    create_context(no_background = True)

    with font_registry():
        
        default_font = add_font("Prototype.ttf", 15)
        default_font2 = add_font("Prototype.ttf", 18)
    bind_font(default_font)

    width, height, channels, data = load_image("image_1.png")

    with texture_registry():
        texture_id = add_static_texture(width, height, data)
        
 

    with window(label='', width=GUI_WIDTH, height=GUI_HEIGHT, no_move=True, no_resize=True, no_title_bar=True, no_background=True, tag="Primary Window"):  
        with tab_bar():
            with tab(label='Spaceglider'):
                t1=add_checkbox(label='Use Spaceglider', callback=main_instance.start_spaceglider_process)
                with child_window(width=GUI_WIDTH * 0.8, height=360, tag="Spaceglider_settings"):
                    add_combo(
                        label='Kiting mode', width=150, items=['Normal', 'Normal v2', 'In-place', 'Kalista'],
                        default_value=jsonGetter().get_data('kiting_mode'),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('kiting_mode', data),
                    )
                    add_combo(
                        label='Target Prio', width=150, items=['Less Basic Attacks','Nearest Enemy','Most Damage'],
                        default_value=jsonGetter().get_data('orbwalk_prio'),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('orbwalk_prio', data)
                    )
                    add_combo(
                        label='Lasthit mode', width=150, items=['Normal'],
                        default_value=jsonGetter().get_data('lasthit_mode'),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('lasthit_mode', data)
                    )
                    add_checkbox(
                        label='In-game Range',
                        default_value=jsonGetter().get_data('press_range'),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('press_range', data)
                    )
                    add_checkbox(
                        label='Potato PC',
                        default_value=jsonGetter().get_data('ppc'),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('ppc', data)
                    )
                    add_checkbox(
                        label='Autoconfig',
                        default_value=False,
                        callback=GUIFunctions.set_autoconfig
                    )
                    t2=add_text('Keys to use:', color=(255, 255, 255, 255))
                    add_input_text(
                        label='Spaceglider Key', width=50, no_spaces=True,
                        hint=jsonGetter().get_data('orbwalk').upper(),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('orbwalk', data)
                    )
                    add_input_text(
                        label='Laneclear Key', width=50, no_spaces=True,
                        hint=jsonGetter().get_data('laneclear').upper(),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('laneclear', data)
                    )
                    add_input_text(
                        label='Lasthit Key', width=50, no_spaces=True,
                        hint=jsonGetter().get_data('lasthit').upper(),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('lasthit', data)
                    )
                    t3=add_text('Keys In-game:', color=(255, 255, 255, 255))
                    add_input_text(
                        label='PlayerAttackMoveClick', width=30, no_spaces=True,
                        hint=jsonGetter().get_data('attack').upper(),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('attack', data)
                    )
                    add_input_text(
                        label='ShowAdvancedPlayerStats', width=30, no_spaces=True,
                        hint=jsonGetter().get_data('range').upper(),
                        callback=lambda _, data: GUIFunctions.set_spaceglider_data('range', data)
                    )
            
            with tab(label='Drawings'):
                t4=add_checkbox(label='Drawings (borderless)', callback=main_instance.start_drawings_process)
                with child_window(width=GUI_WIDTH * 0.8, height=360):
                    add_checkbox(
                        label='Position',
                        default_value=jsonGetter().get_data('show_position'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('show_position', data)
                    )
                    add_checkbox(
                        label='Prioritized',
                        default_value=jsonGetter().get_data('show_focused'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('show_focused', data)
                    )
                    add_checkbox(
                        label='Health',
                        default_value=jsonGetter().get_data('show_healths'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('show_healths', data)
                    )
                    add_checkbox(
                        label='Player Range',
                        default_value=jsonGetter().get_data('show_player_range'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('show_player_range', data)
                    )
                    add_checkbox(
                        label='Enemy Range',
                        default_value=jsonGetter().get_data('show_enemy_range'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('show_enemy_range', data)
                    )
                    add_checkbox(
                        label='Turret Range',
                        default_value=jsonGetter().get_data('show_turret_range'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('show_turret_range', data)
                    )
                    add_checkbox(
                        label='Hits',
                        default_value=jsonGetter().get_data('show_hits'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('show_hits', data)
                    )
                    add_checkbox(
                        label='Gold',
                        default_value=jsonGetter().get_data('show_gold'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('show_gold', data)
                    )
                    ## REMOVED DUE READ ISSUE [v13.21]
                    #add_checkbox(
                    #    label='Spell level',
                    #    default_value=jsonGetter().get_data('show_spells'),
                    #    callback=lambda _, data: GUIFunctions.set_drawings_data('show_spells', data)
                    #)
                    add_checkbox(
                        label='Vision Tracking',
                        default_value=jsonGetter().get_data('vision_tracker'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('vision_tracker', data)
                    )
                    add_checkbox(
                        label='Limit position',
                        default_value=jsonGetter().get_data('screen_track'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('screen_track', data)
                    )
                    add_input_text(
                        label='Max FPS', width=50, no_spaces=True,
                        hint=jsonGetter().get_data('fps'),
                        callback=lambda _, data: GUIFunctions.set_drawings_data('fps', data)
                    )
                    
            with tab(label='AutoSmite'):
                t5=add_checkbox(label='Use Auto Smite', callback=main_instance.start_autosmite_process)
                with child_window(width=GUI_WIDTH * 0.8, height=80):    
                    add_checkbox(
                        label='Consider Blue / Red / Crab',
                        default_value=jsonGetter().get_data('randb'),
                        callback=lambda _, data: GUIFunctions.set_autosmite_data('randb', data)
                    )
                    add_input_text(
                        label='Smite Key', width=30, no_spaces=True,
                        hint=jsonGetter().get_data('smite').upper(),
                        callback=lambda _, data: GUIFunctions.set_autosmite_data('smite', data)
                    )
                with child_window(width=GUI_WIDTH * 0.8, height=80):
                    add_checkbox(
                        label='Smite Toggle',
                        default_value=jsonGetter().get_data('randa'),
                        callback=lambda _, data: GUIFunctions.set_autosmite_data('randa', data)
                    )
                    add_input_text(
                        label='Smite Toggle Key', width=30, no_spaces=True,
                        hint=jsonGetter().get_data('Smite_toggle').upper(),
                        callback=lambda _, data: GUIFunctions.set_autosmite_data('Smite_toggle', data)
                    )

            with tab(label='Scripts'):
                t6=add_checkbox(label='Turn on external scripts', callback=main_instance.start_scripts_process, user_data=loaded_scripts)
                add_input_text(
                    label='Scripts FPS', width=50, no_spaces=True,
                    hint=jsonGetter().get_data('scripts_fps') if jsonGetter().get_data('scripts_fps') != None else 60,
                    callback=lambda _, data: jsonSetter().set_scripts_data('scripts_fps', data)
                ) 
                for script_tab in scripts_tabs:
                    script_tab() 
                    
    items = [t1, t2, t3, t4, t5, t6]

    for item in items:
        bind_item_font(item, default_font2)   
                                        
    create_viewport(
        title=("Vaskcript 14.4 modified by Shurtug"),
        width=GUI_WIDTH, height=GUI_HEIGHT,
        x_pos=0, y_pos=0,
        resizable=False
    )
    add_viewport_drawlist(tag="drawlist", front=False)
    draw_image(texture_id, tag="background", pmin=(0,0), pmax=(GUI_HEIGHT, GUI_HEIGHT), uv_min=(0,0), uv_max=(1,1), parent="drawlist")

    setup_dearpygui()
    with theme() as global_theme:

        with theme_component(mvAll):
            add_theme_color(mvThemeCol_FrameBg, (10, 0, 40), category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_FrameRounding, 5, category=mvThemeCat_Core)

        with theme_component(mvAll):
            add_theme_color(mvThemeCol_ChildBg, (0, 0, 0, 0), category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_FrameRounding, 5, category=mvThemeCat_Core)
            
            
        with theme_component(mvAll):
            add_theme_color(mvThemeCol_Border, (0, 0, 0, 0), category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_FrameRounding, 5, category=mvThemeCat_Core)
            
    bind_theme(global_theme)
    
    show_viewport()
    set_primary_window("Primary Window", True)
    configure_item("Primary Window", no_background=True)
    while is_dearpygui_running():
        render_dearpygui_frame()

    destroy_context()