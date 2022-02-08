# Home Assistant Windows Portable (HassWP)

[![Donate](https://img.shields.io/badge/donate-Coffee-yellow.svg)](https://www.buymeacoffee.com/AlexxIT)
[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://money.yandex.ru/to/41001428278477)

Portable version of Home Assistant for Windows.

Tested on Windows 7 and Windows 10 (both 64-bit).

Preinstalled:

- [WinPython](https://winpython.github.io/) v3.8.9 32-bit
- [Home Assistant](https://www.home-assistant.io/) v2021.12.10
- [HACS](https://hacs.xyz/) v1.22.0
- [SonoffLAN](https://github.com/AlexxIT/SonoffLAN) v2.4.6
- [XiaomiGateway3](https://github.com/AlexxIT/XiaomiGateway3) v1.6.5
- [YandexStation](https://github.com/AlexxIT/YandexStation) v3.8.0
- [StartTime](https://github.com/AlexxIT/StartTime) v1.1.6
- [NotePad++](https://notepad-plus-plus.org/) v7.8.5 32bit

**Attention:** Direct works in Windows is not tested by the core developers of Home Assistant. So some components/integrations may not work at all.

# HOWTO

1. Download [HassWP.zip](https://github.com/AlexxIT/HassWP/releases/latest)
2. Unpack
3. Run

Useful files:

- `hass.cmd` - run Home Assistant and default Browser
- `notepad.cmd` - run NotePad with `configuration.yaml`
- `web.url` - open default Browser with http://localhost:8123/
- `config/reset.cmd` - reset Home Assistant but don't touch config files

# Supervisor and Addons

HassWP **don't have and can't have supervisor** and any Hass.io addons. Supervisor can be installed only over Docker. Nativelly Docker works only on Linux core. In any other OS it will use virtualization.

If you really needs Hass.io addons on Windows - use [virtualization](https://www.home-assistant.io/installation/windows).

# Move config

You can transfer your configuration to another Hass installation at any time. In another HassWP, venv, docker, hass.io, etc. Windows or Linux, it doesn't matter. Just move the contents of the `config` folder to a new location. Remember about `config/.storage` folder, it is also important. The `config/deps` folder may not be moved, but if you do, it's not a problem.

Before any movement - stop the old and new Home Assistant!

# Video Demo

[![Home Assistant Windows Portable (HassWP)](https://img.youtube.com/vi/GFw3J3Jbuas/mqdefault.jpg)](https://www.youtube.com/watch?v=GFw3J3Jbuas)

# Problems

1. If you have this problem:

   ```
   File "C:\HassWP\python-3.8.7\lib\socket.py", line 49, in <module>
       import _socket
   ImportError: DLL load failed while importing _socket
   ```
   
   Install Windows update: **KB2533623**.
