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

        logger.py : logging facilities
"""
import logging
import cfgini

class LoggerPlus(logging.Logger):
    """
        LoggerPlus class
    """
    def __init__(self, name, level=logging.NOTSET):
        """
                LoggerPlus.__init__()
        """
        logging.Logger.__init__(self, name, level)

    def pipelinetrace(self, pipeline_part, msg, *args, **kwargs):
        """
                LoggerPlus.pipelinetrace()

                Call Logger.info() only if the flags defined in the cfg file
                authorize a log message.
        """
        if pipeline_part in cfgini.CFGINI["pipeline.trace"]["yes"]:
            return logging.Logger.info(self, "["+pipeline_part+"] "+msg, *args, **kwargs)

        elif not pipeline_part in cfgini.CFGINI["pipeline.trace"]["no"]:
            raise RuntimeError("Undefined pipeline part '%s'.", pipeline_part)

        return None

logging.setLoggerClass(LoggerPlus)
LOGGERFORMAT = '%(levelname)-8s %(message)s'
logging.basicConfig(format=LOGGERFORMAT, level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)
