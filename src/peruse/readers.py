import importlib
import json
from pathlib import Path
from typing import Callable

import yaml


def delayed_reader(module_name: str, func_name: str, alias: str | None = None) -> Callable:
    """
    Return a function that lazily imports the required module `module_name` and
    calls `func_name` from that module.

    Make the required module available as `alias` if given, otherwise
    use `module_name`.

    The rationale for this function is to only spend time importing modules if
    they're required by an input file provided to __main__.
    """
    def reader(path: Path, *args, **kwargs):
        module = importlib.import_module(module_name)
        globals()[alias or module_name] = module
        func = getattr(module, func_name)
        return func(path, *args, **kwargs)
    return reader


def read_json(path: Path) -> dict:
    with open(path, "r") as fp:
        return json.load(fp)


def read_text(path: Path) -> list[str]:
    with open(path, "r") as fp:
        return fp.readlines()


def read_yaml(path: Path) -> dict:
    with open(path, "r") as fp:
        return yaml.safe_load(fp)

