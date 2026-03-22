"""
- [x] Python 3.10.11 / Home Assistant 2023.2.5
- [x] Python 3.11.9  / Home Assistant 2023.8.4
"""

import os
import platform
import socket

from homeassistant import __main__, setup
from homeassistant.helpers import signal
from homeassistant.loader import Integration
from homeassistant.util import package

from hass_win.hass import (
    install_component_requirements,
    install_requirements,
    sys_module,
)


def fix_add_signal_handler():
    """Fix runner import core and call async_register_signal_handling: NotImplementedError."""
    signal.async_register_signal_handling = lambda *args: None


def fix_validate_os():
    """Fix HA 2022.2: Home Assistant only supports Linux, OSX and Windows using WSL."""
    __main__.validate_os = lambda: None


def fix_config_dir():
    func = Integration.__init__

    def wrapper(self, hass, pkg_path, file_path, manifest, *args):
        if manifest["domain"] == "homeassistant":
            # set config directory as cwd (useful for camera snapshot)
            os.chdir(hass.config.config_dir)
            # and adds it to PATH (useful for ffmpeg)
            os.environ["PATH"] += ";" + hass.config.config_dir
        return func(self, hass, pkg_path, file_path, manifest, *args)

    Integration.__init__ = wrapper


def fix_is_virtual_env():
    """Move deps to python folder."""
    package.is_virtual_env = lambda: True


# noinspection PyUnresolvedReferences,PyPackageRequirements
def fix_turbojpeg():
    """Fix PyTurboJPEG for camera and stream."""
    install_component_requirements("camera")

    from turbojpeg import DEFAULT_LIB_PATHS

    arch = platform.architecture()[0][:2]  # 32 or 64
    # downloaded from: https://pypi.org/project/PyTurboJPEG/
    DEFAULT_LIB_PATHS["Windows"].append(
        os.path.dirname(__file__) + f"\\turbojpeg-{arch}.dll"
    )


def fix_setup_components():
    func = setup.async_setup_component

    async def wrapper(hass, domain, config):
        # Fix dhcp - No libpcap provider available
        # Fix radio_browser - Could not connect to Radio Browser API
        if domain in ("dhcp", "radio_browser"):
            return True
        return await func(hass, domain, config)

    setup.async_setup_component = wrapper


# noinspection PyUnresolvedReferences,PyPackageRequirements
def fix_bluetooth():
    install_component_requirements("bluetooth")

    import bluetooth_adapters
    from bluetooth_adapters import dbus

    bluetooth_adapters.get_dbus_managed_objects = dbus.get_dbus_managed_objects

    from bleak.backends.winrt.client import BleakClientWinRT

    func = BleakClientWinRT.__init__

    def wrapper(self, address_or_ble_device, **kwargs):
        kwargs.setdefault("winrt", {})
        return func(self, address_or_ble_device, **kwargs)

    BleakClientWinRT.__init__ = wrapper


def fix_cast():
    func = Integration.__init__

    def wrapper(self, hass, pkg_path, file_path, manifest, *args):
        if manifest["domain"] == "cast":
            ver = manifest["requirements"][0]
            # fix bugs in libs
            if "pychromecast==13.0.1" <= ver <= "pychromecast==13.0.4":
                # HA 2022.11 / pychromecast==12.1.4 - OK
                # HA 2023.4  / pychromecast==13.0.7 - OK
                manifest["requirements"] = ["pychromecast==12.1.4"]
        return func(self, hass, pkg_path, file_path, manifest, *args)

    Integration.__init__ = wrapper


def fix_cloud():
    """Fix HA 2023.2: cloud"""
    # Fix component cloud -> hass-nabucasa==0.61.0 -> acme==1.31.0 -> josepy>=1.13.0
    # AttributeError: module 'josepy' has no attribute 'ComparableX509'
    install_requirements(["josepy==1.13.0"])


def fix_fcntl():
    sys_module(
        "fcntl",  # HA 2022.9 bluetooth
        ioctl=None,  # HA 2023.3
        flock=lambda *args: None,  # HA 2025.10?
        LOCK_EX=0,  # HA 2025.10?
        LOCK_NB=0,  # HA 2025.10?
    )


def fix_os_fchmod():
    # Fix homeassistant\helpers\storage.py -> homeassistant\util\file.py
    # AttributeError: module 'os' has no attribute 'fchmod'
    os.fchmod = lambda *args: None


def fix_socket():
    """Fix HA 2022.12: bluetooth"""
    assert not hasattr(socket, "CMSG_LEN") and not hasattr(socket, "SCM_RIGHTS")

    socket.CMSG_LEN = lambda *args: None
    # noinspection PyFinal
    socket.SCM_RIGHTS = 0


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
    fix_bluetooth()
    fix_cast()
    fix_cloud()
    fix_fcntl()
    fix_os_fchmod()
    fix_socket()
