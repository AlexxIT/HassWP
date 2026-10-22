"""
- [x] Python 3.13.12 / Home Assistant 2025.2.5
"""

import inspect
import os
import warnings

from homeassistant.util import loop

from hass_2023_2 import (
    fix_add_signal_handler,
    fix_bluetooth,
    fix_config_dir,
    fix_is_virtual_env,
    fix_setup_components,
    fix_turbojpeg,
    fix_validate_os,
    install_component_requirements,
    install_requirements,
)
from hass_2024_4 import fix_assist_pipeline


# noinspection PyPackageRequirements
def fix_aiodns():
    """Fix HA 2024.9: RuntimeError: aiodns needs a SelectorEventLoop on Windows."""
    from aiohttp import resolver

    resolver.AsyncResolver = resolver.ThreadedResolver


def fix_aiohttp_fast_zlib():
    """Fix HA 2024.6: aiohttp_fast_zlib."""
    # WARNING (MainThread) [aiohttp_fast_zlib] zlib_ng and isal are not available,
    # falling back to zlib, performance will be degraded.
    install_requirements(["zlib_ng==1.0.0"])


def fix_miio_warning():
    """Fix warning for miio package."""
    # FutureWarning: functools.partial will be a method descriptor in future Python versions
    warnings.filterwarnings("ignore")


def fix_tzdata():
    """Fix: onboarding - Detected blocking call to import_module..."""
    func = loop.raise_for_blocking_call

    def wrapper(*args, **kwargs):
        if any(i.function == "get_time_zone" for i in inspect.stack()):
            return
        func(*args, **kwargs)

    loop.raise_for_blocking_call = wrapper


def fix_dependencies():
    """
    Fix HA 2025.2: Important to install esphome dependencies, because:
      - aioesphomeapi==29.0.0 will install required version
      - bleak-esphome==2.7.0 will update it to latest and wrong version
    And on the next call, the correct version of aioesphomeapi will be installed.

    Fix HA 2026.3: Missing aioesphomeapi dependency in bluetooth module.
    """
    install_component_requirements("esphome")


def fix_uv_find_links():
    """Useful for arm64 architecture."""
    os.environ["UV_FIND_LINKS"] = "https://alexxit.github.io/python-wheels/"


def main():
    # start-up locks
    fix_validate_os()
    fix_add_signal_handler()

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
    fix_miio_warning()
    fix_tzdata()
    fix_dependencies()
    fix_uv_find_links()
