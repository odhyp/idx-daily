"""
Project constants
"""

import tomllib

with open("config.toml", "rb") as f:
    cfg = tomllib.load(f)


CHROME_DIR = cfg["base"]["chrome_dir"]
BASE_URL = cfg["base"]["base_url"]
