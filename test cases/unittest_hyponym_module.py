#!/usr/bin/env python3

"""
This Python script is designed to perform unit testing of Wordhoard's
Hyponyms module.
"""
__author__ = 'John Bumgarner'
__date__ = 'September 20, 2020'
__status__ = 'Quality Assurance'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"


import unittest
import warnings
from wordhoard import Hyponyms


class TestHypernymFunction(unittest.TestCase):

    def test_hyponym_always_pass(self):
        """
        This test is designed to pass, because the word "horse" has known hyponyms
        and the default output format is a list
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsInstance(Hyponyms('horse').find_hyponyms(), list)

    def test_hyponym_always_fail(self):
        """
        This test is designed to fail, because the word "horse" has known hyponyms
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsNone(Hyponyms('horse').find_hyponyms())


unittest.main()
