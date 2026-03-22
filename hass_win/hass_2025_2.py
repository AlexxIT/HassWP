"""
- [x] Python 3.13.12 / Home Assistant 2025.2.5
"""
import inspect
import warnings

from homeassistant.util import loop

from hass_win.hass import install_component_requirements
from hass_win.hass_2023_2 import (
    fix_add_signal_handler,
    fix_bluetooth,
    fix_config_dir,
    fix_is_virtual_env,
    fix_setup_components,
    fix_turbojpeg,
    fix_validate_os,
)
from hass_win.hass_2024_4 import fix_assist_pipeline, fix_yamaha_musiccast


# noinspection PyPackageRequirements
def fix_aiodns():
    """Fix HA 2024.9: RuntimeError: aiodns needs a SelectorEventLoop on Windows."""
    from aiohttp import resolver

    resolver.AsyncResolver = resolver.ThreadedResolver


def fix_isal():
    """Fix HA 2024.6: aiohttp_fast_zlib."""
    # zlib_ng and isal are not available, falling back to zlib, performance will be degraded.
    install_component_requirements("isal")


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


def main():
    # start-up locks
    fix_add_signal_handler()
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
    fix_miio_warning()
    fix_tzdata()
    fix_yamaha_musiccast()
