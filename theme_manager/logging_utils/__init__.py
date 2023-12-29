"""Defines the Logger class."""

import sys

from ..envs import DEFAULT_VERBOSITY

class Logger():
    """Based on the verbosity level, logs to stdout and stderr."""

    def __init__(self, verbosity: int = DEFAULT_VERBOSITY) -> None:
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        if verbosity > 2:
            self.verbosity = 2
        elif verbosity < -1:
            self.verbosity = -1
        else:
            self.verbosity = verbosity
        self.debug(f'Logger created with verbosity level at {verbosity}!', __name__)
    
    def debug(self, message: str, module: str) -> None:
        # Used for extreme verbosity / debug.
        # Verbosity level: 2
        if self.verbosity < 2:
            return
        if module:
            module = ':' + module
        self.stdout.write(f'[DEBUG{module}] ' + message + '\n')

    def info(self, message: str) -> None:
        # Used to track the program flow.
        # Verbosity level: 1
        if self.verbosity < 1:
            return
        self.stdout.write('[INFO]' + message + '\n')

    def print(self, message: str) -> None:
        # Used to tell the user about the start and the end of the execution.
        # Verbosity level: 0
        if self.verbosity < 0:
            return
        self.stdout.write(message + '\n')

    def warn(self, message: str) -> None:
        # Used to warn about things that aren't normal and might be unintentional or wrong.
        # Verbosity level: 0
        if self.verbosity < 0:
            return
        self.stderr.write('[WARNING] ' + message + '\n')

    # def error(self, message: str) -> None:
    #     # Used to warn about a critical problem that prevent the normal execution of the program.
    #     # The program should be stopped after this log.
    #     # Verbosity level: -1
    #     self.stderr.write('[ERROR] ' + message + '\n')


def create(verbosity: int = DEFAULT_VERBOSITY) -> Logger:
    global logger
    try:
        if logger:
            logger.info(f'The logger is being recreated. Setting verbosity to {verbosity}.')
    except NameError:
        pass
    logger = Logger(verbosity)
    return logger


def get() -> Logger:
    global logger
    try:
        return logger
    except NameError:
        logger = Logger()
        logger.debug(f'Logger wasn\'t created explicitly. Verbosity level set to default ({DEFAULT_VERBOSITY}).')
        return logger
