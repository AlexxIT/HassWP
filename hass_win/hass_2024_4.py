"""
- [x] Python 3.12.10 / Home Assistant 2024.4.4
"""

from homeassistant.loader import Integration

from hass_2023_2 import (
    fix_add_signal_handler,
    fix_bluetooth,
    fix_cloud,
    fix_config_dir,
    fix_is_virtual_env,
    fix_os_fchmod,
    fix_setup_components,
    fix_turbojpeg,
    fix_tzdata,
    fix_validate_os,
    install_component_requirements,
    install_requirements,
    sys_module,
)


def fix_assist_pipeline():
    # Fix HA 2026.3: mobile_app import cloud import assist_pipeline import pymicro_vad
    sys_module("pymicro_vad", MicroVad=lambda self: None)
    sys_module("pyspeex_noise", AudioProcessor=None)

    func = Integration.__init__

    def wrapper(self, hass, pkg_path, file_path, manifest, *args):
        if manifest["domain"] == "assist_pipeline":
            manifest["requirements"] = []
        func(self, hass, pkg_path, file_path, manifest, *args)

    Integration.__init__ = wrapper


def fix_yamaha_musiccast():
    """Fix HA 2024.4: Error occurred loading flow for integration yamaha_musiccast."""
    # ModuleNotFoundError: No module named 'pkg_resources'
    install_requirements(["setuptools==78.1.1"])


def fix_tts():
    """Fix HA 2024.4: ModuleNotFoundError: No module named 'mutagen'"""
    install_component_requirements("tts")


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
    fix_tzdata()
    fix_assist_pipeline()
    fix_bluetooth()
    fix_cloud()
    fix_os_fchmod()
    fix_yamaha_musiccast()
    fix_tts()
