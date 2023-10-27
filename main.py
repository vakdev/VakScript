
"""
[v13.21]:
    - Auto last hit while spacing removed.
    - Spell tracker (lvl) removed.
    - Custom pyMeow.pyd removed.
"""

#built-in
import sys
from multiprocessing import Process, Manager, freeze_support
from ctypes import windll

#own
from multiprocessing_functions import MultiprocessingFunctions
from gui import show_gui
from utils import debug_info

if __name__ == '__main__':
    freeze_support() #required for pyinstaller --onefile

    if not windll.shell32.IsUserAnAdmin():
        windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)
        sys.exit()

    manager = Manager()
    main_instance = MultiprocessingFunctions(manager)

    updater_process = Process(target=main_instance.updater)
    updater_process.start()
    
    show_gui(main_instance)

    main_instance.drawings_terminate.value = 1
    main_instance.autosmite_terminate.value = 1
    main_instance.updater_terminate.value = 1
    main_instance.spaceglider_terminate.value = 1


