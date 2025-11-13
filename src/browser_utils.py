"""
Launch Chrome browser instance
"""

import logging
import shlex
import subprocess
from pathlib import Path


log = logging.getLogger(__name__)


def launch_chrome(chrome_path: str, user_data_dir: str, port: int = 9222) -> None:
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
