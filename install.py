"""
- [x] Python 3.10.11 amd64 / Home Assistant 2023.2.5
- [x] Python 3.11.9  amd64 / Home Assistant 2023.8.4
- [x] Python 3.12.10 amd64 / Home Assistant 2024.4.4
- [x] Python 3.13.12 amd64 / Home Assistant 2025.2.5
- [x] Python 3.14.8  arm64 / Home Assistant 2026.3.4
- [x] Python 3.14.8  arm64 / Home Assistant 2026.10.2
"""

import subprocess
import sys

if len(sys.argv) < 2:
    packages = subprocess.check_output(["uv", "pip", "freeze"], text=True).splitlines()
    if packages:
        subprocess.run(["uv", "pip", "uninstall", *packages], check=True)
    exit(0)

version = sys.argv[1]
major, minor, patch = [int(i) for i in version.split(".")]

# Check Home Assistant and minimal python version
if (major, minor) >= (2026, 3):
    assert sys.version_info >= (3, 14, 2)
elif (major, minor) >= (2025, 2):
    assert sys.version_info >= (3, 13)
elif (major, minor) >= (2024, 4):
    assert sys.version_info >= (3, 12)
elif (major, minor) >= (2023, 8):
    assert sys.version_info >= (3, 11)
elif (major, minor) >= (2023, 2):
    assert sys.version_info >= (3, 10)

args = [
    "uv",
    "pip",
    "install",
    "--find-links",
    "https://alexxit.github.io/python-wheels/",
]

if major == 2026:
    # Fix first start for serialx
    args.append("pywin32")

elif major == 2023:
    # ModuleNotFoundError: No module named 'pkg_resources'
    args.append("setuptools==78.1.1")  # version from HA 2026.9.0

args += ["homeassistant==" + version]

print(" ".join(args))

subprocess.run(args, capture_output=False, text=True)
