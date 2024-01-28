"""Based on command-line options, parses the operation specified by the user for the program to execute."""

import argparse

from ..envs import DEFAULT_VERBOSITY, EX_USAGE

def parse_operation() -> tuple[list, str, int]:
    """Based on command-line options, parses the operation specified by the user for the program to execute."""

    # Parses the command-line arguments
    parser = _build_parser()
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        exit(EX_USAGE)

    # Parses the verbosity
    if args.quiet:
        verbosity = -1
    else:
        verbosity = args.verbosity
    pass

    # Parses the output format
    output_format = args.output_format

    # Parses the requested operation
    args_dict = vars(args)
    args_dict.pop('quiet')
    args_dict.pop('verbosity')
    args_dict.pop('output_format')

    selected_options = list()
    for key in args_dict:
        if args_dict[key]:
            selected_options.append((key.split('_'), args_dict[key]))
    
    # Using hexadecimal numbers for identifing the operation allows easier expansion.
    operation = [0x0, None, None, None]  # List structure inspired on asm.

    for option in selected_options:

        match option[0][0]:

            case 'sty':
                _style_operation_parser(operation, option[0], option[1])

            # case 'pre':
            #     _preset_operation_parser(operation, option)

            # case 'con':
            #     _configuration_operation_parser(operation, option)
    
    return (operation, output_format, verbosity)


def _style_operation_parser(operation: list, option_key: list, option_value: str | int | bool) -> None:
    """Parses the requested style operation."""

    # 0x1000
    match option_key[1]:
        case 'ena':  # 0x100
            match option_key[2]:
                case 'req':  # 0x10
                    operation[1] = option_value
                    match option_key[3]:
                        case 'the':  # 0x1
                            operation[0] = 0x1111
                        case 'fon':  #0x2
                            operation[0] = 0x1112

                case 'tar':
                    operation[2] = option_key[3]
                    if operation[2] == 'app':
                        operation[3] = option_value
        
        case 'get':  # 0x200
            match option_key[2]:
                case 'spe':  # 0x10
                    operation[1] = option_value
                    match option_key[3]:
                        case 'the':  # 0x1
                            operation[0] = 0x1211
                        case 'app':  # 0x2
                            operation[0] = 0x1212
                
                case 'gen':  # 0x20
                    match option_key[3]:
                        case 'sta':  # 0x1
                            operation[0] = 0x1221
                        case 'the':  # 0x2
                            operation[0] = 0x1222
                        case 'app':  # 0x3
                            operation[0] = 0x1223
                        case 'dum':  # 0x4
                            operation[0] = 0x1224


def _build_parser() -> argparse.ArgumentParser:
    """Builds the command-line parser."""

    parser = argparse.ArgumentParser(exit_on_error=False)

    parser.add_argument('--output-format', action='store', choices=['human', 'json'], 
                        default='human', dest='output_format',
                        help='defines how theme-manager should output information when requested to')

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('-v', '--verbose', action='count', default=DEFAULT_VERBOSITY, dest='verbosity',
                        help='the program will be more verbose on its operation (when used twice, it will print existing debug messages)')
    verbosity_group.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                                 help='the program won\'t print anything to stdout, but will still print to stderr in case of errors '
                                      '(recommended when using theme-manager in a script)')

    main_subparsers = parser.add_subparsers(title='Theme/style management', required=True)
    
    style_parser = main_subparsers.add_parser('style', help='manage the style of your system')

    sp_subparsers = style_parser.add_subparsers(title='Operations', required=True)

    spsp_enable_parser = sp_subparsers.add_parser('enable', help='enables a theme or style configuration')
    
    spspep_tar_group = spsp_enable_parser.add_mutually_exclusive_group(required=True)
    spspep_tar_group.add_argument('--global', action='store_true', dest='sty_ena_tar_glo',
                                   help='enables whatever you chose on every configured application')
    spspep_tar_group.add_argument('--application', action='store', dest='sty_ena_tar_app', metavar='APPLICATIONS',
                                   help='enables whatever you chose for the specified applications '
                                        '(write the list of applications between quotation marks and separated by a colon)')

    spspep_opt_group = spsp_enable_parser.add_mutually_exclusive_group(required=True)
    spspep_opt_group.add_argument('--theme', action='store', dest='sty_ena_req_the', metavar='THEME',
                                  help='enables the specified theme')
    # spspep_opt_group.add_argument('--font', action='store', dest='sty_ena_req_fon', metavar='FONT',
    #                               help='enables the specified font')
    
    spsp_get_parser = sp_subparsers.add_parser('get', help='gets information about style-related configuration \
                                               (this is affected by the --output-format option and doesn\'t obbey --quiet)')
    
    spspgp_group = spsp_get_parser.add_mutually_exclusive_group(required=True)
    spspgp_group.add_argument('--theme', action='store', dest='sty_get_spe_the', metavar='THEME',
                                       help='prints all possible information about one specific theme')
    spspgp_group.add_argument('--application', action='store', dest='sty_get_spe_app', metavar='APPLICATION',
                                       help='prints all possible information about one specific application')

    spspgp_group.add_argument('--current-state', action='store_true', dest='sty_get_gen_sta',
                                      help='prints the current state of all applications (what theme-manager thinks is the current state)')
    spspgp_group.add_argument('--configured-themes', action='store_true', dest='sty_get_gen_the',
                                      help='prints all configured themes and their supported applications')
    spspgp_group.add_argument('--configured-applications', action='store_true', dest='sty_get_gen_app',
                                      help='prints all configured applications and their style options')
    spspgp_group.add_argument('--dump', action='store_true', dest='sty_get_gen_dum',
                                      help='prints all the previous options combined')
    
    # preset_parser = main_subparsers.add_parser('preset', help='manages the presets for style configuration')

    # pp_subparsers = preset_parser.add_subparsers(title='Operations', required=True)

    # ppsp_create_parser = pp_subparsers.add_parser('create', help='creates a preset')
    # ppsp_create_parser.add_argument('--current', action='store_true', dest='...', 
    #                                 help='creates a preset for the current style state')

    # ppsp_get_parser = pp_subparsers.add_parser('get', help='gets information about the available presets ' 
    #                                                        '(this is affected by the --output-format option and doesn\'t obbey --quiet)')
    
    # ppspgp_group = ppsp_get_parser.add_mutually_exclusive_group(required=True)
    # ppspgp_group.add_argument('--preset', action='store', dest='...', metavar='PRESET',
    #                                    help='prints all possible information about one specific preset')
    # ppspgp_group.add_argument('--application', action='store', dest='preset_get_application', metavar='APPLICATION',
    #                                    help='prints all presets that affect a specific application')
    
    # # ppspgp_generic_group = ppsp_get_parser.add_argument_group(title='Generic').add_mutually_exclusive_group(required=True)
    # ppspgp_group.add_argument('--configured-presets', action='store_true', dest='...',
    #                                   help='prints all configured presets')
    # ppspgp_group.add_argument('--dump', action='store_true', dest='preset_get_dump', 
    #                                   help='prints all the previous options combined')

    # configuration_parser = main_subparsers.add_parser('configuration', help='manages the available configurations')
    
    return parser
