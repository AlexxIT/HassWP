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
import os
import subprocess
import sys

from homeassistant import __main__, requirements, setup
from homeassistant.helpers import signal
from homeassistant.util import dt

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

elif __main__.REQUIRED_PYTHON_VER >= (3, 9, 0):
    # runner arg supported only on old Hass versions
    sys.argv.remove("--runner")


def wrap_requirements(func):
    async def wrapper(hass, name, requirements):
        result = await func(hass, name, requirements)

        if name == "zha":
            from serial.urlhandler import protocol_socket

            class Serial(protocol_socket.Serial):
                out_waiting = 1

            protocol_socket.Serial = Serial

        return result

    return wrapper


def wrap_setup(func):
    async def wrapper(hass, domain, config):
        if domain in ("dhcp", "ffmpeg"):
            return True

        return await func(hass, domain, config)

    return wrapper


# fix Windows depended core bugs
__main__.validate_os = lambda: None
dt.get_time_zone = lambda _: dt.DEFAULT_TIME_ZONE
os.fchmod = lambda *args: None
signal.async_register_signal_handling = lambda *args: None

# fix socket for ZHA
requirements.async_process_requirements = \
    wrap_requirements(requirements.async_process_requirements)
# fix DHCP and FFmpeg components bugs
setup.async_setup_component = wrap_setup(setup.async_setup_component)

# run hass
sys.exit(__main__.main())
