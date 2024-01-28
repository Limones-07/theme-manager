"""Defines the _PathHandler class."""

import os
from pathlib import Path

from . import logging_utils
from ..envs import EX_SOFTWARE

class _PathHandler():
    """Provides an API to interact with the paths theme-manager requires."""

    def __init__(self) -> None:
        """Loads all the necessary paths."""

        _logger.debug('Loading all necessary paths.', __name__)
        # Loads the theme-manager paths in order of priority
        self._theme_manager_paths = self._load_theme_manager_paths()

        # Loads the themes configuration paths (directory of each theme)
        self._themes_configuration_paths = self._load_theme_paths(self._theme_manager_paths)

        # Loads the application configurations paths (each application configuration, toml or json)
        self._applications_configuration_paths = self._load_app_paths(self._theme_manager_paths)

        # Loads the scripts paths (each script source code)
        self._scripts_paths = self._load_script_paths(self._theme_manager_paths)

        _logger.debug('Paths loaded.', __name__)

    def get_theme_manager_paths(self) -> list[Path]:
        """Returns a list with the theme-manager paths in order of priority."""

        return self._theme_manager_paths.copy()
    
    def get_themes_paths(self) -> list[Path]:
        """Returns a list with the paths to the directories of the installed themes in order of priority."""

        return self._themes_configuration_paths.copy()
    
    def get_applications_paths(self) -> list[Path]:
        """Returns a list with the paths to each application configuration file in order of priority."""

        return self._applications_configuration_paths.copy()

    def get_script_paths(self) -> list[Path]:
        """Returns a list with the paths to each script in order of priority."""

        return self._scripts_paths.copy()

    def _load_theme_manager_paths(self) -> list[Path]:
        """Loads the existing theme-manager directories."""

        # Return list
        ret_value = list()
        _logger.debug('Loading theme-manager\'s directories...', __name__)

        # Finds the XDG config home and the XDG data dirs
        try:
            xdg_config_home_tm_path = Path(os.getenv('XDG_CONFIG_HOME'), 'theme-manager')
            _logger.debug('Got the directory at the XDG config home from the environment variable. '
                          f'({xdg_config_home_tm_path})', __name__)
        except TypeError:
            xdg_config_home_tm_path = Path('~', '.config', 'theme-manager').expanduser()
            _logger.debug('Got the directory at the XDG config home from the default value. '
                          f'({xdg_config_home_tm_path})', __name__)
        if xdg_config_home_tm_path.exists():
            _logger.debug(f'{xdg_config_home_tm_path} exists. ', __name__)
            ret_value.append(xdg_config_home_tm_path)

        xdg_data_dirs: list[Path] = list()
        try:
            xdg_data_dirs.extend([Path(x) for x in os.getenv('XDG_DATA_DIRS').split(':')])
            _logger.debug('Got the XDG data directories from the environment variable. '
                          f'({xdg_data_dirs})', __name__)
        except (TypeError, AttributeError):
            xdg_data_dirs.extend([Path('/usr', 'local', 'share'), Path('/usr', 'share')])
            _logger.debug('Got the XDG data directories from the default value. '
                          f'({xdg_data_dirs})', __name__)
        for dir in xdg_data_dirs:
            theme_manager_path = Path(dir, 'theme-manager')
            if theme_manager_path.exists():
                _logger.debug(f'{theme_manager_path} exists. ', __name__)
                ret_value.append(theme_manager_path)
        
        _logger.debug(f'theme-manager directories in order of priority: {ret_value}', __name__)
        return ret_value

    def _load_theme_paths(self, theme_manager_paths: list[Path]) -> list[Path]:
        """Loads the paths of all the themes in order of priority."""

        # Return list
        ret_value = list()
        _logger.debug(f'Loading the theme paths from the directories {theme_manager_paths}...', __name__)

        # Iteration on every theme-manager directory
        for dir in theme_manager_paths:
            themes_dir = Path(dir, 'themes')
            if not themes_dir.exists():
                _logger.debug(f'{themes_dir} doesn\'t exist.', __name__)
                continue
            _logger.debug(f'Searching on {themes_dir}', __name__)
            # Iteration of every directory inside the themes directory
            for theme_dir in themes_dir.glob('*'):
                # Checks if theme_dir is actually a directory before proceeding
                if not theme_dir.is_dir():
                    continue
                theme_dir_contents = os.listdir(theme_dir)
                if 'theme.toml' in theme_dir_contents and 'theme.json' in theme_dir_contents:
                    _logger.warn('There are two configuration files for the theme at '
                                 f'{theme_dir}. Ignoring.')
                    continue
                elif not 'theme.toml' in theme_dir_contents and not 'theme.json' in theme_dir_contents:
                    continue
                _logger.debug(f'{theme_dir} contains a "theme.toml" or a "theme.json" file. '
                              'Including as a theme directory.', __name__)
                ret_value.append(theme_dir)
        
        _logger.debug(f'Theme directories in order of priority: {ret_value}', __name__)
        return ret_value
    
    def _load_app_paths(self, theme_manager_paths: list[Path]) -> list[Path]:
        """Loads the paths of the application configurations in order of priority."""

        # Return list
        ret_value = list()
        _logger.debug(f'Loading the applications paths from the directories {theme_manager_paths}', __name__)

        # Iterations on every theme-manager directory
        for dir in theme_manager_paths:
            applications_dir = Path(dir, 'applications')
            if not applications_dir.exists():
                _logger.debug(f'{applications_dir} doesn\'t exist.', __name__)
                continue
            _logger.debug(f'Searching on {applications_dir}', __name__)
            # Finds all toml files
            app_files = [toml for toml in applications_dir.glob('*.toml')]
            # Finds all json files
            app_files.extend([json for json in applications_dir.glob('*.json')])
            _logger.debug(f'Found {app_files}', __name__)
            ret_value.extend(app_files)
        
        _logger.debug('Applicaton configuration files with directories in order of priority: '
                      f'{ret_value}', __name__)
        return ret_value
    
    def _load_script_paths(self, theme_manager_paths: list[Path]) -> list[Path]:
        """Loads the paths of the scripts in order of priority."""

        # Return list
        ret_value = list()
        _logger.debug(f'Loading the scripts paths from the directories {theme_manager_paths}', __name__)

        # Iterations on every theme-manager directory
        for dir in theme_manager_paths:
            scripts_dir = Path(dir, 'scripts')
            if not scripts_dir.exists():
                _logger.debug(f'{scripts_dir} doesn\'t exist.', __name__)
                continue
            _logger.debug(f'Searching on {scripts_dir}', __name__)
            # Finds all Python files
            scripts = [script for script in scripts_dir.glob('*.py')]
            _logger.debug(f'Found {scripts}', __name__)
            ret_value.extend(scripts)
        
        _logger.debug(f'Scripts with directories in order of priority: {ret_value}', __name__)
        return ret_value


def create() -> _PathHandler:
    global path_handler
    global _logger
    _logger = logging_utils.get()
    try:
        if path_handler:
            _logger.warn('Tried to recreate the path handler. If you are seeing this warning, '
                        'please open an issue at https://github.com/Limones-07/theme-manager.')
            return path_handler
    except NameError:
        pass
    path_handler = _PathHandler()
    
    return path_handler


def get() -> _PathHandler:
    global path_handler
    try:
        return path_handler
    except NameError:
        logger = logging_utils.get()
        logger.error(f'Tried to get the path handler without creating it. If you are seeing this error, '
                     'please open an issue at https://github.com/Limones-07/theme-manager.', EX_SOFTWARE, __name__)

