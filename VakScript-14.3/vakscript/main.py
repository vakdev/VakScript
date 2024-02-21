#built-in
import sys
from multiprocessing import Process, Manager, freeze_support
from ctypes import windll

#own
from multiprocessing_functions import MultiprocessingFunctions
from gui import show_gui
from scripts_manager import load_scripts

"""
TODO:
    - Optimize scripts loader.
"""

if __name__ == '__main__':
    freeze_support() #required for pyinstaller --onefile

    if not windll.shell32.IsUserAnAdmin():
        windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)
        sys.exit()

    manager = Manager()
    main_instance = MultiprocessingFunctions(manager)

    updater_process = Process(target=main_instance.updater)
    updater_process.start()

    scripts_tabs = []
    print('Loading scripts...')
    loaded_scripts = load_scripts()
    for script in loaded_scripts:
        try:
            scripts_tabs.append(script.VakScript_draw_menu)
        except Exception as e:
            print(f'Error loading {script} tab! Error: {e}')

    show_gui(main_instance, scripts_tabs, loaded_scripts)

    main_instance.drawings_terminate.value = 1
    main_instance.autosmite_terminate.value = 1
    main_instance.updater_terminate.value = 1
    main_instance.spaceglider_terminate.value = 1


