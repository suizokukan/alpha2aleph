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

        globals.py : global declarations
"""
import re
from logger import LOGGER

def create_rtlreader_regex():

    if RTL_SYMBOLS[0] == RTL_SYMBOLS[1]:
        res = '{0}(?P<rtltext>[^{0}]*){0}'.format(re.escape(RTL_SYMBOLS[0]))
    else:
        res = '{0}(?P<rtltext>[^{0}{1}]*){1}'.format(re.escape(RTL_SYMBOLS[0]),
                                                     re.escape(RTL_SYMBOLS[1]))

    LOGGER.debug("[D05] new RTLREADER_REGEX : %s", res)

    return re.compile(res)

__projectname__ = "alphab2heb"
__version__ = "0.0.2"
__license__ = "GPLv3"
__author__ = "Xavier Faure (suizokukan)"
__email__ = "suizokukan@orange.fr"

# input file format:
# symbols used before/after hebrew text
#   nb : about rtl, see https://en.wikipedia.org/wiki/Bi-directional_text
#
# They may be equal
RTL_SYMBOLS = ("“", "”")

RTLREADER_REGEX = create_rtlreader_regex()