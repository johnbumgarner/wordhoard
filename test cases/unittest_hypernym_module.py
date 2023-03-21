#!/usr/bin/env python3

"""
This Python script is designed to perform unit testing of Wordhoard's
Hypernyms module.
"""
__author__ = 'John Bumgarner'
__date__ = 'September 20, 2020'
__status__ = 'Quality Assurance'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"

##################################################################################
# Date Completed: September 20, 2020
# Author: John Bumgarner
#
# Date Last Revised:
# Revised by:
##################################################################################

##################################################################################
# “AS-IS” Clause
#
# Except as represented in this agreement, all work produced by Developer is
# provided “AS IS”. Other than as provided in this agreement, Developer makes no
# other warranties, express or implied, and hereby disclaims all implied warranties,
# including any warranty of merchantability and warranty of fitness for a particular
# purpose.
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import unittest
import warnings
from wordhoard import Hypernyms


class TestHypernymFunction(unittest.TestCase):

    def test_hypernym_always_pass(self):
        """
        This test is designed to pass, because the word "red" has known hypernyms
        and the default output format is a list
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsInstance(Hypernyms('red').find_hypernyms(), list)

    def test_hypernym_always_fail(self):
        """
        This test is designed to fail, because the word "red" has known hypernyms
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsNone(Hypernyms('red').find_hypernyms())


unittest.main()
