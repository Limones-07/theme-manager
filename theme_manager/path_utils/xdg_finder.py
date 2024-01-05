"""Finds the XDG directories. Exists basically to avoid `pyxdg` dependency."""

import os
from pathlib import Path

from .. import logging_utils

_HOME_DIR = Path(os.path.expanduser('~'))


def get_xdg_config_home() -> Path:
    logger = logging_utils.get()
    default = Path(_HOME_DIR, '.config')
    xdg_config_home = Path(os.getenv('XDG_CONFIG_HOME', default))
    logger.debug(f'The XDG config home is {xdg_config_home}', __name__)
    return xdg_config_home


def get_xdg_data_home() -> Path:
    logger = logging_utils.get()
    default = Path(_HOME_DIR, '.local', 'share')
    xdg_data_home = Path(os.getenv('XDG_DATA_HOME', default))
    logger.debug(f'The XDG data home is {xdg_data_home}', __name__)
    return xdg_data_home


def get_xdg_state_home() -> Path:
    logger = logging_utils.get()
    default = Path(_HOME_DIR, '.local', 'state')
    xdg_state_home = Path(os.getenv('XDG_STATE_HOME', default))
    logger.debug(f'The XDG state home is {xdg_state_home}', __name__)
    return xdg_state_home


def get_xdg_data_dirs() -> list[Path]:
    logger = logging_utils.get()
    default = str(Path('/usr', 'local', 'share')) + ':' + str(Path('/usr', 'share'))
    xdg_data_dirs = [Path(path) for path in os.getenv('XDG_DATA_DIRS', default).split(':')]
    logger.debug(f'The XDG data dirs are {xdg_data_dirs}', __name__)
    return xdg_data_dirs