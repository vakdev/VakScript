def autosmite(terminate, settings, jungle_pointers, on_window):
    #verified context and no warnings.
    import requests
    import ssl
    requests.packages.urllib3.disable_warnings()
    ssl._create_default_https_context = ssl._create_unverified_context

    #ext
    from pyMeow import open_process, get_module
    from pyMeow import r_int, r_float
    from win32api import GetSystemMetrics
    from orjson import loads
    from urllib.request import urlopen
    from urllib.parse import quote
    from collections import namedtuple
    from time import sleep
    from win32api import GetAsyncKeyState
    from ctypes import windll
    from keyboard import send
    from gc import collect as del_mem

    #own
    from data import Data, Offsets, VK_CODES
    from world_to_screen import World

    #offsets
    obj_health = Offsets.obj_health
    obj_spawn_count = Offsets.obj_spawn_count
    obj_x = Offsets.obj_x
    obj_y = Offsets.obj_y
    obj_z = Offsets.obj_z

    def get_settings():
        smite_key = settings['smite']
        update_key = VK_CODES[settings['update']]

        return smite_key, update_key
    
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

    rawNames = {
        "GeneratedTip_SummonerSpell_SummonerSmite_DisplayName":600.,
        "GeneratedTip_SummonerSpell_S5_SummonerSmitePlayerGanker_DisplayName":900.,
        "GeneratedTip_SummonerSpell_SummonerSmiteAvatarOffensive_DisplayName":1200.,
        "GeneratedTip_SummonerSpell_SummonerSmiteAvatarDefensive_DisplayName":1200.,
        "GeneratedTip_SummonerSpell_SummonerSmiteAvatarUtility_DisplayName":1200.
    }

    while not terminate.value:
        if on_window.value:
            del_mem()
            try:
                process = open_process(process=Data.game_name_executable)
                base_address = get_module(process, Data.game_name_executable)["base"]
                username = quote(get_username())
                url_request = f"https://127.0.0.1:2999/liveclientdata/playersummonerspells?summonerName={username}"
                smite_key, update_key = get_settings()
                damage = get_damage(rawNames, url_request)

                width, height = GetSystemMetrics(0), GetSystemMetrics(1)
                world = World(process, base_address, width, height)
                world_to_screen = world.world_to_screen_limited
                get_view_proj_matrix = world.get_view_proj_matrix

                def read_attr(process, address, nt):
                    d = dict()
                    d["health"] = r_float(process, address + obj_health)
                    d["is_alive"] = r_int(process, address + obj_spawn_count) % 2 == 0
                    d["x"] = r_float(process, address + obj_x)
                    d["y"] = r_float(process, address + obj_y)
                    d["z"] = r_float(process, address + obj_z)

                    return nt(**d)

                nt = namedtuple('Attributes', 'health is_alive x y z')
                while 1:
                    targets = [read_attr(process, pointer, nt) for pointer in jungle_pointers]
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

            except:
                pass
            
        sleep(.1)
