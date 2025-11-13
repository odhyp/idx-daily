"""
Project constants
"""

import tomllib

with open("config.toml", "rb") as f:
    cfg = tomllib.load(f)

APP_VERSION = "v0.0.1"
CHROME_DIR = cfg["base"]["chrome_dir"]
BASE_URL = cfg["base"]["base_url"]
