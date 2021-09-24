#!/usr/bin/env python3

"""
This Python script is designed to perform unit testing of Wordhoard's
Antonyms module.
"""
__author__ = 'John Bumgarner'
__date__ = 'September 20, 2020'
__status__ = 'Quality Assurance'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"


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
