import sys

from ..utils import logging_utils
from ..utils import configuration_handler
from ..utils import cli_parser


def main():

    if sys.argv[1] == 'TEST':
        from ..utils import path_handler
        logger = logging_utils.create(2)
        logger.debug('RUNNING TESTS', __name__)
        path_handler.test()
        exit()
    
    # Parse operation and initialize some important objects
    operation, output_format, verbosity = cli_parser.parse_operation()

    logger = logging_utils.create(verbosity)
    
    logger.debug('Starting main logic.', __name__)
    logger.debug(f'Operation instruction: {operation}', __name__)
    logger.debug(f'Output format: {output_format}', __name__)

    config_handler = configuration_handler.create()
    

if __name__ == "__main__":
    main()