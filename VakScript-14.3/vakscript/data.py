from os import path
import configparser

"""
TODO:
    - bonus_attack_speed offset in offsets.ini is wrong
"""

class Offsets:
    offsets_file = configparser.ConfigParser()
    offsets_file.read("offsets.ini")
    local_player = int(offsets_file.get("offsets", "local_player"), 16)
    game_time = int(offsets_file.get("offsets", "game_time"), 16)
    view_proj_matrix = int(offsets_file.get("offsets", "view_proj_matrix"), 16)
    champion_list = int(offsets_file.get("offsets", "champion_list"), 16)
    minion_list = int(offsets_file.get("offsets", "minion_list"), 16)
    turret_list = int(offsets_file.get("offsets", "turret_list"), 16)

    obj_name = int(offsets_file.get("offsets", "obj_name"), 16)
    obj_lvl = int(offsets_file.get("offsets", "obj_lvl"), 16)
    obj_team = int(offsets_file.get("offsets", "obj_team"), 16)
    obj_gold = int(offsets_file.get("offsets", "obj_gold"), 16)
    obj_health = int(offsets_file.get("offsets", "obj_health"), 16)
    obj_max_health = int(offsets_file.get("offsets", "obj_max_health"), 16)
    obj_armor = int(offsets_file.get("offsets", "obj_armor"), 16)
    obj_magic_resist = int(offsets_file.get("offsets", "obj_magic_resist"), 16)
    obj_base_attack = int(offsets_file.get("offsets", "obj_base_attack"), 16)
    obj_bonus_attack = int(offsets_file.get("offsets", "obj_bonus_attack"), 16)
    obj_bonus_as = int(offsets_file.get("offsets", "obj_bonus_as"), 16)
    obj_magic_damage = int(offsets_file.get("offsets", "obj_magic_damage"), 16)
    obj_attack_range = int(offsets_file.get("offsets", "obj_attack_range"), 16)
    obj_spawn_count = int(offsets_file.get("offsets", "obj_spawn_count"), 16)
    obj_targetable = int(offsets_file.get("offsets", "obj_targetable"), 16)
    obj_visible = int(offsets_file.get("offsets", "obj_visible"), 16)
    obj_x = int(offsets_file.get("offsets", "obj_x"), 16)
    obj_y = int(offsets_file.get("offsets", "obj_y"), 16)
    obj_z = int(offsets_file.get("offsets", "obj_z"), 16)
    obj_spell_book = int(offsets_file.get("offsets", "obj_spell_book"), 16)

    obj_item_list = int(offsets_file.get("offsets", "obj_item_list"), 16)
    item_info = int(offsets_file.get("offsets", "item_info"), 16)
    item_info_id = int(offsets_file.get("offsets", "item_info_id"), 16)

    spell_info = int(offsets_file.get("offsets", "spell_info"), 16)
    spell_data = int(offsets_file.get("offsets", "spell_data"), 16)
    spell_name = int(offsets_file.get("offsets", "spell_name"), 16)
    spell_level = int(offsets_file.get("offsets", "spell_level"), 16)
    spell_cooldown = int(offsets_file.get("offsets", "spell_cooldown"), 16)
    spell_charges = int(offsets_file.get("offsets", "spell_charges"), 16)

    buff_manager = int(offsets_file.get("offsets", "buff_manager"), 16)
    buff_count = int(offsets_file.get("offsets", "buff_count"), 16)
    buff_count2 = int(offsets_file.get("offsets", "buff_count2"), 16)
    buff_start = int(offsets_file.get("offsets", "buff_start"), 16)
    buff_end = int(offsets_file.get("offsets", "buff_end"), 16)
    buff_info = int(offsets_file.get("offsets", "buff_info"), 16)
    buff_name = int(offsets_file.get("offsets", "buff_name"), 16)

class Info:
    offsets_file = configparser.ConfigParser()
    offsets_file.read("offsets.ini")
    script_version = offsets_file.get("version", "script_version")
    settings_file_name = 'settings.json'
    settings_file_path = path.abspath(settings_file_name)
    font_file_name = 'drawings_font.ttf'
    client_name_executable = 'LeagueClient.exe'
    game_name_executable = 'League of Legends.exe'
    game_name_window = 'League of Legends (TM) Client'
    game_files_path = '\Riot Games\League of Legends'
    settings_to_persist = 'DATA\CFG\defaults\SettingsToPersist.json'
    persisted_settings = 'Config\PersistedSettings.json'
    settings_to_persist_path = path.join(game_files_path, settings_to_persist)
    persisted_settings_path = path.join(game_files_path, persisted_settings)
    url_allgamedata = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
    url_comunitydragon = 'https://raw.communitydragon.org/latest/game/data/characters/{name}/{name}.bin.json'
    root_key = 'characters/{}/characterrecords/root'

VK_CODES = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'space':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}
