from .. import logging_utils
from ..parsers import cli_parser, theme_parser


def main():
    
    # Parse operation and start the logger
    operation = cli_parser.parse_request()
    logger = logging_utils.create(operation.pop(2))
    
    logger.debug('Starting main logic.', __name__)
    themes = theme_parser.parse_themes()


if __name__ == "__main__":
    main()