from distutils.core import setup

setup(
    name="hass_win",
    version="0.1.1",
    description="Windows runner for Home Assistant",
    author="AlexxIT",
    install_requires=["homeassistant", "colorlog"],
    packages=["hass_win"],
    package_data={"hass_win": ["*.dll"]},
)
