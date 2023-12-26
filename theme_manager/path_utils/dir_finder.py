"""Finds directories. Exists basically to avoid `pyxdg` dependency."""

import os
from pathlib import Path

from .. import logging_utils

_HOME_DIR = Path(os.path.expanduser('~'))

def on_xdg_data(target: str) -> list[Path]:
    """Looks for `target` on $XDG_DATA_DIRS and $XDG_CONFIG_HOME. """
    logger = logging_utils.get()
    
    xdg_combined = _get_xdg_data_dirs()
    xdg_combined.append(_get_xdg_config_home())
    logger.debug(f'Searching for {target} on {xdg_combined}.', __name__)
    
    ret_value = list()
    for directory in xdg_combined:
        try:
            if not directory.is_dir():
                logger.warn(f'{directory.absolute()} is listed as a XDG data directory but isn\'t a directory. This might be unintentional.')
                continue
        except OSError:
            continue
        if target in os.listdir(directory):
            logger.debug(f'Found {target} on {directory.absolute()}.', __name__)
            ret_value.append(Path(directory, target).absolute())

    logger.debug(f'Returning {ret_value}.', __name__)
    return ret_value


def _get_xdg_config_home() -> Path:
    default = Path(os.path.expanduser('~'), '.config')
    return Path(os.getenv('XDG_CONFIG_HOME', 
                          default))


def _get_xdg_data_dirs() -> list[Path]:
    default = str(Path('/usr', 'local', 'share')) + ':' + str(Path('/usr', 'share'))
    return [Path(path) for path in os.getenv('XDG_DATA_DIRS', default).split(':')]
