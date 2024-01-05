"""Defines the ConfigurationHandler class"""

import os
import tomllib
import json
from pathlib import Path

from . import reference_interpreter
from .. import logging_utils
from ..path_utils import dir_finder
from ..envs import EX_DATAERR, EX_SOFTWARE


class _ConfigurationHandler():
    """Provides an API for interacting with `theme-manager`'s configuration."""

    def __init__(self) -> None:
        """Initializes the handler with every path it needs."""

        global logger

        # Loads the configuration paths
        self._theme_manager_dirs = dir_finder.on_xdg_configuration_paths('theme-manager')
        logger.debug(f'Found theme-manager\'s directories at {self._theme_manager_dirs}.', __name__)
        
        self._theme_config_paths: list[Path] = list()
        self._application_config_paths: list[Path] = list()
        # self._script_paths: list[Path] = list()
        for path in self._theme_manager_dirs:
            theme_path = Path(path, 'themes')
            applications_path = Path(path, 'applications')
            # scripts_path = Path(path, 'scripts')
            if theme_path.exists():
                self._theme_config_paths.append(theme_path)
            if applications_path.exists():
                self._application_config_paths.append(Path(path, 'applications'))
            # if scripts_path.exists():
            #     self._script_paths.append(Path(path, 'scripts'))

        logger.debug(f'Theme configuration paths: {self._theme_config_paths}.', __name__)
        logger.debug(f'Application configuration paths: {self._application_config_paths}.', __name__)
        # logger.debug(f'Script paths: {self._script_paths}.', __name__)

        self._load_themes()

    def get_themes(self) -> dict:
        """Returns the themes dictionary."""

        return self._themes
     
    def _load_themes(self) -> None:
        """Validates and loads the theme configuration files."""

        logger.debug(f'Loading and validating the themes.', __name__)
        self._themes: dict = dict()
        for themes_path in self._theme_config_paths:
            theme_dirs = os.listdir(themes_path)
            for theme_dir in theme_dirs:
                theme_path = Path(themes_path, theme_dir)
                theme = self._load_theme_file(theme_path)
                if not theme:
                    continue
                theme['path'] = theme_path
                theme = reference_interpreter.replace_references(theme)
                self._validate_theme_config(theme)
    
    def _load_theme_file(self, theme_path: Path) -> dict | None:
        """Loads a theme's TOML or JSON configuration file into a dictionary."""

        theme_dir_files = os.listdir(theme_path)
        if not 'theme.toml' in theme_dir_files and not 'theme.json' in theme_dir_files:
            logger.warn(f'The directory {theme_path.name} at {theme_path.parent} does not contain a "theme.toml" '
                         'nor a "theme.json" file. ')
            return None

        if 'theme.toml' in theme_dir_files:
            if 'theme.json' in theme_dir_files:
                logger.error(f'Found "theme.toml" and "theme.json" at {theme_path}. If you made this configuration, '
                              'remove one of the files. If you didn\'t, ask the author to do so.', EX_DATAERR, __name__)
            
            theme_file = Path(theme_path, 'theme.toml')
            with open(theme_file, 'rb') as file: 
                logger.debug(f'Loading TOML theme configuration file at {theme_file}.', __name__)
                return tomllib.load(file)
        
        theme_file = Path(theme_path, 'theme.json')
        with open(theme_file, 'r') as file:
            logger.debug(f'Loading JSON theme configuration file at {theme_file}.', __name__)
            return json.load(theme_file)
    
    def _validate_theme_config(self, theme: dict) -> None:
        """Validates a theme configuration's syntax. """

        def validate_instance(obj, cls) -> bool:
            cls_str = ' table/object' if cls == dict else \
                'n array' if cls == list else \
                ' string'

            if cls == str:
                if not obj and not isinstance(obj, str):
                    logger.error(f'The entry "{testing_key} of the theme at {theme["path"]} is not a{cls_str}"', EX_DATAERR, __name__)
            elif not isinstance(obj, cls):
                logger.error(f'The entry "{testing_key} of the theme at {theme["path"]} is not a{cls_str}"', EX_DATAERR, __name__)
            return True
        
        try:
            testing_key = 'name'
            validate_instance(theme['name'], str)
            
            testing_key = 'check_procedures'
            validate_instance(theme['check_procedures'], list)
            
            for check_procedure_index in range(len(theme['check_procedures'])):
                testing_key = f'check_procedures.[{check_procedure_index}]'
                validate_instance(theme['check_procedures'][check_procedure_index], dict)
                self._validate_check_procedure(theme['check_procedures'][check_procedure_index], check_procedure_index, 
                                               testing_key, theme['path'], validate_instance, True)

                testing_key = f'check_procedures.[{check_procedure_index}].required_by'
                # validate_instance(theme['check_procedures'][check_procedure_index]['required_by'], str)

        except KeyError as missing_entry:
            logger.error(f'The entry "{testing_key}" of the theme at {theme["path"]} is missing.', EX_DATAERR, __name__)
        
    def _validate_check_procedure(self, check_procedure: dict, check_procedure_index: int, testing_key_base: str, 
                                  file_path: str, validate_instance, is_theme: bool = False,) -> None:
        """Validates a check procedure's syntax. """

        KNOWN_TYPES = ['json_entry', 'command_exists', 'file_exists', 'directory_exists', 'script']

        try:
            testing_key = f'{testing_key_base}.type'
            # validate_instance(check_procedure['type'], str)
            if not check_procedure['type'] in KNOWN_TYPES:
                logger.error(f'The entry "{testing_key}" of the check procedure {check_procedure_index} at {file_path} provides an invalid check procedure type.', 
                             EX_DATAERR, __name__)
            
            match check_procedure['type']:
                case 'json_entry':
                    testing_key = f'{testing_key_base}.file'
                    
                    

        except KeyError as missing_entry:
            if is_theme:
                logger.error(f'The entry "{missing_entry}" of the theme at {file_path} is missing.', EX_DATAERR, __name__)
            logger.error(f'The entry "{missing_entry}" of the application at {file_path} is missing.', EX_DATAERR, __name__)


def create() -> _ConfigurationHandler:
    global config_handler
    global logger
    logger = logging_utils.get()
    try:
        if config_handler:
            logger.warn('Tried to recreate the configuration handler. If you are seeing this warning, '
                        'please open an issue at https://github.com/Limones-07/theme-manager.')
            return config_handler
    except NameError:
        pass
    config_handler = _ConfigurationHandler()
    return config_handler


def get() -> _ConfigurationHandler:
    global config_handler
    try:
        return config_handler
    except NameError:
        logger = logging_utils.get()
        logger.error(f'Tried to get the configuration handler without creating it. If you are seeing this error, '
                     'please open an issue at https://github.com/Limones-07/theme-manager.', EX_SOFTWARE, __name__)