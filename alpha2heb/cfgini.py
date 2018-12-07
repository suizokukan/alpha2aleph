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

        cfgini.py : read the configuration file.
"""
import configparser
import globals

def read_cfg_file(filename):
    """
        read_cfg_file()

        Read the config file <filename>.

        PARAMETER : (str)filename

        RETURNED VALUE : (bool_success, configparser.ConfigParser object)
    """
    success = True
    errors = []
    cfgini = configparser.ConfigParser()

    try:
        cfgini.read(filename)
    except configparser.DuplicateOptionError as err:
        success = False
        errors.append("Ill-formed config file '{0}' : duplicate key {1}".format(filename, err))

    if success:
        try:
            # let's check the presence of some values :
            _ = cfgini["output.console"]
            _ = cfgini["output.console"]["invert_rtltext"]

            _ = cfgini["pipeline.trace"]
            _ = cfgini["pipeline.trace"]["yes"]
            _ = cfgini["pipeline.trace"]["no"]

            _ = cfgini["pipeline.use FB1D-FB4F chars"]

            _ = cfgini["pipeline.improve rtltext"]
            _ = cfgini["pipeline.improve rtltext"]["final kaf"]
            _ = cfgini["pipeline.improve rtltext"]["alef + holam > alef + point_on_right"]
            _ = cfgini["pipeline.improve rtltext"]["ḥe + holam + shin > ḥe + shin"]

        except KeyError as err:
            success = False
            errors.append("Ill-formed config file '{0}' : missing key {1}".format(filename, err))

    if success:
        globals.RTL_SYMBOLS = (cfgini["inputdata.format"]["RTL_SYMBOL_START"],
                               cfgini["inputdata.format"]["RTL_SYMBOL_END"])
        globals.RTLREADER_REGEX = globals.create_rtlreader_regex()

    return success, errors, cfgini

# should be initialized by read_cfg_file()
CFGINI = None