"""Defines the _ConfigurationHandler class."""

import os
import json
import shutil
import tomllib
from pathlib import Path
from abc import ABC, abstractmethod

from . import scripts_handler as scripts_handler_module
from . import path_handler as path_handler_module
from .reference_interpreter import ReferenceInterpreter
from . import logging_utils
from ..envs import EX_DATAERR, EX_UNAVAILABLE, EX_SOFTWARE


class _Configuration(ABC):
    """Provides the common methods between application and theme configurations.
    Before using a configuration, call the `check` method to validate the contents of the file,
    interpret and replace all the references and run the check procedures."""

    def __init__(self, config_path: Path) -> None:
        """Loads the configuration file."""

        self._path = self._name = config_path  # The name of the configuration should be properly defined when validating the config.
        self._document = self._load()
        self._reference_interpreter = self._create_reference_interpreter()
        self._checked = False

    def check(self, weak=False) -> None:
        """Calls `_validate_config`, runs the check procedures and stops the program if a check procedure fails.
        If the parameter `weak` is true, it won't stop the program if a check procedure fails, but print a warning instead."""

        def json_entry(file: Path, entry: list, value, procedure_index: int | None = None) -> None:
            def navigate_json(navigator, entry_list: list) -> bool:
                if len(entry_list) == 0:
                    return True if navigator == value else False
                entry = entry_list.pop(0)
                if entry == '?':
                    if not isinstance(navigator, list):
                        check_failure('Tried to iterate a object that isn\'t an array using "?".', EX_DATAERR, procedure_index)
                    for index in range(len(navigator)):
                        if navigate_json(navigator[index], entry_list):
                            return True
                    return False
                try:
                    navigator = navigator[entry]
                except KeyError:
                    check_failure(f'Tried to access the inexistent "{entry}" key.', EX_DATAERR, procedure_index)
                return navigate_json(navigator, entry_list)
            
            with open(file, 'r') as f:
                document = json.load(file)
            if not navigate_json(document, entry):
                check_failure(f'The json entry "{".".join(entry)}" doesn\'t exist or doesn\'t contain the value {value}.',
                              EX_DATAERR, procedure_index)

        def command_exists(command: str, procedure_index: int | None = None) -> None:
            if not shutil.which('command'):
                check_failure(f'The command {command} does not exist.', EX_UNAVAILABLE)

        def file_exists(file: str, path: str | None = None, recursive: bool = False, procedure_index: int | None = None) -> None:
            file_path = Path(file)

            if file_path.is_absolute():
                if not file_path.exists():
                    check_failure(f'The file {file} doesn\'t exist.', procedure_index)
                if file_path.is_dir():
                    check_failure(f'{file} is a directory, not a file.', procedure_index)
            
            else:
                for search_path in path.split(':'):
                    full_path = Path(search_path, file)
                    if recursive:
                        for testing_path in Path(search_path).glob('**/*'):
                            if file == testing_path.parts[-1] and testing_path.is_file():
                                return
                    else:
                        if file in os.listdir(search_path) and full_path.is_file():
                            return
                check_failure(f'The file {file} doesn\'t exist at the specified paths.', procedure_index)

        def directory_exists(directory: str, path: str | None = None, recursive: bool = False, procedure_index: int | None = None) -> None:
            dir_path = Path(directory)

            if dir_path.is_absolute():
                if not dir_path.exists():
                    check_failure(f'The directory {directory} doesn\'t exist.', procedure_index)
                if dir_path.is_file():
                    check_failure(f'{directory} is a file, not a directory.', procedure_index)
            
            else:
                for search_path in path.split(':'):
                    full_path = Path(search_path, dir_path)
                    if recursive:
                        for testing_path in Path(search_path).glob('**/*'):
                            if directory == testing_path.parts[-1] and testing_path.is_file():
                                return
                    else:
                        if directory in os.listdir(search_path) and full_path.is_dir():
                            return
                check_failure(f'The directory {directory} doesn\'t exist at the specified paths.', procedure_index)

        def check_failure(message: str, exit_code: int, procedure_index: int | None):
            if procedure_index != None:
                pos_str = f' on the index {procedure_index} of the check procedures array'
            else:
                pos_str = ''
            failure_str = f'The check procedure defined at {self._path}{pos_str} failed. \n\
                Error message: {message}'
            _logger.warn(failure_str) if weak else _logger.error(failure_str, exit_code, __name__)
        
        # Validates the configuration file and defines its name
        self._validate_config()

        # # Interprets and replaces all the references
        # self._reference_interpreter.run(self._document)

        # Runs the check procedures
        for procedure_index in range(len(self._document['check_procedures'])):
            procedure = self._document['check_procedures'][procedure_index]

            match procedure['type']:
                case 'json_entry':
                    json_entry(procedure['file'], procedure['entry'], procedure['value'])

                case 'command_exists':
                    command_exists(procedure['command'], procedure_index)

                case 'file_exists':
                    file_exists(procedure['file'], procedure['path'], procedure['recursive'], procedure_index)

                case 'directory_exists':
                    directory_exists(procedure['directory'], procedure['path'], procedure['recursive'], procedure_index)

                case 'script':
                    scripts_handler = scripts_handler_module.get()
                    if not scripts_handler.run_check_procedure(procedure['name'], *tuple(procedure['args']), **procedure['kwargs']):
                        check_failure(f'The check procedure from the script {procedure["name"]} failed.', 1, procedure_index)

                case _:
                    check_failure('The specified type is invalid.', EX_DATAERR, procedure_index)
        
        self._checked = True

    def get_name(self) -> str:
        """Returns the name of what this configures."""

        if not self._checked:
            _logger.error(f'Tried to get the name of a configuration before checking it. If you are seeing this error,
                          please open an issue at https://github.com/Limones-07/theme-manager.', EX_SOFTWARE, __name__)
        return self._name
    
    def _validate_check_procedure(self, procedure: dict, procedure_index: int, parent_testing_key: str) -> None:
        """Validates the contents of a check procedure and stops the program if something is invalid"""

        testing_key = parent_testing_key
        try:
            testing_key = parent_testing_key + '.type'
            self._validate_instance(procedure['type'], str, testing_key)

            match procedure['type']:
                # Validates the required entries of the "json_entry" type
                case 'json_entry':
                    testing_key = parent_testing_key + '.file'
                    self._validate_instance(procedure['type'], str, testing_key)
                    
                    testing_key = parent_testing_key + '.value'
                    procedure['value']  # Just try to access the entry "value", as it can be basically anything.
                
                # Validates the required entries of the "command_exists" type
                case 'command_exists':
                    testing_key = parent_testing_key + '.command'
                    self._validate_instance(procedure['command'], str, testing_key)

                # Validates the required entries of the "file_exists" type
                case 'file_exists':
                    testing_key = parent_testing_key + '.file'
                    self._validate_instance(procedure['file'], str, testing_key)

                    testing_key = parent_testing_key + '.path'
                    self._validate_instance(procedure['path'], str, testing_key)

                    testing_key = parent_testing_key + '.recursive'
                    self._validate_instance(procedure['recursive'], bool, testing_key)

                # Validates the required entries of the "directory_exists" type
                case 'directory_exists':
                    testing_key = parent_testing_key + '.directory'
                    self._validate_instance(procedure['directory'], str, testing_key)

                    testing_key = parent_testing_key + '.path'
                    self._validate_instance(procedure['path'], str, testing_key)

                    testing_key = parent_testing_key + '.recursive'
                    self._validate_instance(procedure['recursive'], bool, testing_key)

                # Validates the required entries of the "script" type
                case 'script':
                    testing_key = parent_testing_key + '.name'
                    self._validate_instance(procedure['directory'], str, testing_key)

                    testing_key = parent_testing_key + '.args'
                    self._validate_instance(procedure['path'], list, testing_key)

                    testing_key = parent_testing_key + '.kwargs'
                    self._validate_instance(procedure['recursive'], dict, testing_key)

        except KeyError:
            _logger.error(f'The entry "{testing_key}" of the check procedure at index {procedure_index} from the '
                          f'check procedures array in the configuration at {self._path} is missing.', EX_DATAERR, __name__)

    def _validate_instance(self, obj, cls, testing_key) -> bool:
        """Validates if an object is the type it should be. Used on functions that validate the contents of a file."""

        cls_str = ' table/object' if cls == dict else \
            'n array' if cls == list else \
            ' string'

        if cls == str:
            if not obj and not isinstance(obj, str):
                _logger.error(f'The entry "{testing_key} of the configuration at {self._path} is not a{cls_str}"', EX_DATAERR, __name__)
        elif not isinstance(obj, cls):
            _logger.error(f'The entry "{testing_key} of the configuration at {self._path} is not a{cls_str}"', EX_DATAERR, __name__)
        return True

    @abstractmethod
    def _load(self) -> dict:
        """Loads the configuration file into a dictionary."""

        pass

    @abstractmethod
    def _create_reference_interpreter(self) -> ReferenceInterpreter:
        """Creates the reference interpreter."""

        pass

    @abstractmethod
    def _validate_config(self) -> None:
        """Validates the contents of a configuration file and stops the program if something is invalid."""

        pass


class _ApplicationConfiguration(_Configuration):
    """Provides a way to store the configuration of an application as an object."""

    def _load(self) -> dict:
        """Loads an application's TOML or JSON configuration file into a dictionary."""

        # If the configuration file is a TOML file...
        if self._path.suffix == '.toml':
            # Loads the TOML file as a dictionary and returns it.
            with open(self._path, 'rp') as file:
                _logger.debug(f'Loading TOML application configuration file at {self._path}.', __name__)
                return tomllib.load(file)

        # If the configuration file isn't a TOML file, it must be a JSON, so...
        # Loads the JSON file as a dictionary and returns it.
        with open(self._path, 'r') as file:
            _logger.debug(f'Loading JSON application configuration file at {self._path}.', __name__)
            return json.load(file)
    
    def _create_reference_interpreter(self) -> ReferenceInterpreter:
        """Creates the reference interpreter."""

        return ReferenceInterpreter()
    
    def _validate_enabling_procedure(self, procedure: dict, procedure_index: int, parent_testing_key: str) -> None:
        """Validates an enabling procedure's syntax. """
        # TODO this whole function
    
    def _validate_config(self) -> None:
        """Validates an application configuration's syntax. """

        # Runs the reference interpreter only for the default references.
        self._document = self._reference_interpreter.run(self._document, only_defaults=True)

        # Validates the data type of every entry in the configuration file
        try:
            testing_key = 'name'
            self._validate_instance(self._document['name'], str, testing_key)
            self._name = self._document['name']

            testing_key = 'check_procedures'
            self._validate_instance(self._document['check_procedures'], list, testing_key)

            for check_procedure_index in range(len(self._document['check_procedures'])):
                testing_key = f'check_procedures.[{check_procedure_index}]'
                self._validate_instance(self._document['check_procedures'][check_procedure_index], dict, testing_key)
                self._validate_check_procedure(self._document['check_procedures'][check_procedure_index], 
                                               check_procedure_index, testing_key)
            
            testing_key = 'enabling_procedures'
            self._validate_instance(self._document['enabling_procedures'], list, testing_key)

            for enabling_procedure_index in range(len(self._document['enabling_procedures'])):
                testing_key = f'enabling_procedures.[{enabling_procedure_index}]'
                self._validate_instance(self._document['enabling_procedures'][enabling_procedure_index],
                                        dict, testing_key)
                self._validate_enabling_procedure(self._document['enabling_procedures'][enabling_procedure_index],
                                                  enabling_procedure_index, testing_key)
                
        except KeyError:
            _logger.error(f'The entry "{testing_key}" of the application at {self._path} is missing.', EX_DATAERR, __name__)


class _ThemeConfiguration(_Configuration):
    """Provides a way to store the configuration of a theme as an object."""

    def _load(self) -> dict:
        """Loads a theme's TOML or JSON configuration file into a dictionary."""

        # Files of the theme's directory
        theme_dir_files = os.listdir(self._path)

        # If the configuration file is a TOML file...
        if 'theme.toml' in theme_dir_files:
            # Loads the TOML file as a dictionary and returns it.
            theme_file = Path(self._path, 'theme.toml')
            with open(theme_file, 'rb') as file: 
                _logger.debug(f'Loading TOML theme configuration file at {theme_file}.', __name__)
                return tomllib.load(file)
        
        # If the configuration file isn't a TOML file, it must be a JSON file, so...
        # Loads the JSON file as a dictionary and returns it.
        theme_file = Path(self._path, 'theme.json')
        with open(theme_file, 'r') as file:
            _logger.debug(f'Loading JSON theme configuration file at {theme_file}.', __name__)
            return json.load(file)
        
    def _create_reference_interpreter(self) -> ReferenceInterpreter:
        """Creates the reference interpreter with the "@THEME_DIR" default reference."""

        default_references = {
            '@THEME_DIR': ReferenceInterpreter.construct_reference(str, self._path)
        }
        return ReferenceInterpreter(default_references)
    
    def _validate_config(self) -> None:
        """Validates a theme configuration's syntax. """
        
        # Runs the reference interpreter only for the default references.
        self._document = self._reference_interpreter.run(self._document, only_defaults=True)

        # Validates the data type of every entry in the configuration file
        try:
            # Validates and defines the theme's name
            testing_key = 'name'
            self._validate_instance(self._document['name'], str, testing_key)
            self._name = self._document['name']
            
            testing_key = 'check_procedures'
            self._validate_instance(self._document['check_procedures'], list, testing_key)
            
            for check_procedure_index in range(len(self._document['check_procedures'])):
                testing_key = f'check_procedures.[{check_procedure_index}]'
                self._validate_instance(self._document['check_procedures'][check_procedure_index], dict, testing_key)
                self._validate_check_procedure(self._document['check_procedures'][check_procedure_index], 
                                               check_procedure_index, testing_key)

                testing_key = f'check_procedures.[{check_procedure_index}].required_by'
                self._validate_instance(self._document['check_procedures'][check_procedure_index]['required_by'], str, testing_key)
                # TODO store the required_by data to be used when checking the theme's config

            testing_key = 'applications'
            self._validate_instance(self._document['applications'], list, testing_key)

            for application_index in range(len(self._document['applications'])):
                testing_key = f'applications.[{application_index}]'
                self._validate_instance(self._document['applications'][application_index], dict, testing_key)
                
                testing_key = f'applications.[{application_index}].id'
                self._validate_instance(self._document['applications'][application_index]['id'], str, testing_key)

                testing_key = f'applications.[{application_index}].procedure'
                self._validate_instance(self._document['applications'][application_index]['procedure'], dict, testing_key)

                testing_key = f'applications.[{application_index}].procedure.id'
                self._validate_instance(self._document['applications'][application_index]['procedure']['id'], 
                                        dict, testing_key)
                # TODO validate procedure

        except KeyError:
            _logger.error(f'The entry "{testing_key}" of the theme at {self._path} is missing.', EX_DATAERR, __name__)


class _ConfigurationHandler():
    """Provides an API for interacting with theme-manager's configuration."""

    def __init__(self) -> None:
        """Initializes the handler with every path it needs."""

        _logger.debug('Initializing the Configuration Handler.')

        # Initializes the Path Handler
        path_handler = path_handler_module.create()

        # Initializes the Scripts Handler
        self._scripts_handler = scripts_handler_module.create()
        
        _logger.debug('Got the Path Handler and Scripts Handler. Starting to load themes and applications.')

        # Loads the themes
        self._themes = [_ThemeConfiguration(path) for path in path_handler.get_themes_paths()]

        # Loads the applications
        self._applications = [_ApplicationConfiguration(path) for path in path_handler.get_applications_paths()]

        _logger.debug('Themes and applications loaded. ')

    def get_themes(self) -> list:
        """Returns the themes list."""

        return self._themes.copy()
    
    def get_applications(self) -> list:
        """Returns the applications list."""

        return self._applications.copy()


def create() -> _ConfigurationHandler:
    global config_handler
    global _logger
    _logger = logging_utils.get()
    try:
        if config_handler:
            _logger.warn('Tried to recreate the configuration handler. If you are seeing this warning, '
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