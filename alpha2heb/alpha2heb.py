#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    alpha2heb Copyright (C) 2018 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of alpha2heb.
#    alpha2heb is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    alpha2heb is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with alpha2heb.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
        alpha2heb by suizokukan (suizokukan AT orange DOT fr)

        A (Python3/GPLv3/Linux/CLI) project, using no additional
        modules than the ones installed with Python3.

        alphabetic text → translitteration → Hebrew text

        see README.md for more documentation.
        ________________________________________________________________________

        alphaheb.py : entry point in the project.
"""
import argparse
import configparser
import logging
import logging.config
import re
import sys
import unicodedata

import globals
from globals import __projectname__, __name__, __version__, __license__, __author__, __email__,  create_rtlreader_regex

from logger import LOGGER
import cfgini

import fb1d_fb4f

def stranalyse(src):
    res = []
    for char in src:
        name = unicodedata.name(char)
        res.append('\"{0}\"(#{1})={2}'.format(char,
                                              hex(ord(char)),
                                              name))
    return ";".join(res)

def add_firstlast_marker(src):
    LOGGER.pipelinetrace("add_firstlast_marker",
                         "add markers for the first and last characters")
    return "$"+src+"$"

def remove_firstlast_marker(src):
    LOGGER.pipelinetrace("remove_firstlast_marker",
                         "remove markers for the first and last characters")
    return src[1:-1]

def match_repr(match):
    """
        Return a human readable representation of <match>
    """
    return "(indexes {0} to {1}) : '{2}'".format(match.start(), match.end(), match.group())

def extract_around_index(string, index, amplitude=10):
    index0 = max(0, index-amplitude)
    index1 = min(len(string)-1, index+amplitude)

    before = "…"
    if index0 == 0:
        before = ""

    after = "…"
    if index1 == len(string)-1:
        after = ""

    return before+string[index0:index1]+after

def extracts(target, src, amplitude=10):
    res = []
    for _res in re.finditer(target, src):
        index0 = _res.start()
        _index0 = max(0, index0 - amplitude)

        index1 = _res.end()
        _index1 = min(len(src)-1, index1 + amplitude)

        res.append("…" + src[_index0:index0] + _res.group() + src[index1:_index1] + "…")

    finalres = []
    for i, _res in enumerate(res):
        finalres.append("(#{0}) : \"{1}\"".format(i, _res))

    return " /// ".join(finalres)

def replace_and_log(pipeline_part, comment, src, before, after):
    """
        simply return src.replace(before, after) but with a log message
    """
    if before in src:
        LOGGER.pipelinetrace(pipeline_part,
                             "%s : '%s' > '%s' in %s",
                             comment, before, after, extracts(before, src))
        return src.replace(before, after)

    LOGGER.debug("[D01] Nothing to do in '%s' for %s : '%s' > '%s' in %s",
                 src, comment, before, after, extracts(before, src))
    return src

def sub_and_log(pipeline_part, comment, before, after, src):
    """
        simply return re.sub(before, after, src) with a log message
    """
    if before in src:
        LOGGER.pipelinetrace(pipeline_part,
                             "%s : '%s' > '%s' in '%s'",
                             comment, before, after, extracts(before, src))
        return re.sub(before, after, src)

    LOGGER.debug("[D02] Nothing to do in '%s' for %s : '%s' > '%s' in %s",
                 src, comment, before, after, extracts(before, src))

    return src


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

def read_symbols(filename):
    success = True
    errors = []

    alpha2hebrew = dict()
    with open(filename) as symbols:
        for line_index, _line in enumerate(symbols.readlines()):
            line = _line.strip()

            if '#' in line:
                line = line[:line.index('#')]
                line = line.strip()

            if line != "":
                if '→' in line:
                    alpha, hebrew = line.split("→")
                    alpha = alpha.strip()
                    hebrew = hebrew.strip()
                    if alpha in alpha2hebrew:
                        errors.append("key '{0}' has alread been defined; new definition in line {1} (line #{2})".format(alpha, line, line_index))
                        success = False
                    alpha2hebrew[alpha] = hebrew

    keys = sorted(alpha2hebrew.keys(), key=len, reverse=True)

    if not keys:
        success = False
        errors.append("empty alpha2hebrew dict")

    return success, errors, alpha2hebrew, keys

def transf__text_alpha2hebrew(_src):
    src = _src.group("rtltext")

    for alphachar in ALPHA2HEBREW_KEYS:
        src = replace_and_log("transf__text_alpha2hebrew",
                              "[transf__text_alpha2hebrew]",
                              src, alphachar, ALPHA2HEBREW[alphachar])

    LOGGER.pipelinetrace("transf__text_alpha2hebrew",
                         "Adding globals.RTL_SYMBOLS to '%s' : '%s' and '%s'",
                         src, globals.RTL_SYMBOLS[0], globals.RTL_SYMBOLS[1])

    return globals.RTL_SYMBOLS[0]+src+globals.RTL_SYMBOLS[1]

def transf__improve_rtltext(src):

    src = sub_and_log("transf__improve_rtltext",
                      "final kaf:",
                      "ḵ:(?P<ponctuation>)", "ḵ²:\\g<ponctuation>", src)

    src = sub_and_log("transf__improve_rtltext",
                      "alef + holam > alef + point_on_right",
                      "Aô", "A°", src)

    src = sub_and_log("transf__improve_rtltext",
                      "ḥe + holam + shin > ḥe + shin",
                      "ḥ(?P<accent>[<])?ôš", "ḥ\\g<accent>š", src)

    return src

def transf__invert_text(src):
    res = src.group("rtltext")[::-1]
    res = globals.RTL_SYMBOLS[0]+res+globals.RTL_SYMBOLS[1]

    LOGGER.pipelinetrace("transf__invert_text",
                         "inverting the text : '%s' > '%s'",
                         match_repr(src), res)

    return res


def transf__use_FB1D_FB4F_chars(_src):

    src = _src.group("rtltext")

    # ---- 1/2 FB1D-FB4F characters : ----
    for shortname, (fullname, before, after) in fb1d_fb4f.TRANSF_FB1D_FB4F:

        if cfgini.CFGINI["pipeline.use FB1D-FB4F chars"][fullname].lower() == "true":
            pipeline_part = "transf__use_FB1D_FB4F_chars"
            comment = "{0}::{1}".format("transf__use_FB1D_FB4F_chars",
                                        fullname)
            src = replace_and_log(pipeline_part, comment, src, before, after)

    # ---- 2/2 let's add the first/last chars removed by calling this function ----
    LOGGER.pipelinetrace("transf__use_FB1D_FB4F_chars",
                         "Adding globals.RTL_SYMBOLS to '%s' : '%s' and '%s'",
                         src, globals.RTL_SYMBOLS[0], globals.RTL_SYMBOLS[1])

    return globals.RTL_SYMBOLS[0]+src+globals.RTL_SYMBOLS[1]

def output_html(inputdata):
    LOGGER.debug("[D03] [output_html] : data to be read=%s", inputdata)

    RTL_START = '<span dir="rtl">'
    RTL_END = '</span>'

    header = []
    header.append("<!DOCTYPE html>")
    header.append("")
    header.append("<html>")
    header.append("")
    header.append("<head>")
    header.append("    <title>Page Title</title>")
    header.append('    <meta http-equiv="content-type" content="text/html; charset=utf-8" />')
    header.append("</head>")
    header.append("")
    header.append("<body>")
    header.append("")
    header = "\n".join(header)

    # transformation html.1::text_delimiters
    #    let's add a char at the very beginning and at the very end of the
    #    source string.
    inputdata = add_firstlast_marker(inputdata)

    # transformation html.2::main
    inputdata = transf__maingroup(inputdata)

    # transformation html.3::\n
    inputdata = inputdata.replace("\n", "<br/>\n")

    # transformation html.4::globals.RTL_SYMBOLS
    inputdata = inputdata.replace(globals.RTL_SYMBOLS[0], RTL_START)
    inputdata = inputdata.replace(globals.RTL_SYMBOLS[1], RTL_END)

    # transformation console.5::undo_text_delimiters
    #    see transformation html.1::text_delimiters
    inputdata = remove_firstlast_marker(inputdata)

    foot = []
    foot.append("")
    foot.append("</body>")
    foot.append("")
    foot.append("</html>")
    foot = "\n".join(foot)

    return header + inputdata + foot

def output_console(inputdata):
    LOGGER.debug("[D04] [output_console] : data to be read=%s", inputdata)

    # transformation console.1::text_delimiters
    #    let's add a char at the very beginning and at the very end of the
    #    source string.
    inputdata = add_firstlast_marker(inputdata)

    # transformation console.2::main
    inputdata = transf__maingroup(inputdata)

    # transformation console.3::rtltext
    if cfgini.CFGINI["output.console"]["invert_rtltext"] == 'True':
        inputdata = re.sub(globals.RTLREADER_REGEX, transf__invert_text, inputdata)

    # transformation console.4::globals.RTL_SYMBOLS
    # https://en.wikipedia.org/wiki/Bi-directional_text
    inputdata = inputdata.replace(globals.RTL_SYMBOLS[0], "")
    inputdata = inputdata.replace(globals.RTL_SYMBOLS[1], "")

    # transformation console.4::undo_text_delimiters
    #    see console.1::text_delimiters
    inputdata = remove_firstlast_marker(inputdata)

    return inputdata

def transf__maingroup(src):

    # transformation maingroup.1::improve_rtltext
    src = transf__improve_rtltext(src)

    # transformation maingroup.2::transf__text_alpha2hebrew
    src = re.sub(globals.RTLREADER_REGEX, transf__text_alpha2hebrew, src)

    # transformation maingroup.3::transf__use_FB1D_FB4F_chars
    src = re.sub(globals.RTLREADER_REGEX, transf__use_FB1D_FB4F_chars, src)

    return src

def check_inputdata(inputdata):
    success = True
    errors = []

    # ------------------------------------------------------------------------
    # ---- a special case : no check if RTL_SYMBOLS[0]==RTL_SYMBOLS[1]
    # ------------------------------------------------------------------------
    if globals.RTL_SYMBOLS[0] == globals.RTL_SYMBOLS[1]:
        return True, []

    # ------------------------------------------------------------------------
    # ---- common case : RTL_SYMBOLS[0] != RTL_SYMBOLS[1]
    # ------------------------------------------------------------------------
    # first check : is num_of(globals.RTL_SYMBOLS[0]) equal to num_of(globals.RTL_SYMBOLS[1]) ?
    if inputdata.count(globals.RTL_SYMBOLS[0]) != inputdata.count(globals.RTL_SYMBOLS[1]):
        success = False
        errors.append("Not even numbers of symbols '{0}' and '{1}'".format(globals.RTL_SYMBOLS[0],
                                                                           globals.RTL_SYMBOLS[1]))

    # second check : no two globals.RTL_SYMBOLS[x] twice in a row
    # third check : first RTL_SYMBOL must be globals.RTL_SYMBOLS[0]
    last_symbol = None
    for line_number, line in enumerate(inputdata):
        for char_number, char in enumerate(line):

            context = 'line #{0}::character {1} (\"{2}\")'.format(line_number+1, char_number+1, extract_around_index(line, char_number))

            if char in globals.RTL_SYMBOLS:
                if last_symbol is None:
                    if char == globals.RTL_SYMBOLS[1]:
                        errors.append("first RTL_SYMBOL must be {0}, not {1} (context={2})".format(globals.RTL_SYMBOLS[0],
                                                                                                   globals.RTL_SYMBOLS[1],
                                                                                                   context))
                        success = False
                    else:
                        last_symbol = char
                else:
                    if last_symbol == char:
                        LOGGER.error("[E01] the symbol '{0}' appears two times in a row (context={1})".format(char, context))
                        success = False
                    last_symbol = char

    return success, errors


##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

ARGS = read_command_line_arguments()

CFGINI_SUCCESS, CFGERRORS, cfgini.CFGINI = cfgini.read_cfg_file(ARGS.cfgfile)

if not CFGINI_SUCCESS:
    LOGGER.error("[E02] Ill-formed config file '%s' : %s", ARGS.cfgfile, CFGERRORS)
    LOGGER.error("[E03] === program stops ===")
    sys.exit(-1)

READSYMBOLS_SUCCESS, READSYMBOLS_ERRORS, ALPHA2HEBREW, ALPHA2HEBREW_KEYS = read_symbols(ARGS.symbolsfilename)

if not READSYMBOLS_SUCCESS:
    LOGGER.error("[E04] ill-formed symbole file '%s' : %s", ARGS.symbolsfilename, READSYMBOLS_ERRORS)
    LOGGER.error("[E05] === program stops ===")
    sys.exit(-3)

if ARGS.showsymbols:
    for key in ALPHA2HEBREW_KEYS:
        print(stranalyse(key), "---→", stranalyse(ALPHA2HEBREW[key]))

INPUTDATA = ""
if ARGS.source == "inputfile":
    with open(ARGS.inputfile) as inputfile:
        INPUTDATA = inputfile.readlines()
elif ARGS.source == "stdin":
    INPUTDATA = sys.stdin.read()

if ARGS.checkinputdata == 'yes':
    check_success, check_errors = check_inputdata(INPUTDATA)
    if not check_success:
        LOGGER.error("[E06] Ill-formed input data '%s'; error(s)=%s", ARGS.cfgfile, check_errors)
        LOGGER.error("[E07] === program stops ===")
        sys.exit(-2)

# input > output
if not ARGS.no_alpha2hebrew:

    if ARGS.outputformat == 'console':
        print(output_console("".join(INPUTDATA)))
    if ARGS.outputformat == 'html':
        print(output_html("".join(INPUTDATA)))
