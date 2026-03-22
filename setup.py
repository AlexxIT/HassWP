from distutils.core import setup

setup(
    name="hass_win",
    version="2026.3.3",
    description="Windows runner for Home Assistant",
    author="AlexxIT",
    install_requires=["homeassistant"],
    packages=["hass_win"],
    package_data={"hass_win": ["*.dll"]},
)
