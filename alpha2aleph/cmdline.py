from .glob import __projectname__, __name__, __version__, __license__, __author__, __email__

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

    parser.add_argument('--version',
                        action="store_true",
                        help="show version number and exit")

    parser.add_argument('--about',
                        action="store_true",
                        help="show informations about the version, license, author and exit")

    parser.add_argument('--downloadbasics',
                        action="store_true",
                        help="download basic files like default symbols.txt and config.ini, and exit")

    parser.add_argument('--showsymbols',
                        action="store_true",
                        help="show symbols")

    parser.add_argument('--transform_alpha2alephrew',
                        choices=['yes', 'no'],
                        default="yes",
                        help="if 'no', do not read the input file, do not transform it")

    parser.add_argument('--inputfile',
                        type=str,
                        default="input.txt",
                        help="name of the inputfile to be read and transformed")

    parser.add_argument('--symbolsfile',
                        type=str,
                        default="symbols.txt",
                        help='name of the symbols file to be read')

    parser.add_argument('--outputformat',
                        choices=['html', 'console'],
                        default="console",
                        help="output format")

    parser.add_argument("--cfgfile",
                        type=str,
                        default="config.ini",
                        help="name of the configuration file to be read")

    parser.add_argument("--checkinputdata",
                        choices=['yes', 'no'],
                        default="yes",
                        help="if 'yes', check the coherency of the input data")

    parser.add_argument("--source",
                        choices=['stdin', 'inputfile'],
                        default="inputfile",
                        help="choose 'stdin' to use the script through a pipe")


    return parser.parse_args()
