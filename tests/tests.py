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

        tests/tests.py : unit tests.
"""
import unittest
import os.path

from alpha2aleph.main import entrypoint


class Tests(unittest.TestCase):
    """
        Tests class

        Main test class of the project.
    """
    def test1(self):
        """
            Tests.test1()

            Simple test : "“mlḵ”" -> "כלמ"
        """
        res = entrypoint((os.path.join("tests", "config1.ini"),
                          os.path.join("tests", "symbols1.txt"),
                          "“mlḵ”",
                          "console",))
        self.assertEqual(res, "כלמ")
