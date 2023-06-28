#ext
from multiprocessing import Process, Manager, freeze_support
from dearpygui.dearpygui import create_context, destroy_context, create_viewport, setup_dearpygui, show_viewport, is_dearpygui_running, render_dearpygui_frame
from ctypes import windll 
import sys

#own
from multiprocessing_functions import MultiprocessingFunctions
from gui import gui
from utils import safe_title

def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    freeze_support()

    if not is_admin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    manager = Manager()
    main_instance = MultiprocessingFunctions(manager)

    proc = Process(target=main_instance.updater)
    proc.start()

    width, height = 290, 400
    create_context()
    gui(main_instance, width, height)
    create_viewport(
        title=safe_title(),
        width=width, height=height,
        max_width=width, max_height=height,
        x_pos=0, y_pos=0,
        resizable=False
    )

    setup_dearpygui()
    show_viewport()

    while is_dearpygui_running():
        render_dearpygui_frame()

    destroy_context()
    main_instance.drawings_terminate.value = 1
    main_instance.autosmite_terminate.value = 1
    main_instance.updater_terminate.value = 1
    main_instance.spaceglider_terminate.value = 1
