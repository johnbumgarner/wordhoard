#!/usr/bin/env python3

"""
This Python script is designed to perform unit testing of WordHoard's
Antonyms module.
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
from wordhoard import Antonyms


class TestAntonymFunction(unittest.TestCase):

    def test_antonymn_always_pass(self):
        """
        This test is designed to pass, because the word "good" has known antonymns
        and the default output format is a list
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsInstance(Antonyms('good').find_antonyms(), list)

    def test_antonymn_always_fail(self):
        """
        This test is designed to fail, because the word "good" has known antonymns
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsNone(Antonyms('good').find_antonyms())


unittest.main()
