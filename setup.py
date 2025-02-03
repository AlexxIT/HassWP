from distutils.core import setup

setup(
    name="hass_win",
    version="2025.1.4",
    description="Windows runner for Home Assistant",
    author="AlexxIT",
    install_requires=[
        "homeassistant",
        "colorlog",  # optional color log
    ],
    packages=["hass_win"],
    package_data={"hass_win": ["*.dll"]},
)
