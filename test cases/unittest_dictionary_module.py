#!/usr/bin/env python3

"""
This Python script is designed to perform unit testing of Wordhoard's
Dictionary module.
"""
__author__ = 'John Bumgarner'
__date__ = 'September 20, 2020'
__status__ = 'Quality Assurance'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"


import unittest
import warnings
from wordhoard import Definitions


class TestDefinitionFunction(unittest.TestCase):

    def test_definition_always_pass(self):
        """
        This test is designed to pass, because the word "mother" has a known definition
        and the default output format is a list
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsInstance(Definitions('mother').find_definitions(), list)

    def test_definition_always_fail(self):
        """
        This test is designed to fail, because the word "mother" has a known definition
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsNone(Definitions('mother').find_definitions())


unittest.main()
