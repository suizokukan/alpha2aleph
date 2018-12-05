from globals import __projectname__, __name__, __version__, __license__, __author__, __email__

import argparse

def read_command_line_arguments():
    """
        read_command_line_arguments()
        ________________________________________________________________________

        Read the command line arguments.
        ________________________________________________________________________

        no PARAMETER

        RETURNED VALUE
                return the argparse object.
    """
    parser = \
      argparse.ArgumentParser(description="{0} v. {1}".format(__projectname__, __version__),
                              epilog="{0} v. {1} ({2}), "
                                     "a project by {3} "
                                     "({4})".format(__projectname__,
                                                    __version__,
                                                    __license__,
                                                    __author__,
                                                    __email__),
                              formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--showsymbols',
                        action="store_true",
                        help="show symbols")

    parser.add_argument('--no_alpha2hebrew',
                        action="store_true",
                        help="do not read the input file, do not transform it")

    parser.add_argument('--inputfile',
                        type=str,
                        default="input.txt",
                        help="…")

    parser.add_argument('--symbolsfilename',
                        type=str,
                        default="symbols.txt",
                        help='todo')

    parser.add_argument('--outputformat',
                        choices=['html', 'console'],
                        default="console",
                        help="…")

    parser.add_argument("--cfgfile",
                        type=str,
                        default="config.ini",
                        help="todo")

    parser.add_argument("--checkinputdata",
                        choices=['yes', 'no'],
                        default="yes",
                        help="todo")

    parser.add_argument("--source",
                        choices=['stdin', 'inputfile'],
                        default="inputfile",
                        help="todo")


    return parser.parse_args()
