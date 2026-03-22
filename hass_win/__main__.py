import os
import subprocess
import sys

from homeassistant import __main__ as hass, requirements
from homeassistant.const import MAJOR_VERSION, MINOR_VERSION


def run_forever():
    """Run a simple daemon runner process on Windows to handle restarts."""
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
            if exc.returncode != hass.RESTART_EXIT_CODE:
                sys.exit(exc.returncode)


def install_requirements(reqs: list[str]):
    # noinspection PyProtectedMember
    requirements._install_requirements_if_missing(reqs, requirements.pip_kwargs(None))


if __name__ == "__main__":
    if "--runner" not in sys.argv:
        run_forever()

    # runner arg supported only on old Hass versions
    sys.argv.remove("--runner")

    assert sys.flags.utf8_mode, "env PYTHONUTF8=1 should be set"

    install_requirements(["colorlog"])

    if (MAJOR_VERSION, MINOR_VERSION) >= (2026, 3):
        from hass_2026_3 import main
    elif (MAJOR_VERSION, MINOR_VERSION) >= (2025, 2):
        from hass_2025_2 import main
    elif (MAJOR_VERSION, MINOR_VERSION) >= (2024, 4):
        from hass_2024_4 import main
    elif (MAJOR_VERSION, MINOR_VERSION) >= (2023, 2):
        from hass_2023_2 import main

    main()

    sys.exit(hass.main())
