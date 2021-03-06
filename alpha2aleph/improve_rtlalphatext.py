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

        improve_rtlalphatext.py : definition of the IMPROVE_RTLALPHATEXT.
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
IMPROVE_RTLALPHATEXT = (("final kaf",
                         "transf__improve_rtlalphatext",
                         "final kaf",
                         "ḵ[:|ə](?P<ponctuation>)",
                         "ḵ²:\\g<ponctuation>"),

                        ("alef + holam > alef + point_on_right",
                         "transf__improve_rtlalphatext",
                         "alef + holam > alef + point_on_right",
                         "Aô",
                         "A°"),

                        ("ḥe + holam + shin > ḥe + shin",
                         "transf__improve_rtlalphatext",
                         "ḥe + holam + shin > ḥe + shin",
                         "(?P<het>[H|ḥ|ħ|ẖ])(?P<accent>[<])?(?P<holam>[ô])(?P<shin>[š|ʃ])",
                         "\\g<het>\\g<accent>\\g<shin>"),)
