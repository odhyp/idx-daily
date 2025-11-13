"""
Launch Chrome browser instance
"""

import logging
import shlex
import subprocess
from pathlib import Path


log = logging.getLogger(__name__)


def launch_chrome(chrome_path, user_data_dir, port: int = 9222):
    Path(user_data_dir).mkdir(exist_ok=True)
    cmd = f'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="{user_data_dir}"'

    try:
        subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        log.info("Chrome started on port %s with user data dir %s", port, user_data_dir)

    except FileNotFoundError:
        log.error("Chrome executable not found.")

    except Exception as e:
        log.error("Failed to run command: %s", e)
