#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    alpha2aleph Copyright (C) 2018 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of alpha2aleph.
#    alpha2aleph is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    alpha2aleph is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with alpha2aleph.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
        alpha2aleph by suizokukan (suizokukan AT orange DOT fr)

        A (Python3/GPLv3/Linux/CLI) project, using no additional
        modules than the ones installed with Python3.

        alphabetic text → translitteration → Hebrew text

        see README.md for more documentation.
        ________________________________________________________________________

        main.py : entry point in the project.
"""
import re
import sys
import os
import os.path
import urllib.request
import shutil
import alpha2aleph.logger   # ... initialization of LOGGER

from .glob import LOGGER, ALPHA2HEBREW, ALPHA2HEBREW_KEYS
from .glob import __projectname__, __version__, __license__, __author__, __location__

import alpha2aleph.globalsrtl
from alpha2aleph.regex import get_rtlreader_regex

alpha2aleph.globalsrtl.RTLREADER_REGEX = get_rtlreader_regex()

from alpha2aleph.cfgini import CFGINI

from alpha2aleph.fb1d_fb4f import TRANSF_FB1D_FB4F

from alpha2aleph.utils import stranalyse, match_repr, extracts, extract_around_index, normpath
from alpha2aleph.cmdline import read_command_line_arguments

def add_firstlast_marker(src):
    # no id number for messages given to LOGGER.pipelinetrace(), e.g. no "[I01]".
    LOGGER.pipelinetrace("add_firstlast_marker",
                         "add markers for the first and last characters")
    return "$"+src+"$"

def remove_firstlast_marker(src):
    # no id number for messages given to LOGGER.pipelinetrace(), e.g. no "[I01]".
    LOGGER.pipelinetrace("remove_firstlast_marker",
                         "remove markers for the first and last characters")
    return src[1:-1]

def replace_and_log(pipeline_part, comment, src, before, after):
    """
        simply return src.replace(before, after) but with a log message
    """
    if before in src:
        # no id number for messages given to LOGGER.pipelinetrace(), e.g. no "[I01]".
        LOGGER.pipelinetrace(pipeline_part,
                             "%s : '%s' > '%s' in %s",
                             comment, before, after, extracts(before, src))
        return src.replace(before, after)

    LOGGER.debug("[D02] Nothing to do in '%s' for %s : '%s' > '%s' in \"%s\"",
                 src, comment, before, after, extracts(before, src))
    return src

def sub_and_log(cfgini_flag, pipeline_part, comment, before, after, src):
    """
        simply return re.sub(before, after, src) with a log message if cfgini_flag.lower() == "true"
    """
    if cfgini_flag.lower() != "true":
        LOGGER.debug("[D03] Nothing to do in '%s' for %s : '%s' > '%s' in %s",
                     src, comment, before, after, extracts(before, src))

    if before in src:
        # no id number for messages given to LOGGER.pipelinetrace(), e.g. no "[I01]".
        LOGGER.pipelinetrace(pipeline_part,
                             "%s : '%s' > '%s' in '%s'",
                             comment, before, after, extracts(before, src))
        return re.sub(before, after, src)

    LOGGER.debug("[D04] Nothing to do in '%s' for %s : '%s' > '%s' in %s",
                 src, comment, before, after, extracts(before, src))

    return src

def read_symbols(filename):
    LOGGER.debug("[D05] read_symbols : '%s'", filename)

    if not os.path.exists(filename):
        return False, ["Where is symbols file '{0}', namely '{1}' ?".format(filename, normpath(filename))], None, None

    success = True
    errors = []

    alpha2alephrew = dict()
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
                    if alpha in alpha2alephrew:
                        errors.append("key '{0}' has alread been defined; "
                                      "new definition in line {1} (line #{2})".format(alpha,
                                                                                      line,
                                                                                      line_index))
                        success = False
                    alpha2alephrew[alpha] = hebrew

    keys = sorted(alpha2alephrew.keys(), key=len, reverse=True)

    if not keys:
        success = False
        errors.append("empty alpha2alephrew dict")

    return success, errors, alpha2alephrew, keys

def transf__text_alpha2alephrew(_src):
    src = _src.group("rtltext")

    for alphachar in alpha2aleph.logger.ALPHA2HEBREW_KEYS:
        src = replace_and_log("transf__text_alpha2alephrew",
                              "[transf__text_alpha2alephrew]",
                              src, alphachar, alpha2aleph.logger.ALPHA2HEBREW[alphachar])

    # no id number for messages given to LOGGER.pipelinetrace(), e.g. no "[I01]".
    LOGGER.pipelinetrace("transf__text_alpha2alephrew",
                         "Adding globals.RTL_SYMBOLS to '%s' : '%s' and '%s'",
                         src, alpha2aleph.globalsrtl.RTL_SYMBOLS[0], alpha2aleph.globalsrtl.RTL_SYMBOLS[1])

    return alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+src+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]

def transf__improve_rtlalphatext(src):
    src = sub_and_log(alpha2aleph.cfgini.CFGINI["pipeline.improve rtlalphatext"]["final kaf"],
                      "transf__improve_rtlalphatext",
                      "final kaf",
                      "ḵ:(?P<ponctuation>)", "ḵ²:\\g<ponctuation>", src)

    src = sub_and_log(alpha2aleph.cfgini.CFGINI["pipeline.improve rtlalphatext"]["alef + holam > alef + point_on_right"],
                      "transf__improve_rtlalphatext",
                      "alef + holam > alef + point_on_right",
                      "Aô", "A°", src)

    src = sub_and_log(alpha2aleph.cfgini.CFGINI["pipeline.improve rtlalphatext"]["ḥe + holam + shin > ḥe + shin"],
                      "transf__improve_rtlalphatext",
                      "ḥe + holam + shin > ḥe + shin",
                      "ḥ(?P<accent>[<])?ôš", "ḥ\\g<accent>š", src)

    return src

def transf__invert_rtltext(src):
    res = src.group("rtltext")[::-1]
    res = alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+res+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]

    # no id number for messages given to LOGGER.pipelinetrace(), e.g. no "[I01]".
    LOGGER.pipelinetrace("transf__invert_rtltext",
                         "inverting the text : '%s' > '%s'",
                         match_repr(src), res)

    return res

def transf__use_FB1D_FB4F_chars(_src):
    src = _src.group("rtltext")

    # ---- 1/2 FB1D-FB4F characters : ----
    for shortname, (fullname, before, after) in alpha2aleph.fb1d_fb4f.TRANSF_FB1D_FB4F:

        if alpha2aleph.cfgini.CFGINI["pipeline.use FB1D-FB4F chars"][fullname].lower() == "true":
            pipeline_part = "transf__use_FB1D_FB4F_chars"
            comment = "{0}::{1}".format("transf__use_FB1D_FB4F_chars",
                                        fullname)
            src = replace_and_log(pipeline_part, comment, src, before, after)

    # ---- 2/2 let's add the first/last chars removed by calling this function ----
    # no id number for messages given to LOGGER.pipelinetrace(), e.g. no "[I01]".
    LOGGER.pipelinetrace("transf__use_FB1D_FB4F_chars",
                         "Adding alpha2aleph.globalsrtl.RTL_SYMBOLS to '%s' : '%s' and '%s'",
                         src, alpha2aleph.globalsrtl.RTL_SYMBOLS[0], alpha2aleph.globalsrtl.RTL_SYMBOLS[1])

    return alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+src+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]

def output_html(inputdata):
    LOGGER.debug("[D06] [output_html] : data to be read=%s", inputdata)

    rtl_start = '<span class="rtltext" dir="rtl">'
    rtl_end = '</span>'

    header = []
    header.append("<!DOCTYPE html>")
    header.append("")
    header.append("<html>")
    header.append("")
    header.append("<head>")
    header.append("    <title>Page Title</title>")
    header.append('    <meta http-equiv="content-type" content="text/html; charset=utf-8" />')
    header.append("    <style>")
    header.append("        body {")
    header.append('          {0}'.format(alpha2aleph.cfgini.CFGINI["output.html"]["body"]))
    header.append("          }")
    header.append("")
    header.append("        .rtltext {")
    header.append('          {0}'.format(alpha2aleph.cfgini.CFGINI["output.html"]["rtltext"]))
    header.append("        }")
    header.append("    </style>")
    header.append("</head>")
    header.append("")
    header.append("<body>")
    header.append("")
    header = "\n".join(header)

    # transformation html.1::text_delimiters
    #    let's add a char at the very beginning and at the very end of the
    #    source string.
    outputdata = add_firstlast_marker(inputdata)

    # transformation html.2::maingroup
    outputdata = transf__maingroup(outputdata)

    # transformation html.3::br
    outputdata = outputdata.replace("\n", "<br/>\n")

    # transformation html.4::RTL_SYMBOLS
    outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[0], rtl_start)
    outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[1], rtl_end)

    # transformation html.5::undo_text_delimiters
    #    see transformation html.1::text_delimiters
    outputdata = remove_firstlast_marker(outputdata)

    foot = []
    foot.append("")
    foot.append("</body>")
    foot.append("")
    foot.append("</html>")
    foot = "\n".join(foot)

    return header + outputdata + foot

def output_console(inputdata):
    LOGGER.debug("[D07] [output_console] : data to be read=%s", inputdata)

    # transformation console.1::text_delimiters
    #    let's add a char at the very beginning and at the very end of the
    #    source string.
    outputdata = add_firstlast_marker(inputdata)

    # transformation console.2::maingroup
    outputdata = transf__maingroup(outputdata)

    # transformation console.3::invert_rtltext
    if alpha2aleph.cfgini.CFGINI["output.console"]["invert_rtltext"].lower() == 'true':
        outputdata = re.sub(alpha2aleph.globalsrtl.RTLREADER_REGEX, transf__invert_rtltext, outputdata)

    # transformation console.4::remove_RTL_SYMBOLS
    # https://en.wikipedia.org/wiki/Bi-directional_text
    if alpha2aleph.cfgini.CFGINI["output.console"]["rtl symbols"].lower() == "0x200f_0x200e":
        outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[0], chr(0x200F))
        outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[1], chr(0x200E))

    elif alpha2aleph.cfgini.CFGINI["output.console"]["rtl symbols"].lower() == "empty string":
        outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[0], "")
        outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[1], "")

    # transformation console.5::undo_text_delimiters
    outputdata = remove_firstlast_marker(outputdata)

    # transformation console.6::use fribidi
    if alpha2aleph.cfgini.CFGINI["output.console"]["use fribidi"].lower() == "true":
        import pyfribidi
        outputdata = pyfribidi.log2vis(outputdata)

    return outputdata

def transf__maingroup(src):
    LOGGER.debug("[D08] transf__maingroup()")

    # transformation maingroup.1::improve_rtlalphatext
    src = transf__improve_rtlalphatext(src)

    # transformation maingroup.2::transf__text_alpha2alephrew
    src = re.sub(alpha2aleph.globalsrtl.RTLREADER_REGEX, transf__text_alpha2alephrew, src)

    # transformation maingroup.3::transf__use_FB1D_FB4F_chars
    src = re.sub(alpha2aleph.globalsrtl.RTLREADER_REGEX, transf__use_FB1D_FB4F_chars, src)

    return src

def check_inputdata(inputdata):
    LOGGER.debug("[D09] check_inputdata()")

    success = True
    errors = []

    # ------------------------------------------------------------------------
    # ---- a special case : no check if RTL_SYMBOLS[0]==RTL_SYMBOLS[1]
    # ------------------------------------------------------------------------
    if alpha2aleph.globalsrtl.RTL_SYMBOLS[0] == alpha2aleph.globalsrtl.RTL_SYMBOLS[1]:
        return True, []

    # ------------------------------------------------------------------------
    # ---- common case : RTL_SYMBOLS[0] != RTL_SYMBOLS[1]
    # ------------------------------------------------------------------------
    # first check : is num_of(globals.RTL_SYMBOLS[0]) equal to num_of(globals.RTL_SYMBOLS[1]) ?
    if inputdata.count(alpha2aleph.globalsrtl.RTL_SYMBOLS[0]) != inputdata.count(alpha2aleph.globalsrtl.RTL_SYMBOLS[1]):
        success = False
        errors.append("Not even numbers of symbols '{0}' and '{1}'".format(alpha2aleph.globalsrtl.RTL_SYMBOLS[0],
                                                                           alpha2aleph.globalsrtl.RTL_SYMBOLS[1]))

    # second check : no two globals.RTL_SYMBOLS[x] twice in a row
    # third check : first RTL_SYMBOL must be globals.RTL_SYMBOLS[0]
    last_symbol = None
    for line_number, line in enumerate(inputdata):
        for char_number, char in enumerate(line):

            context = 'line #{0}::character {1} (\"{2}\")'.format(line_number+1, char_number+1, extract_around_index(line, char_number))

            if char in alpha2aleph.globalsrtl.RTL_SYMBOLS:
                if last_symbol is None:
                    if char == alpha2aleph.globalsrtl.RTL_SYMBOLS[1]:
                        errors.append("first RTL_SYMBOL must be {0}, not {1} (context={2})".format(alpha2aleph.globalsrtl.RTL_SYMBOLS[0],
                                                                                                   alpha2aleph.globalsrtl.RTL_SYMBOLS[1],
                                                                                                   context))
                        success = False
                    else:
                        last_symbol = char
                else:
                    if last_symbol == char:
                        LOGGER.error("[E01] the symbol '%s' appears two times in a row (context=%s)", char, context)
                        success = False
                    last_symbol = char

    return success, errors

def downloadbasics():
    """
        downloadbasics()
        ________________________________________________________________________

        Download the default configuration file and save them in the current
        directory.
        ________________________________________________________________________

        no PARAMETER

        RETURNED VALUE :
            (bool) success
    """
    success = True

    for filename, url in (('config.ini', 'https://raw.githubusercontent.com/suizokukan/alpha2aleph/master/examples/config.ini'),
                          ('symbols.txt', 'https://raw.githubusercontent.com/suizokukan/alpha2aleph/master/examples/symbols.txt')):
        try:
            with urllib.request.urlopen(url) as response, \
                 open(filename, 'wb') as out_file:
                 shutil.copyfileobj(response, out_file)

                 # no id number (e.g. no [I01])
                 LOGGER.info("Downloaded '%s' as '%s'", filename, normpath(filename))

        except urllib.error.URLError as exception:
            success = False

    return success

def entrypoint(paramaters=None):
    """
        entrypoint()
        ________________________________________________________________________

        main entry point into alpha2aleph.
        ________________________________________________________________________

        paramaters : either None (cfgfile, ... will be read from the command line)
                     either a list of strings (cfgfile, symbolsfile, inputdata, "console|html").

        returned value : a str if no error occured, None otherwise
    """
    # --------------------------------------
    # ---- (0/4) command line arguments ----
    # --------------------------------------
    if paramaters is None:
        args = read_command_line_arguments()

    # ----------------------------------------------------
    # ---- (1/4) --version, --about, --downloadbasics ----
    # ----------------------------------------------------
    if paramaters is None:
        if args.version:
            print(__version__)
            sys.exit(0)

        if args.about:
            __projectname__, __license__, __author__, __location__
            print("{0} v. {1} by {2} : see {3}; a {4} project".format(__projectname__,
                                                                      __version__,
                                                                      __author__,
                                                                      __location__,
                                                                      __license__))
            sys.exit(0)

        if args.downloadbasics:
            downloadbasics()
            sys.exit(0)

    # ----------------------------------
    # ---- (1/4) configuration file ----
    # ----------------------------------
    if paramaters is None:
        cfgini_success, cfgerrors, alpha2aleph.cfgini.CFGINI = alpha2aleph.cfgini.read_cfg_file(args.cfgfile)

        if not cfgini_success:
            LOGGER.error("[E02] problem with the config file '%s' : %s", args.cfgfile, cfgerrors)
            LOGGER.error("[E03] === program stops ===")
            sys.exit(-1)

    else:
        cfgini_success, cfgerrors, alpha2aleph.cfgini.CFGINI = alpha2aleph.cfgini.read_cfg_file(paramaters[0])
        if not cfgini_success:
            return None

    # ----------------------------
    # ---- (2/4) symbols file ----
    # ----------------------------
    if paramaters is None:
        readsymbols_success, readsymbols_errors, alpha2aleph.logger.ALPHA2HEBREW, alpha2aleph.logger.ALPHA2HEBREW_KEYS = read_symbols(args.symbolsfile)

        if not readsymbols_success:
            LOGGER.error("[E04] problem with the symbols file '%s' : %s", args.symbolsfile, readsymbols_errors)
            LOGGER.error("[E05] === program stops ===")
            sys.exit(-3)

    else:
        readsymbols_success, readsymbols_errors, alpha2aleph.logger.ALPHA2HEBREW, alpha2aleph.logger.ALPHA2HEBREW_KEYS = read_symbols(paramaters[1])
        if not readsymbols_success:
            return None

    if paramaters is None:
        if args.showsymbols:
            for key in alpha2aleph.logger.ALPHA2HEBREW_KEYS:
                print(stranalyse(key), "---→", stranalyse(alpha2aleph.logger.ALPHA2HEBREW[key]))

    # -----------------------------------
    # ---- (3/4) input data reading  ----
    # -----------------------------------
    inputdata = ""
    if paramaters is None:
        if args.source == "inputfile":
            if not os.path.exists(args.inputfile):
                LOGGER.error("[E06] Where is input file '%s', namely '%s' ?", args.inputfile, normpath(args.inputfile))
                LOGGER.error("[E07] === program stops ===")
                sys.exit(-4)
            else:
                with open(args.inputfile) as inputfile:
                    inputdata = inputfile.readlines()
        elif args.source == "stdin":
            #
            inputdata = sys.stdin.read()
            if inputdata[-1] == "\n":
                inputdata = inputdata[:-1]
    else:
        inputdata = paramaters[2]

    if paramaters is None:
        if args.checkinputdata == 'yes':
            check_success, check_errors = check_inputdata(inputdata)
            if not check_success:
                LOGGER.error("[E08] Ill-formed input data '%s'; error(s)=%s", args.cfgfile, check_errors)
                LOGGER.error("[E09] === program stops ===")
                sys.exit(-2)

    # ----------------------------------------
    # ---- (4/4) input data > output data ----
    # ----------------------------------------
    if paramaters is None:
        if args.transform_alpha2alephrew == 'yes':
            if args.outputformat == 'console':
                res = output_console("".join(inputdata))
                print(res)
                return res
            if args.outputformat == 'html':
                res = output_html("".join(inputdata))
                print(res)
                return res
    else:
        if paramaters[3] == "console":
            return output_console("".join(inputdata))
        elif paramaters[3] == "html":
            return output_html("".join(inputdata))

#if __name__ == '__main__':
#    entrypoint()
