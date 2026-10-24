import logging
import os
import subprocess
import sys


def run_forever():
    """Run a simple daemon runner process on Windows to handle restarts."""
    if sys.argv[0].endswith(".py"):
        sys.argv.insert(0, sys.executable)

    sys.argv.append("--runner")

    while True:
        try:
            code = subprocess.call(sys.argv)
            if code != 100:  # RESTART_EXIT_CODE
                sys.exit(code)
        except KeyboardInterrupt:
            sys.exit(0)


def main() -> int:
    from homeassistant import __main__ as hass
    from homeassistant.const import MAJOR_VERSION, MINOR_VERSION

    # noinspection unsupported-operator
    if (MAJOR_VERSION, MINOR_VERSION) >= (2026, 3):
        from hass_2026_3 import main
    elif (MAJOR_VERSION, MINOR_VERSION) >= (2025, 2):
        from hass_2025_2 import main
    elif (MAJOR_VERSION, MINOR_VERSION) >= (2024, 4):
        from hass_2024_4 import main
    else:
        from hass_2023_2 import main

    main()

    return hass.main()


if __name__ == "__main__":
    if "--runner" not in sys.argv:
        run_forever()

    # runner arg supported only on old Hass versions
    sys.argv.remove("--runner")

    # https://docs.python.org/3/library/os.html#utf8-mode
    os.environ["PYTHONUTF8"] = "1"

    logging.basicConfig(level=logging.INFO)

    sys.exit(main())
