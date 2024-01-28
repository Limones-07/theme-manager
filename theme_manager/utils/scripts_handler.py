"""Defines the ScriptsHandler class."""

import os
import importlib.util
from pathlib import Path

from . import path_handler as path_handler_module
from . import logging_utils
from ..envs import EX_DATAERR, EX_SOFTWARE


class _Script():
    """Provides a way to store a script as an object."""

    def __init__(self, script_path: Path, script_type: str) -> None:
        """Initializes the script with all the necessary information."""

        self._name = script_path.stem
        self._path = script_path
        self._type = script_type
        self._spec = importlib.util.spec_from_file_location(f'script_{self._name}_{script_type}',
                                                            script_path)
        self._module = importlib.util.module_from_spec(self._spec)
        self._spec.loader.exec_module(self._module)

        try:
            if not callable(getattr(self._module, 'main')):
                _logger.warn(f'The "main" object of the script at {self._path} isn\'t a callable. Ignoring.')
        except AttributeError:
            _logger.warn(f'The script at {self._path} does not contain the function "main". Ignoring.')
    
    def run(self, *args, **kwargs):
        """Imports and executes the script. Returns whatever the script's `main` function returns."""

        # Creates the script logger
        script_logger = logging_utils.script_create()
        
        # Loads the module
        self._spec.loader.exec_module(self._module)

        # Executes the "main" function of the script
        match self._type:
            case 'enabling_procedure':
                self._module.main(logger=script_logger, *args, **kwargs)
                return None
            case 'check_procedure':
                ret_value = self._module.main(logger=script_logger, *args, **kwargs)
                return bool(ret_value)
            case 'reference':
                return self._module.main(logger=script_logger, *args, **kwargs)


class _ScriptsHandler():
    """Provides an API for interacting with installed scripts."""

    def __init__(self) -> None:
        """Initializes the handler with every path it needs."""

        # Gets the Path Handler
        path_handler = path_handler_module.get()

        # Gets the scripts paths
        scripts_paths = path_handler.get_script_paths()

        # Finds all the scripts and classify them
        self._enabling_procedures = dict()
        self._check_procedures = dict()
        self._references = dict()

        for scripts_path in scripts_paths:
            for script_path in scripts_path.glob('**/*.py'):
                self._load_script(script_path)
    
    def _load_script(self, script_path: Path):
        """Loads a script and adds it to the scripts dictionary."""

        if script_path.match('theme-manager/scripts/enabling-procedures/*.py'):
            self._enabling_procedures[script_path.stem] = _Script(script_path, 'enabling-procedure')
        elif script_path.match('theme-manager/scripts/check-procedures/*.py'):
            self._check_procedures[script_path.stem] = _Script(script_path, 'check-procedure')
        elif script_path.match('theme-manager/scripts/references/*.py'):
            self._references[script_path.stem] = _Script(script_path, 'reference')
        else:
            _logger.warn(f'There is a script at the wrong place ({script_path}). It will not be loaded.')

    def run_enabling_procedure(self, script: str, *args, **kwargs) -> None:
        """Runs an enabling procedure."""

        if not script in self._enabling_procedures:
            _logger.error(f'Tried to run the script {script}, but it does not exist or isn\'t an enabling procedure.',
                          EX_DATAERR, __name__)
        self._enabling_procedures[script].run(*args, **kwargs)

    def run_check_procedure(self, script: str, *args, **kwargs) -> None:
        """Runs a check procedure."""

        if not script in self._check_procedures:
            _logger.error(f'Tried to run the script {script}, but it does not exist or isn\'t a check procedure.',
                          EX_DATAERR, __name__)
        return self._check_procedures[script].run(*args, **kwargs)
    
    def run_reference(self, script: str, *args, **kwargs) -> None:
        """Runs a reference script."""

        if not script in self._references:
            _logger.error(f'Tried to run the script {script}, but it does not exist or isn\'t a reference.',
                          EX_DATAERR, __name__)
        return self._references[script].run(*args, **kwargs)
        

def create() -> _ScriptsHandler:
    global scripts_handler
    global _logger
    _logger = logging_utils.get()
    try:
        if scripts_handler:
            _logger.warn('Tried to recreate the scripts handler. If you are seeing this warning, '
                        'please open an issue at https://github.com/Limones-07/theme-manager.')
            return scripts_handler
    except NameError:
        pass
    scripts_handler = _ScriptsHandler()
    return scripts_handler


def get() -> _ScriptsHandler:
    try:
        return scripts_handler
    except NameError:
        logger = logging_utils.get()
        logger.error(f'Tried to get the scripts handler without creating it. If you are seeing this error, '
                     'please open an issue at https://github.com/Limones-07/theme-manager.', EX_SOFTWARE, __name__)