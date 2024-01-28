"""Defines the Logger class."""

import sys

from ..envs import DEFAULT_VERBOSITY

class _Logger():
    """Based on the verbosity level, logs to stdout and stderr."""

    def __init__(self, verbosity: int = DEFAULT_VERBOSITY, script_create: bool = False) -> None:
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        if verbosity > 2:
            self.verbosity = 2
        elif verbosity < -1:
            self.verbosity = -1
        else:
            self.verbosity = verbosity
        if script_create:
            self.debug(f'Logger created for a script with verbosity level at {verbosity}!', __name__)
            self.print = None
        else:
            self.debug(f'Logger created with verbosity level at {verbosity}!', __name__)
            self.debug(f'theme-manager called with command: {" ".join(sys.argv)}', __name__)

    def get_verbosity(self) -> int:
        """Returns the logger's verbosity level."""

        return self.verbosity
    
    def debug(self, message: str, module: str) -> None:
        """Used for debug information."""

        # Verbosity level: 2
        if self.verbosity < 2:
            return
        self.stdout.write(f'[DEBUG:{module}] ' + message + '\n')

    def info(self, message: str) -> None:
        """Used to track the program flow."""

        # Verbosity level: 1
        if self.verbosity < 1:
            return
        self.stdout.write('[INFO]' + message + '\n')

    def warn(self, message: str) -> None:
        """Used to warn about things that aren't normal and might be unintentional or wrong."""

        # Verbosity level: 0
        if self.verbosity < 0:
            return
        self.stderr.write('[WARNING] ' + message + '\n')

    def print(self, message: str) -> None:
        """Used to print the requested information on the console. This function doesn't obbey
        the `--quiet` option."""

        # Verbosity level: -1
        self.stdout.write(message + '\n')

    def error(self, message: str, exit_code: int, module: str) -> None:
        """Used to warn about a critical problem that prevent the normal execution of the program.
        The program will be stopped after this log."""

        # Verbosity level: -1
        self.stderr.write(f'[ERROR:{module}] ' + message + '\n')
        self.stderr.write(f'[ERROR] Ending theme-manager\'s execution.\n')
        exit(exit_code)


def create(verbosity: int = DEFAULT_VERBOSITY) -> _Logger:
    global _logger
    try:
        if _logger:
            _logger.warn(f'Tried to recreate the logger. ')
            return _logger
    except NameError:
        pass
    _logger = _Logger(verbosity)
    return _logger


def script_create() -> _Logger:
    global _logger
    verbosity = _logger.get_verbosity()
    return _Logger(verbosity, script_create=True)


def get() -> _Logger:
    global _logger
    try:
        return _logger
    except NameError:
        _logger = _Logger()
        _logger.debug(f'Logger wasn\'t created explicitly. Verbosity level set to default ({DEFAULT_VERBOSITY}).')
        return _logger
