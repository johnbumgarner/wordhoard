
"""
This Python script is designed to perform unit testing of Wordhoard's
Synonyms module.
"""
__author__ = 'John Bumgarner'
__date__ = 'September 20, 2020'
__status__ = 'Quality Assurance'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"


import unittest
import warnings
from wordhoard import Synonyms


class TestSynonymFunction(unittest.TestCase):

    def test_synonym_always_pass(self):
        """
        This test is designed to pass, because the word "good" has known synonyms
        and the default output format is a list
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsInstance(Synonyms('good').find_synonyms(), list)

    def test_synonym_always_fail(self):
        """
        This test is designed to fail, because the word "good" has known synonyms
        :return:
        """
        # this warning filter suppresses ResourceWarnings related to unclosed sockets
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        self.assertIsNone(Synonyms('good').find_synonyms())


unittest.main()
