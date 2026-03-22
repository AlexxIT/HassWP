import json
import os
import sys

from homeassistant import __main__, requirements


def sys_module(name: str, **kwargs):
    sys.modules[name] = type(name, (), kwargs)()


def install_requirements(reqs: list[str]):
    # noinspection PyProtectedMember
    requirements._install_requirements_if_missing(reqs, requirements.pip_kwargs(None))


def install_component_requirements(name: str):
    basedir = os.path.dirname(__main__.__file__)
    filename = f"{basedir}/components/{name}/manifest.json"
    with open(filename) as f:
        manifest = json.load(f)
    install_requirements(manifest["requirements"])
