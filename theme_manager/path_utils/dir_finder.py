"""Finds directories."""

import os
from pathlib import Path

from . import xdg_finder
from .. import logging_utils


def on_list_of_paths(target: str, paths: list[Path]) -> list[Path]:
    """Looks for `target` on `paths`. """
    logger = logging_utils.get()
    logger.debug(f'Searching for {target} on {paths}.', __name__)

    ret_value = list()
    for directory in paths:
        if target in os.listdir(directory):
            logger.debug(f'Found {target} on {directory.absolute()}.', __name__)
            ret_value.append(Path(directory, target).absolute())
    
    logger.debug(f'Returning {ret_value}.', __name__)


def on_xdg_configuration_paths(target: str) -> list[Path]:
    """Looks for `target` on $XDG_DATA_DIRS and $XDG_CONFIG_HOME. """
    logger = logging_utils.get()
    
    xdg_combined = xdg_finder.get_xdg_data_dirs()
    xdg_combined.append(xdg_finder.get_xdg_config_home())
    logger.debug(f'Searching for {target} on {xdg_combined}.', __name__)
    
    ret_value = list()
    for directory in xdg_combined:
        try:
            if not directory.exists():
                logger.warn(f'{directory.absolute()} is listed as a XDG data directory but doesn\'t exist. This might be unintentional.')
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
