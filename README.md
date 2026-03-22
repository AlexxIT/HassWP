# Home Assistant Windows Portable (HassWP)

![](https://img.shields.io/github/stars/AlexxIT/HassWP?style=flat-square&logo=github) 
![](https://img.shields.io/github/downloads/AlexxIT/HassWP/total?color=blue&style=flat-square&logo=github)  

Portable version of Home Assistant for Windows.

**ATTENTION:** Direct works on Windows is **not maintained by the core developers** of Home Assistant. So some components/integrations may not work at all. No need to ask me or the core authors to fix it. If something you need doesn't work - use [virtualization](https://www.home-assistant.io/installation/windows).

Preinstalled:

- [WinPython](https://winpython.github.io/) v3.14.2 64-bit
- [Home Assistant](https://www.home-assistant.io/) v2026.3.3
- [NotePad++](https://notepad-plus-plus.org/) v7.8.5 32bit
- [HACS](https://hacs.xyz/) v2.0.5

## HOWTO

1. Download [HassWP_XXXX.XX.X.zip](https://github.com/AlexxIT/HassWP/releases/latest)
2. Unpack
3. Run

Useful files:

- `hass.cmd` - run Home Assistant and default Browser
- `notepad.cmd` - run NotePad with `configuration.yaml`
- `web.url` - open default Browser with http://localhost:8123/
- `config/reset.cmd` - reset Home Assistant but don't touch config files

## Supervisor and Addons

HassWP **don't have and can't have supervisor** and any Hass.io addons. Supervisor can be installed only over Docker. Nativelly Docker works only on Linux core. In any other OS it will use virtualization.

If you really needs Hass.io addons on Windows - use [virtualization](https://www.home-assistant.io/installation/windows).

## Move config

You can transfer your configuration to another Hass installation at any time. In another HassWP, venv, docker, hass.io, etc. Windows or Linux, it doesn't matter. Just move the contents of the `config` folder to a new location. Remember about `config/.storage` folder, it is also important.

Before any movement - stop the old and new Home Assistant!

## Video Demo

[![Home Assistant Windows Portable (HassWP)](https://img.youtube.com/vi/GFw3J3Jbuas/mqdefault.jpg)](https://www.youtube.com/watch?v=GFw3J3Jbuas)

## Do it yourself

1. Download and unpack `WinpythonXX-3.XX.XX.0dot.exe`
2. Run from command line:

```
scripts\env.bat
python -m pip install homeassistant==XXXX.XX
pip install https://github.com/AlexxIT/HassWP/archive/master.zip
mkdir config
python -m hass_win -c config -v
```
