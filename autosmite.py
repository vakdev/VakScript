def autosmite(terminate, settings):
    #verified context and no warnings.
    import requests
    import ssl
    requests.packages.urllib3.disable_warnings()
    ssl._create_default_https_context = ssl._create_unverified_context

    #ext
    from pyMeow import open_process, get_module, get_window_info
    from pyMeow import r_int, r_float, r_uint64, r_ints64, r_int64, r_string
    from orjson import loads
    from urllib.request import urlopen
    from collections import namedtuple
    from time import sleep
    from win32api import GetAsyncKeyState
    from ctypes import windll
    from keyboard import send
    from gc import collect as del_mem

    #own
    from data import Data, Offsets, VK_CODES
    from utils import is_active_window
    from world_to_screen import World

    #offsets
    obj_name = Offsets.obj_name
    obj_health = Offsets.obj_health
    obj_spawn_count = Offsets.obj_spawn_count
    obj_x = Offsets.obj_x
    obj_y = Offsets.obj_y
    obj_z = Offsets.obj_z
    minion_list = Offsets.minion_list

    def get_settings():
        smite_key = settings['smite']
        update_key = VK_CODES[settings['update']]
        randb = settings['randb']
        entities = settings['targets']

        return smite_key, update_key, randb, entities
    
    def get_username():
        return loads(urlopen("https://127.0.0.1:2999/liveclientdata/activeplayername").read())

    def get_damage(rawNames, url_request):
        spells = loads(urlopen(url_request).read())
        sp1, sp2 = spells["summonerSpellOne"], spells["summonerSpellTwo"]
        for v, v2 in zip(sp1.values(), sp2.values()):
            if v in rawNames:
                return rawNames[v]
            if v2 in rawNames:
                return rawNames[v2]

    def valid_pointer(process, pointer, entities):
        try:
            return r_string(process, r_int64(process, pointer + obj_name)).lower() in entities
        except:
            try:
                return r_string(process, pointer + obj_name).lower() in entities
            except:
                return False

    def get_pointers(process, base_address, entities, size):
        readManager = r_uint64(process, base_address + minion_list)
        pointers = r_ints64(process, r_int64(process, readManager + 0x8), size)
        return [pointer for pointer in pointers if valid_pointer(process, pointer, entities)]


    rawNames = {
        "GeneratedTip_SummonerSpell_SummonerSmite_DisplayName":600.,
        "GeneratedTip_SummonerSpell_S5_SummonerSmitePlayerGanker_DisplayName":900.,
        "GeneratedTip_SummonerSpell_SummonerSmiteAvatarOffensive_DisplayName":1200.,
        "GeneratedTip_SummonerSpell_SummonerSmiteAvatarDefensive_DisplayName":1200.,
        "GeneratedTip_SummonerSpell_SummonerSmiteAvatarUtility_DisplayName":1200.
    }

    while not terminate.value:
        del_mem()
        try:
            process = open_process(process=Data.game_name_executable)
            base_address = get_module(process, Data.game_name_executable)["base"]
            username = get_username()
            username = username.replace(' ', '%20')
            url_request = f"https://127.0.0.1:2999/liveclientdata/playersummonerspells?summonerName={username}"
            smite_key, update_key, randb, entities = get_settings()

            if not randb:
                entities.remove('sru_blue')
                entities.remove('sru_red')
                entities.remove('sru_crab')

            entities = set(entities)
            damage = get_damage(rawNames, url_request)

            if is_active_window():
                *_, width, height = get_window_info(Data.game_name_window)
                world = World(process, base_address, width, height)
                world_to_screen = world.world_to_screen_limited
                get_view_proj_matrix = world.get_view_proj_matrix

            else:
                continue

            def read_attr(process, address, nt):
                d = dict()
                d["health"] = r_float(process, address + obj_health)
                d["is_alive"] = r_int(process, address + obj_spawn_count) % 2 == 0
                d["x"] = r_float(process, address + obj_x)
                d["y"] = r_float(process, address + obj_y)
                d["z"] = r_float(process, address + obj_z)

                return nt(**d)

            nt = namedtuple('Attributes', 'health is_alive x y z')
            while settings['can_script']:
                targets = [read_attr(process, pointer, nt) for pointer in get_pointers(process, base_address, entities, 0x100)]
                target = [entity for entity in targets if entity.health <= damage and entity.is_alive]

                if target:
                    pos = world_to_screen(get_view_proj_matrix(), target[0].x, target[0].z, target[0].y)
                    if pos:
                        windll.user32.SetCursorPos(int(pos[0]), int(pos[1]))
                        send(smite_key)
                        targets.clear()
                        sleep(0.03)

                elif GetAsyncKeyState(update_key):
                    damage = get_damage(rawNames, url_request)
                    *_, width, height = get_window_info(Data.game_name_window)

        except:
            pass
