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
