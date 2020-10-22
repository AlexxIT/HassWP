# Home Assistant Windows Portable (HassWP)

[![Donate](https://img.shields.io/badge/donate-Coffee-yellow.svg)](https://www.buymeacoffee.com/AlexxIT)
[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://money.yandex.ru/to/41001428278477)

Portable version of Home Assistant for Windows.

Tested on Windows 7 and Windows 10 (both 64-bit).

Preinstalled:

- [WinPython](https://winpython.github.io/) v3.8.5 32bit
- [Home Assistant](https://www.home-assistant.io/) v0.116.4
- [HACS](https://hacs.xyz/) v1.6.0
- [SonoffLAN](https://github.com/AlexxIT/SonoffLAN) v2.3.2
- [XiaomiGateway3](https://github.com/AlexxIT/XiaomiGateway3) v0.7.2
- [YandexStation](https://github.com/AlexxIT/YandexStation) v2.2.11
- [StartTime](https://github.com/AlexxIT/StartTime) v1.1.4
- [NotePad++](https://notepad-plus-plus.org/) v7.8.5 32bit

# HOWTO

1. Download [HassWP.zip](https://github.com/AlexxIT/HassWP/releases/latest)
2. Unpack
3. Run

Useful files:

- `hass.cmd` - run Home Assistant and default Browser
- `notepad.cmd` - run NotePad with `configuration.yaml`
- `update.cmd` - try update Home Assistant version (stop Hass before updating)
- `web.url` - open default Browser with http://localhost:8123/
- `config/reset.cmd` - reset Home Assistant but don't touch config files

# Move config

You can transfer your configuration to another Hass installation at any time. In another HassWP, venv, docker, hass.io, etc. Windows or Linux, it doesn't matter. Just move the contents of the `config` folder to a new location. Remember about `config/.storage` folder, it is also important. The `config/deps` folder may not be moved, but if you do, it's not a problem.

Before any movement - stop the old and new Home Assistant!

# Video Demo

[![Home Assistant Windows Portable (HassWP)](https://img.youtube.com/vi/GFw3J3Jbuas/mqdefault.jpg)](https://www.youtube.com/watch?v=GFw3J3Jbuas)