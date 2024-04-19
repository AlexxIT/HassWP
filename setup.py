from distutils.core import setup

setup(
    name="hass_win",
    version="2024.4.3",
    description="Windows runner for Home Assistant",
    author="AlexxIT",
    install_requires=[
        "homeassistant",
        "colorlog",  # optional color log
        "chacha20poly1305-reuseable==0.0.4",  # fix HomeKit support on after 2023.5
    ],
    packages=["hass_win"],
    package_data={"hass_win": ["*.dll"]},
)
