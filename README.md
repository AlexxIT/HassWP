# Home Assistant Windows Portable (HassWP)

![](https://img.shields.io/github/stars/AlexxIT/HassWP?style=flat-square&logo=github) 
![](https://img.shields.io/github/downloads/AlexxIT/HassWP/total?color=blue&style=flat-square&logo=github)  

Portable version of Home Assistant for Windows.

**ATTENTION:** Direct works on Windows is **not maintained by the core developers** of Home Assistant. So some components/integrations may not work at all. No need to ask me or the core authors to fix it. If something you need doesn't work - use [virtualization](https://www.home-assistant.io/installation/windows).

Preinstalled:

- [WinPython](https://winpython.github.io/) v3.10.9 64-bit
- [Home Assistant](https://www.home-assistant.io/) v2023.3.6
- [HACS](https://hacs.xyz/) v1.31.0
- [SonoffLAN](https://github.com/AlexxIT/SonoffLAN) v3.5.1
- [XiaomiGateway3](https://github.com/AlexxIT/XiaomiGateway3) v3.1.0
- [WebRTC](https://github.com/AlexxIT/WebRTC) v3.1.0
- [YandexStation](https://github.com/AlexxIT/YandexStation) v3.12.1
- [StartTime](https://github.com/AlexxIT/StartTime) v1.1.6
- [NotePad++](https://notepad-plus-plus.org/) v7.8.5 32bit

## HOWTO

1. Download [HassWP_XXXX.XX.X.zip](https://github.com/AlexxIT/HassWP/releases/latest)
2. Unpack
3. Run

Useful files:

- `hass.cmd` - run Home Assistant and default Browser
- `notepad.cmd` - run NotePad with `configuration.yaml`
- `web.url` - open default Browser with http://localhost:8123/
- `config/reset.cmd` - reset Home Assistant but don't touch config files

## Windows 7 or 32-bit

Latest HassWP versions are build for Windows 8+ 64-bit.

If you want the Windows 7 version or 32-bit support - download [Hass v2021.12.10](https://github.com/AlexxIT/HassWP/releases/tag/v2022.5.3). This is because `Hass 2021.12.10` is the last Hass with `Python 3.8` support. And `Python 3.8` it the last Python with `Windows 7` support.

## Supervisor and Addons

HassWP **don't have and can't have supervisor** and any Hass.io addons. Supervisor can be installed only over Docker. Nativelly Docker works only on Linux core. In any other OS it will use virtualization.

If you really needs Hass.io addons on Windows - use [virtualization](https://www.home-assistant.io/installation/windows).

## Cameras

Latest HassWP supports [cameras stream](https://www.home-assistant.io/integrations/camera/). For snapshot and recording use relative path from your `config` folder - `media\snapshot.jpeg` or `www\video.mp4`.

[Generic camera](https://www.home-assistant.io/integrations/generic/) and [WebRTC](https://github.com/AlexxIT/WebRTC) integrations do not need ffmpeg in your system. But it you want use [FFmpeg](https://www.home-assistant.io/integrations/ffmpeg/) integration - [download ffmpeg](https://ffmpeg.org/download.html) manually and put `ffmpeg.exe` (80-120 MB) to your config folder.

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
