# VakScript - Spaceglider for League of Legends (13.10+)

Tool to automate kiting without any attack speed limit, game mode, or entity.
The main purpose is help AD Carry players, not limited to any other role.
It should be used only for practice, because it creates an huge advantage over a normal player.

https://github.com/vakdev/VakScript/assets/93299015/d8412240-c2dc-45fd-a7aa-d93b6670bd67

![Screenshot_1](https://github.com/vakdev/VakScript/assets/93299015/70ace742-0d9a-4350-80fa-4785e989d6b8)


## Functions.
#### 1. Target prio:
 - Nearest.
 - Most feed.
 - Less AA.

#### 2. Lasthit:
 - Auto last hit minions.
 > If it's manual, you have to use a key. If it's auto, it will lasthit with Orbwalk key while enemies aren't in range.

#### 3. Laneclear:
 - Auto kite minions.

#### 4.Drawings:
 - Show current enemy position.
 - Show current enemy health.
 - Show target to focus.

## How to use.
1. Download VakScript.exe (join discord) and settings.json (both files must be in the same directory).
2. Start VakScript.exe as admin in a custom game.
3. If is your first time using VakScript, enable Autoconfig in GUI,  and reconnect.
4.  And now its ready to use.  Just press spacebar or V.
5. If you want to use drawings, set your game screen mode to Borderless covering the whole screen.

## How to convert to .exe
1. Download pyMeow latest release and install. (https://github.com/qb-0/PyMeow)
2. Install pyMeow: pip install *pymeow file name.
3. Install script requirements: pip install -r requirements.txt
4. Convert to .exe file with: pyinstaller --onefile --noconsole main.py
5. Move settings.json to dist carpet (or where .exe is located)

## About.
### Is it  safe to use?
- Yes, it doesn't use any internal game function.  All it does is through external memory reading. 

### Vakdev:
- Discord group: https://discord.com/invite/Dw4Zjtwmz5
- Discord: Vakdev Zet#5964
- YouTube: https://www.youtube.com/@vakdev881

### Based on outdated source: https://github.com/hrt/Lmeme
