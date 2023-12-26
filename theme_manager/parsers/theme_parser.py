"""Based on a `theme.json` file, parses info about the installed themes."""

import os
import json
from pathlib import Path

from ..path_utils import dir_finder
from .. import logging_utils

def parse_themes() -> list:
    """Parses the available themes based on the existance of a valid `theme.json` file in the themes directory."""
    
    logger = logging_utils.get()

    themes_dirs = [Path(x, 'themes') for x in 
                   dir_finder.on_xdg_data('theme-manager')]
    logger.debug(f'Searching for themes on {themes_dirs}.', __name__)

    themes_data = list()  
    for themes_dir in themes_dirs:
        try:
            if not themes_dir.is_dir():
                logger.warn(f'{themes_dir} is not a directory, and might be unintentional. '
                            'Remove it and create a "themes" directory instead. ')
                continue
        except OSError:
            continue
        theme_dirs = [Path(x) for x in os.listdir(themes_dir)]
        # ...

def _validate_theme(theme_file: os.PathLike) -> bool:
    """Checks if the `theme.json` file is valid and describes a theme correctly."""
    # Do the manual first.