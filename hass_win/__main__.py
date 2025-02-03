import logging
import os
import platform
import subprocess
import sys
import warnings

from aiohttp import resolver
from homeassistant import __main__, requirements, setup
from homeassistant.helpers import signal
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

    # runner arg supported only on old Hass versions
    sys.argv.remove("--runner")

    assert sys.flags.utf8_mode, "env PYTHONUTF8=1 should be set"


def install_requirements(hass, reqs):
    requirements._install_requirements_if_missing(
        reqs, requirements.pip_kwargs(hass.config.config_dir)
    )


def wrap_integration_init(func):
    def wrap(self, hass, pkg_path, file_path, manifest, *args):
        if manifest["domain"] == "homeassistant":
            # set config directory as cwd (useful for camera snapshot)
            os.chdir(hass.config.config_dir)
            # and adds it to PATH (useful for ffmpeg)
            os.environ["PATH"] += ";" + hass.config.config_dir

        elif manifest["domain"] == "camera":
            install_requirements(hass, manifest["requirements"])

            # fix PyTurboJPEG for camera and stream
            from turbojpeg import DEFAULT_LIB_PATHS

            arch = platform.architecture()[0][:2]  # 32 or 64
            # downloaded from: https://pypi.org/project/PyTurboJPEG/
            DEFAULT_LIB_PATHS["Windows"].append(
                os.path.dirname(__file__) + f"\\turbojpeg-{arch}.dll"
            )

        elif manifest["domain"] == "bluetooth":
            install_requirements(hass, manifest["requirements"])

            import bluetooth_adapters
            from bluetooth_adapters import dbus

            bluetooth_adapters.get_dbus_managed_objects = dbus.get_dbus_managed_objects

            from bleak.backends.winrt.client import BleakClientWinRT

            def wrap_bleak_winrt(func):
                def wrap(self, address_or_ble_device, **kwargs):
                    kwargs.setdefault("winrt", {})
                    return func(self, address_or_ble_device, **kwargs)

                return wrap

            BleakClientWinRT.__init__ = wrap_bleak_winrt(BleakClientWinRT.__init__)

        elif manifest["domain"] == "assist_pipeline":
            manifest["requirements"] = []
            sys.modules["pymicro_vad"] = type("", (), {"MicroVad": None})()
            sys.modules["pyspeex_noise"] = type("", (), {"AudioProcessor": None})()

        return func(self, hass, pkg_path, file_path, manifest, *args)

    return wrap


def wrap_on_setup(func):
    async def wrapper(hass, domain, config):
        if domain in ("dhcp", "radio_browser"):
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


# fix Hass 2022.2: Home Assistant only supports Linux, OSX and Windows using WSL
__main__.validate_os = lambda: None  # Hass v2022.2+

# move dependencies to main python libs folder
package.is_virtual_env = lambda: True

# fix: module 'os' has no attribute 'fchmod'. Did you mean: 'chmod'?
os.fchmod = lambda *args: None

# fix: raise NotImplementedError
signal.async_register_signal_handling = lambda *args: None

# fix Hass 2024.9: aiodns needs a SelectorEventLoop on Windows
resolver.AsyncResolver = resolver.ThreadedResolver

# fix before import requirements
Integration.__init__ = wrap_integration_init(Integration.__init__)

# fixes on components setup
setup.async_setup_component = wrap_on_setup(setup.async_setup_component)

# fix "site-packages\miio\miot_device.py:23: FutureWarning: functools.partial..."
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    try:
        # optional color logs
        from colorlog import ColoredFormatter
    except ModuleNotFoundError:
        pass

    sys.exit(__main__.main())
