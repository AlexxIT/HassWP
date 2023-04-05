"""
Run Home Assistant natively in Windows. Tested with:

Version 1:

- Windows 10 x64 (19044.1466)
- Python 3.9.10 x64
- Home Assistant 2022.2.0 (default_config)

Version 2:

- Windows 7 x64
- WinPython v3.8.9 x32
- Home Assistant 2021.12.10 (default_config)
"""
import logging
import mimetypes
import os
import platform
import socket
import subprocess
import sys
from logging import FileHandler
from logging.handlers import BaseRotatingHandler
from types import ModuleType

# noinspection PyPackageRequirements
from atomicwrites import AtomicWriter
from colorlog import ColoredFormatter
from homeassistant import __main__, const, setup
from homeassistant.helpers import frame, signal
from homeassistant.loader import Integration
from homeassistant.util import package

if __name__ == "__main__":
    if "--runner" not in sys.argv:
        # Run a simple daemon runner process on Windows to handle restarts
        if sys.argv[0].endswith(".py"):
            sys.argv.insert(0, "python")

        sys.argv.append("--runner")

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


def wrap_log(func):
    def wrap(*args, **kwargs):
        kwargs.pop("datefmt", None)
        return func(*args, **kwargs)

    return wrap


def wrap_utf8(func):
    def wrap(*args, **kwargs):
        if len(args) == 5:
            return func(args[0], args[1], args[2], args[3] or "utf-8", args[4])
        kwargs["encoding"] = "utf-8"
        return func(*args, **kwargs)

    return wrap


def wrap_before_pip(func):
    def wrap(self, hass, pkg_path, file_path, manifest):
        if manifest["domain"] == "cast":
            if (const.MAJOR_VERSION, const.MINOR_VERSION) >= (2022, 12):
                manifest["requirements"] = ["pychromecast==12.1.4"]
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
                subprocess.Popen(
                    [binary, "-version"], stdout=subprocess.DEVNULL
                )
            except Exception:
                logging.getLogger(__name__).info("FFmpeg DISABLED!")
                return True

        return await func(hass, domain, config)

    return wrapper


def fix_requirements(requirements: list):
    for req in requirements:
        req = req.split("==")[0].lower()
        if req == "pyturbojpeg":
            # fix PyTurboJPEG for camera and stream
            from turbojpeg import DEFAULT_LIB_PATHS
            # downloaded from: https://pypi.org/project/PyTurboJPEG/
            DEFAULT_LIB_PATHS["Windows"].append(
                f"{os.path.dirname(__file__)}\\turbojpeg-{ARCH}.dll"
            )

        elif req == "pyserial":
            # fix socket for ZHA
            # noinspection PyPackageRequirements
            from serial.urlhandler import protocol_socket

            class Serial(protocol_socket.Serial):
                out_waiting = 1

            protocol_socket.Serial = Serial


def wrap_after_pip(func):
    def wrapper(integration: Integration):
        # at this moment requirements already installed
        fix_requirements(integration.requirements)
        return func(integration)

    return wrapper


# fix timezone for Python 3.8
if not package.is_installed("tzdata"):
    package.install_package("tzdata")

ARCH = platform.architecture()[0][:2]  # 32 or 64

# remove python version warning
# noinspection PyFinal
const.REQUIRED_NEXT_PYTHON_HA_RELEASE = None

# adds msec to logger
ColoredFormatter.__init__ = wrap_log(ColoredFormatter.__init__)

# fix Windows encoding
AtomicWriter.__init__ = wrap_utf8(AtomicWriter.__init__)
FileHandler.__init__ = wrap_utf8(FileHandler.__init__)
BaseRotatingHandler.__init__ = wrap_utf8(BaseRotatingHandler.__init__)

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

if __name__ == "__main__":
    sys.exit(__main__.main())
