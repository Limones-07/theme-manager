"""Based on command-line options, parses the operation specified by the user for the program to execute."""

import sys
import argparse

from ..envs import DEFAULT_VERBOSITY, EX_USAGE

def parse_request() -> list:
    """Based on command-line options, parses the operation specified by the user for the program to execute.

    Returns a list, being the first element the requested operation, the second the theme requested by the user and the third the verbosity level.  

    If the operation doesn't require a theme to be selected, the second element is `None`."""

    parser = _build_parser()
    args = parser.parse_args()

    # If there are no arguments, print the help message and leave
    if len(sys.argv) < 2:
        parser.print_help()
        exit(EX_USAGE)
    
    operation = [None, None, None]
    if args.dump:
        operation[0] = 'd'
    elif args.requested_theme:
        operation[0] = 's'
        operation[1] = args.requested_theme
    if args.quiet:
        operation[2] = -1
    else:
        operation[2] = args.verbosity
        
    return operation


def _build_parser() -> argparse.ArgumentParser:
    """Builds the command-line parser."""

    # parser = argparse.ArgumentParser(description="A command-line tool for managing themes in your Linux installation based on each theme's configuration.")
    parser = argparse.ArgumentParser()
    
    option_group = parser.add_mutually_exclusive_group(required=True)
    option_group.add_argument('-d', '--dump', action='store_true', dest='dump',
                              help='dumps information about available themes and their configured applications, '
                                'the current general state of the theme configuration and'
                                'application specific configuration')
    option_group.add_argument('-s', '--set', action='store', 
                              metavar='THEME', dest='requested_theme',
                              help='sets the global theme to the specified theme according to its configuration')

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('-v', '--verbose', action='count', default=DEFAULT_VERBOSITY, dest='verbosity',
                        help='the program will be more verbose on its operation (if used twice, will print debug messages)')
    verbosity_group.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                                 help='the program won\'t print anything to stdout, '
                                    'but will still print to stderr in case of errors (not warnings)')
    
    return parser
