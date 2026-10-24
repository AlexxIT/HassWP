"""
- [x] Python 3.14.7 amd64 / Home Assistant 2026.3.4
    - [x] Onbiarding
- [x] Python 3.14.7 amd64 / Home Assistant 2026.10.2
    - [x] Onbiarding
- [x] Python 3.14.8 arm64 / Home Assistant 2026.3.4
    - [x] Onbiarding
- [x] Python 3.14.8 arm64 / Home Assistant 2026.10.3
    - [x] Onbiarding
    - [x] Apple TV (install only)
    - [x] Bluetooth
    - [x] Google Cast
    - [x] Generic Camera
    - [x] Yamaha MusicCast
    - [x] Xiaomi BLE
    - [x] Xiaomi Home (install only)
    - [x] Yeelight
    - [x] ZHA over TCP (install only)
"""

import logging
import sys

from homeassistant.helpers import issue_registry

from hass_2023_2 import (
    fix_add_signal_handler,
    fix_bluetooth,
    fix_config_dir,
    fix_fcntl,
    fix_is_virtual_env,
    fix_setup_components,
    fix_turbojpeg,
    fix_validate_os,
    install_requirements,
    sys_module,
)
from hass_2024_4 import fix_assist_pipeline
from hass_2025_2 import (
    fix_aiodns,
    fix_aiohttp_fast_zlib,
    fix_dependencies,
    fix_tzdata,
    fix_uv_find_links,
)


def fix_resource():
    """Fix HA 2025.8: runner import resource."""
    # ModuleNotFoundError: No module named 'resource'
    sys_module("resource", getrlimit=lambda *args: (2048, 0), RLIMIT_NOFILE=0)


def fix_issue_registry():
    func = issue_registry.async_create_issue

    def wrapper(hass, domain, issue_id, **kwargs):
        if issue_id != "deprecated_method":
            func(hass, domain, issue_id, **kwargs)

    issue_registry.async_create_issue = wrapper


def check_win32():
    """Fix first start for serialx."""
    install_requirements(["pywin32"])
    try:
        import win32con
    except ModuleNotFoundError:
        logging.warning("pywin32 install require hass restart")
        sys.exit(100)  # call hass restart


def check_cffi_version():
    """Fix HA 2026.07.2: Fix first update of cffi library to 2.0.0."""
    install_requirements(["cffi"])  # version will be selected from constraints file

    import _cffi_backend
    import cffi

    # This may fail if cffi will be updated during run
    if _cffi_backend.__version__ != cffi.__version__:
        logging.warning("cffi version mismatch require hass restart")
        sys.exit(100)  # call hass restart


def main():
    # start-up locks
    fix_validate_os()
    fix_add_signal_handler()
    fix_fcntl()
    fix_resource()

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
    fix_aiohttp_fast_zlib()
    fix_tzdata()
    fix_dependencies()
    fix_uv_find_links()
    fix_issue_registry()

    check_cffi_version()
    check_win32()
