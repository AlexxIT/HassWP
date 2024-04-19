import logging
import mimetypes
import os
import platform
import socket
import subprocess
import sys
from types import ModuleType

from homeassistant import __main__, const, setup
from homeassistant.helpers import frame, signal
from homeassistant.loader import Integration
from homeassistant.util import package

if __name__ == "__main__":
    if "--runner" not in sys.argv:
        # Run a simple daemon runner process on Windows to handle restarts
        if sys.argv[0].endswith(".py"):
            sys.argv.insert(0, sys.executable)

        sys.argv.append("--runner")

        # https://docs.python.org/3/library/os.html#utf8-mode
        os.environ["PYTHONUTF8"] = "1"

        while True:
            try:
                subprocess.check_call(sys.argv)
                sys.exit(0)
            except KeyboardInterrupt:
                sys.exit(0)
            except subprocess.CalledProcessError as exc:
                if exc.returncode != __main__.RESTART_EXIT_CODE:
                    sys.exit(exc.returncode)

    elif (const.MAJOR_VERSION, const.MINOR_VERSION) >= (2022, 2):
        # runner arg supported only on old Hass versions
        sys.argv.remove("--runner")

        assert sys.flags.utf8_mode, "env PYTHONUTF8=1 should be set"


def wrap_before_pip(func):
    def wrap(self, hass, pkg_path, file_path, manifest):
        if manifest["domain"] == "assist_pipeline":
            manifest["requirements"] = [
                i
                for i in manifest["requirements"]
                if not i.startswith("webrtc-noise-gain")
            ]
        # if manifest["domain"] == "cast":
        #     if (const.MAJOR_VERSION, const.MINOR_VERSION) >= (2022, 12):
        #         manifest["requirements"] = ["pychromecast==12.1.4"]
        return func(self, hass, pkg_path, file_path, manifest)

    return wrap


def wrap_on_setup(func):
    async def wrapper(hass, domain, config):
        if domain == "homeassistant":
            # set config directory as cwd (useful for camera snapshot)
            os.chdir(hass.config.config_dir)
            # and adds it to PATH (useful for ffmpeg)
            os.environ["PATH"] += ";" + hass.config.config_dir
        elif domain in ("dhcp", "radio_browser"):
            return True
        elif domain == "ffmpeg":
            try:
                binary = config.get(domain).get(domain + "_bin", domain)
                subprocess.Popen([binary, "-version"], stdout=subprocess.DEVNULL)
            except Exception:
                logging.getLogger(__name__).info("FFmpeg DISABLED!")
                return True

        return await func(hass, domain, config)

    return wrapper


def wrap_bleak_winrt(func):
    def wrap(self, address_or_ble_device, **kwargs):
        kwargs.setdefault("winrt", {})
        return func(self, address_or_ble_device, **kwargs)

    return wrap


def fix_requirements(requirements: list):
    for req in requirements:
        req = req.split("==")[0].lower()
        if req == "pyturbojpeg":
            # fix PyTurboJPEG for camera and stream
            from turbojpeg import DEFAULT_LIB_PATHS

            # downloaded from: https://pypi.org/project/PyTurboJPEG/
            DEFAULT_LIB_PATHS["Windows"].append(
                os.path.dirname(__file__) + f"\\turbojpeg-{ARCH}.dll"
            )

        elif req == "pyserial":
            # fix socket for ZHA
            # noinspection PyPackageRequirements
            from serial.urlhandler import protocol_socket

            class Serial(protocol_socket.Serial):
                out_waiting = 1

            protocol_socket.Serial = Serial

        elif req == "bluetooth-adapters":
            import bluetooth_adapters
            from bluetooth_adapters import dbus

            bluetooth_adapters.get_dbus_managed_objects = dbus.get_dbus_managed_objects

        elif req == "bleak":
            from bleak.backends.winrt.client import BleakClientWinRT

            BleakClientWinRT.__init__ = wrap_bleak_winrt(BleakClientWinRT.__init__)


def wrap_after_pip(func):
    def wrapper(integration: Integration):
        # at this moment requirements already installed
        fix_requirements(integration.requirements)
        return func(integration)

    return wrapper


def wrap_chmod(func):
    def wrapper(path: str, mode, **kwargs):
        if path.endswith(".state"):
            return
        return func(path, mode, **kwargs)

    return wrapper


# fix timezone for Python 3.8
if not package.is_installed("tzdata"):
    package.install_package("tzdata")

ARCH = platform.architecture()[0][:2]  # 32 or 64

# remove python version warning
# noinspection PyFinal
const.REQUIRED_NEXT_PYTHON_HA_RELEASE = None

# fix mimetypes for borked Windows machines
# https://github.com/home-assistant/core/commit/64bcd6097457b0c56528425a6a6ce00a2bce791c
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")

# fix Windows dependes core bugs
__main__.validate_os = lambda: None  # Hass v2022.2+
os.fchmod = lambda *args: None
signal.async_register_signal_handling = lambda *args: None

# fix before import requirements
Integration.__init__ = wrap_before_pip(Integration.__init__)
# fixes after import requirements
Integration.get_component = wrap_after_pip(Integration.get_component)
# fixes on components setup
setup.async_setup_component = wrap_on_setup(setup.async_setup_component)

# move dependencies to main python libs folder
package.is_virtual_env = lambda: True

# fix bluetooth for Hass v2022.9+
sys.modules["fcntl"] = ModuleType("")
setattr(sys.modules["fcntl"], "ioctl", None)

# fix bluetooth for Hass v2022.12+
socket.CMSG_LEN = lambda *args: None
socket.SCM_RIGHTS = 0

# fix Chromecast warning in logs (async_setup_platforms)
frame.report = lambda *args, **kwargs: None

# fix opus library for VOIP integration
os.environ["PATH"] += ";" + os.path.dirname(__file__)

# fix homekit bridge
os.chmod = wrap_chmod(os.chmod)

if __name__ == "__main__":
    try:
        # optional color logs
        from colorlog import ColoredFormatter
    except ModuleNotFoundError:
        pass

    sys.exit(__main__.main())
