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

        transformations.py : the various transformations applied to the input
                             data.
"""
import re

from alpha2aleph.fb1d_fb4f import TRANSF_FB1D_FB4F
from alpha2aleph.utils import extracts, match_repr
from alpha2aleph.improve_rtlalphatext import IMPROVE_RTLALPHATEXT
import alpha2aleph.glob
LOGGER = alpha2aleph.glob.LOGGER


def replace_and_log(pipeline_part, comment, src, before_after):
    """
       replace_and_log()
       ________________________________________________________________________

       simply return src.replace(before, after) but with a log message
       ________________________________________________________________________

       PARAMETERS     : (str)pipeline_part
                        (str)comment
                        (str)src
                        (str, str)before_after

       RETURNED VALUE : (str)the resulting string, namely src.replace(before, after)
    """
    logger = alpha2aleph.glob.LOGGER

    before, after = before_after

    if before in src:
        # remark about logger and pipelinetrace():
        # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
        logger.pipelinetrace(pipeline_part,
                             "%s : '%s' > '%s' in %s",
                             comment, before, after, extracts(before, src))
        return src.replace(before, after)

    logger.debug("[D02] Nothing to do in '%s' for %s : '%s' > '%s' in \"%s\"",
                 src, comment, before, after, extracts(before, src))
    return src


def sub_and_log(cfgini_flag, pipeline_part, comment, before_after, src):
    """
       sub_and_log()
       ________________________________________________________________________

       simply return re.sub(before, after, src) with a log message if
       cfgini_flag.lower() == "true".
       ________________________________________________________________________

       PARAMETERS     : (str)cfgini_flag
                        (str)pipeline_part
                        (str)comment
                        (str)src
                        (str, str)before_after
                        (str)src

       RETURNED VALUE : (str)the resulting string, namely src.replace(before, after)
    """
    logger = alpha2aleph.glob.LOGGER

    before, after = before_after

    if cfgini_flag.lower() != "true":
        logger.debug("[D03] (disabled improvement) "
                     "Nothing to do in '%s' for %s : '%s' > '%s' in %s",
                     src, comment, before, after, extracts(before, src))

    res = re.sub(before, after, src)
    if src != res:
        # remark about logger and pipelinetrace():
        # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
        logger.pipelinetrace(pipeline_part,
                             "%s : '%s' > '%s' in '%s'",
                             comment, before, after, extracts(before, src))
        logger.debug("[D04] (applied improvement) '%s' > '%s' thanks to %s : '%s' > '%s' in %s",
                     src, res, comment, before, after, extracts(before, src))
        return res

    logger.debug("[D05] (no match) Nothing to do in '%s' for %s : '%s' > '%s' in %s",
                 src, comment, before, after, extracts(before, src))

    return src


def transf__text_alpha2alephsymbs(_src):
    """
       transf__text_alpha2alephsymbs()
       ________________________________________________________________________

       Convert the text <_src>, written using some alphabetic symbols, in
       a translitterated text written in hebrew.
       ________________________________________________________________________

       PARAMETERS     : (str)_src, the text to be translitterated.
                        _src is a string so that rtl_begin+_src+rtl_end
                        is the original string.

       RETURNED VALUE : (str)the translitterated text with RTL symbols added
                        at the beginning and at the end.
    """
    logger = alpha2aleph.glob.LOGGER

    src = _src.group("rtltext")

    for alphachar in alpha2aleph.glob.ALPHA2HEBREW_KEYS:
        src = replace_and_log("transf__text_alpha2alephsymbs",
                              "[transf__text_alpha2alephsymbs]",
                              src, (alphachar, alpha2aleph.glob.ALPHA2HEBREW[alphachar]))

    # remark about logger and pipelinetrace():
    # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
    logger.pipelinetrace("transf__text_alpha2alephsymbs",
                         "Adding globals.RTL_SYMBOLS to '%s' : '%s' and '%s'",
                         src,
                         alpha2aleph.globalsrtl.RTL_SYMBOLS[0],
                         alpha2aleph.globalsrtl.RTL_SYMBOLS[1])

    return alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+src+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]


def transf__improve_rtlalphatext(src):
    """
       transf__improve_rtlalphatext()
       ________________________________________________________________________

       Modify the source string <src> using different calls to sub_and_log().
       The calls are defined by IMPROVE_RTLALPHATEXT.
       ________________________________________________________________________

       PARAMETERS     : (str)_src

       RETURNED VALUE : (str) _src through several calls to sub_and_log().
    """
    # IMPROVE_RTLALPHATEXT format:
    # ˮ
    # ˮIMPROVE_RTLALPHATEXT describes various improvements available to improve the alpha-text.
    # ˮThe regex <before> is searched and replaced by the regex <after>.
    # ˮ
    # ˮ* (str) <flag> in config file::["pipeline.improve rtlalphatext"]
    # ˮ  expected value : 'True' or 'False'
    # ˮ
    # ˮ* (str) <pipeline_part> : e.g. 'transf__improve_rtlalphatext'
    # ˮ
    # ˮ* (str) <comment> : e.g. 'alef + holam > alef + point_on_right'
    # ˮ
    # ˮ* (str, a regex) <before> :
    # ˮ  e.g. "(?P<het>[H|ḥ|ħ|ẖ])(?P<accent>[<])?(?P<holam>[ô])(?P<shin>[š|ʃ])"
    # ˮ
    # ˮ* (str, a regex) <after> : e.g. "\\g<het>\\g<accent>\\g<shin>"
    for (_cfgini_flag,
         pipeline_part,
         comment,
         before,
         after) in IMPROVE_RTLALPHATEXT:

        cfgini_flag = alpha2aleph.cfgini.CFGINI["pipeline.improve rtlalphatext"][_cfgini_flag]
        src = sub_and_log(cfgini_flag, pipeline_part, comment, (before, after), src)

    return src


def transf__invert_rtltext(src):
    """
       transf__invert_rtltext()
       ________________________________________________________________________

       Invert src : "abc" becoming "cba"
       ________________________________________________________________________

       PARAMETERS     : (_sre.SRE_Match)src, the source match object.

       RETURNED VALUE : (str)_src.group("rtltext")[::-1] with RTL symbols
                        before/after.
    """
    logger = alpha2aleph.glob.LOGGER

    res = src.group("rtltext")[::-1]
    res = alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+res+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]

    # remark about logger and pipelinetrace():
    # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
    logger.pipelinetrace("transf__invert_rtltext",
                         "inverting the text : '%s' > '%s'",
                         match_repr(src), res)

    return res


def transf__use_fb1d_fb4f_chars(_src):
    """
       transf__use_fb1d_fb4f_chars()
       ________________________________________________________________________

       Modify the source string <_src> using different calls to replace_and_log()
       in order to replace some characters by those defined in the Unicode range
       0xFB1D to 0xFB4F.
       The calls are defined by fb1d_fb4f.TRANSF_FB1D_FB4F .
       The calls are controlled by the configuration file, section "pipeline.use FB1D-FB4F chars".
       ________________________________________________________________________

       PARAMETERS     : (str)_src, the source string

       RETURNED VALUE : (str)the resulting string.
    """
    logger = alpha2aleph.glob.LOGGER

    src = _src.group("rtltext")

    # ---- 1/2 FB1D-FB4F characters : ----
    for _, (fullname, before, after) in TRANSF_FB1D_FB4F:

        if alpha2aleph.cfgini.CFGINI["pipeline.use FB1D-FB4F chars"][fullname].lower() == "true":
            pipeline_part = "transf__use_fb1d_fb4f_chars"
            comment = "{0}::{1}".format("transf__use_fb1d_fb4f_chars",
                                        fullname)
            src = replace_and_log(pipeline_part, comment, src, (before, after))

    # ---- 2/2 let's add the first/last chars removed by calling this function ----
    # remark about logger and pipelinetrace():
    # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
    logger.pipelinetrace("transf__use_fb1d_fb4f_chars",
                         "Adding alpha2aleph.globalsrtl.RTL_SYMBOLS to '%s' : '%s' and '%s'",
                         src,
                         alpha2aleph.globalsrtl.RTL_SYMBOLS[0],
                         alpha2aleph.globalsrtl.RTL_SYMBOLS[1])

    return alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+src+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]
