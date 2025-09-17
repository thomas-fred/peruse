"""
Try and read the contents of data file paths passed from command line, then
open a Python prompt.
"""

import logging
import os
import string
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Callable

from peruse.readers import delayed_reader, read_json, read_text, read_toml, read_yaml

MAX_FILE_READS = 2**8

EXTENSION_READER: dict[str, Callable] = {
    ".csv": delayed_reader("pandas", "read_csv", alias="pd"),
    ".geojson": delayed_reader("geopandas", "read_file", alias="gpd"),
    ".geoparquet": delayed_reader("geopandas", "read_parquet", alias="gpd"),
    ".gpkg": delayed_reader("geopandas", "read_file", alias="gpd"),
    ".gpq": delayed_reader("geopandas", "read_parquet", alias="gpd"),
    ".jpg": delayed_reader("matplotlib.image", "imread"),
    ".jpeg": delayed_reader("matplotlib.image", "imread"),
    ".json": read_json,
    ".log": read_text,
    ".parq": delayed_reader("pandas", "read_parquet", alias="pd"),
    ".parquet": delayed_reader("pandas", "read_parquet", alias="pd"),
    ".pq": delayed_reader("pandas", "read_parquet", alias="pd"),
    ".nc": delayed_reader("xarray", "open_dataset", alias="xr"),
    ".m": delayed_reader("scipy.io", "loadmat"),
    ".md": read_text,
    ".mat": delayed_reader("scipy.io", "loadmat"),
    ".png": delayed_reader("matplotlib.image", "imread"),
    ".shp": delayed_reader("geopandas", "read_file", alias="gpd"),
    ".tif": delayed_reader("xarray", "open_dataset", alias="xr"),
    ".tiff": delayed_reader("xarray", "open_dataset", alias="xr"),
    ".toml": read_toml,
    ".txt": read_text,
    ".xlsx": delayed_reader("pandas", "read_excel", alias="pd"),
    ".yaml": read_yaml,
    ".yml": read_yaml,
    ".zarr": delayed_reader("xarray", "open_zarr", alias="xr"),
}


def string_refs(count: int) -> list[str]:
    """Generate the Excel column name sequence to use as short file references."""
    alpha: str = string.ascii_lowercase
    refs: list[str] = []
    while len(refs) < count:
        floor: int = len(refs) // 26
        mod: int = len(refs) % 26
        if floor < 1:
            refs.append(alpha[mod])
        else:
            refs.append(f"{alpha[floor - 1]}{alpha[mod]}")
    return refs


def read(paths: list[str]) -> tuple[SimpleNamespace, SimpleNamespace]:
    """
    Try and read the contents of each path.

    Return objects containing the paths, `p` and deserialised data `x`, with
    short string references (e.g. "a", "b", ..., "z", "aa", "ab", ...) as
    attribute names for retrieval.
    """
    x = SimpleNamespace()
    p = SimpleNamespace()
    for i, (ref, path) in enumerate(zip(string_refs(len(paths)), paths)):

        setattr(p, ref, path)
        setattr(x, ref, None)

        if not path.exists():
            logging.info(f"Couldn't find {path} from {os.getcwd()}")
            continue

        if path.is_dir():
            logging.info(f"{path} is a directory, skipping")
            continue

        try:
            reader: Callable = EXTENSION_READER[path.suffix.lower()]
        except KeyError:
            logging.info(f"Don't know how to open {path.suffix.lower() or '?'} files")
            continue

        try:
            setattr(x, ref, reader(path))
        except Exception as error:
            logging.info(error)
            continue

        logging.info(f"x.{ref} = {path}")

    return p, x


if __name__ == "__main__":

    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

    _, *paths = sys.argv

    if not paths:
        raise ValueError("Require at least one path to try and open")
    elif len(paths) > MAX_FILE_READS:
        raise ValueError(f"Cannot read more than {MAX_FILE_READS} files")
    else:
        p, x = read([Path(path) for path in paths])

