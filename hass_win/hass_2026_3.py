"""
- [x] Python 3.14.7 amd64 / Home Assistant 2026.3.4
    - [x] Onbiarding
- [x] Python 3.14.7 amd64 / Home Assistant 2026.10.2
    - [x] Onbiarding
- [x] Python 3.14.8 arm64 / Home Assistant 2026.3.4
    - [x] Onbiarding
- [x] Python 3.14.8 arm64 / Home Assistant 2026.10.2
    - [x] Onbiarding
    - [ ] Apple TV
    - [ ] Bluetooth
    - [ ] Cast
    - [ ] Generic Camera
    - [ ] MusicCast
    - [ ] Xiaomi BLE
    - [ ] Xiaomi Home
    - [ ] Yeelight
    - [ ] ZHA over TCP
"""

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
