"""
- [x] Python 3.14.3 / Home Assistant 2026.3.3
    - [x] Onbiarding
    - [x] Apple TV
    - [x] Bluetooth
    - [x] Cast
    - [x] Generic Camera
    - [x] MusicCast
    - [x] Xiaomi BLE
    - [x] Xiaomi Home
    - [x] Yeelight
    - [x] ZHA over TCP
"""

import inspect

from homeassistant.util import package

from hass_win.hass import sys_module
from hass_win.hass_2023_2 import (
    fix_add_signal_handler,
    fix_bluetooth,
    fix_config_dir,
    fix_fcntl,
    fix_setup_components,
    fix_turbojpeg,
    fix_validate_os,
)
from hass_win.hass_2024_4 import fix_assist_pipeline
from hass_win.hass_2025_2 import fix_aiodns, fix_isal, fix_tzdata

def fix_resource():
    """Fix HA 2025.8: runner import resource."""
    sys_module("resource", getrlimit=lambda *args: (2048, 0), RLIMIT_NOFILE=0)


def fix_is_virtual_env():
    """Move deps to python folder. Fix Hass 2025.12: Core installation deprecated."""

    def wrapper() -> bool:
        if any(i.function == "_async_check_deprecation" for i in inspect.stack()):
            return False
        return True

    package.is_virtual_env = wrapper


def main():
    # start-up locks
    fix_add_signal_handler()
    fix_fcntl()
    fix_resource()
    fix_validate_os()

    # user-friendliness
    fix_config_dir()
    fix_is_virtual_env()
    fix_turbojpeg()

    # unsupported components
    fix_setup_components()

    # other errors
    fix_aiodns()
    fix_assist_pipeline()
    fix_bluetooth()
    fix_isal()
    fix_tzdata()
