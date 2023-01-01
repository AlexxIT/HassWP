from distutils.core import setup

setup(
    name="hass_win",
    version="2012.12.8",
    description="Windows runner for Home Assistant",
    author="AlexxIT",
    install_requires=["homeassistant", "colorlog"],
    packages=["hass_win"],
    package_data={"hass_win": ["*.dll"]},
)
