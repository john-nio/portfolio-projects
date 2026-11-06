"""download_data.py — fetch Bike Share ridership zips via the City's open data API.

Usage: python3 download_data.py 2024
"""

import json
import sys
import zipfile
from pathlib import Path

import requests

METADATA = Path("data_source/ckan_metadata_2026-11-05.json")
DATA_DIR = Path("data_source")


def find_resource(metadata: dict, year: int) -> dict:
    """Return the resource dict for bikeshare-ridership-<year>.zip."""
    for r in metadata["result"]["resources"]:
        print(r["name"])
        if r["name"] == f"bikeshare-ridership-{year}.zip":
            return r
    raise ValueError(f"no resource for {year}")
