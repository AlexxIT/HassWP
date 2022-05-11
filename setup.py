from distutils.core import setup

setup(
    name="Hass Win",
    version="0.1.0",
    description="Windows Runner for Home Assistant",
    author="AlexxIT",
    install_requires=["homeassistant"],
    packages=["hass_win"]
)
