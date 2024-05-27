#!/usr/bin/env python3

"""
This Python module is designed to query internal repositories for the
homophones associated with the given word.
"""
__author__ = 'John Bumgarner'
__date__ = 'June 11, 2021'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"

##################################################################################
# Date Completed: June 11, 2021
# Author: John Bumgarner
#
# Date Last Revised: May 09, 2024
# Revised by: John Bumgarner
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
# Standard library imports
import os
import sys
import pickle
import logging
import traceback
from typing import List, Union

# Local or project-specific imports
from wordhoard.utilities import word_verification
from wordhoard.utilities.colorized_text import colorized_text

logger = logging.getLogger(__name__)

# Define module-level variables to store loaded data
_known_homophones_list = []
_no_homophones_list = []

class PickleLoader:
    """
        A utility class for loading pickle files containing English homophones and
        English words with no known homophones.
    """

    @staticmethod
    def load_pickle_files() -> None:
        """
            Loads pickle files containing English homophones and English words with no known homophones.

            :returns: None
            :rtype: NoneType
        """
        global _known_homophones_list, _no_homophones_list
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        _file_known_homophones = os.path.join(parent_directory, 'files/common_english_homophones.pkl')
        _file_no_known_homophones = os.path.join(parent_directory, 'files/no_homophones_english.pkl')

        try:
                # Opening the pickle file that contains a nested list of common
                # English language homophones.
            with open(file=_file_known_homophones, mode='rb') as _eng_homophones:
                _known_homophones_list = pickle.load(file=_eng_homophones)
        except (FileNotFoundError, OSError) as error:
            PickleLoader.handle_pickle_load_error(_file_known_homophones, error)

        try:
            # Opening the pickle file that contains a nested list of English
            # language words that have no known homophones.
            with open(file=_file_no_known_homophones, mode='rb') as _no_eng_homophones:
                _no_homophones_list = pickle.load(file=_no_eng_homophones)
        except (FileNotFoundError, OSError) as error:
            PickleLoader.handle_pickle_load_error(_file_no_known_homophones, error)

    @staticmethod
    def handle_pickle_load_error(file_path: str, error: Exception) -> None:
        """
            Handles errors when loading pickle files.

            :arg file_path: The path of the pickle file.
            :arg type file_path: str
            :arg error: The error raised during file loading.
            :arg type error: Exception
            :returns: None
            :rtype; NoneType
        """
        if isinstance(error, FileNotFoundError):
            logger.error(f'The pickle file {file_path} was not found. Aborting operation.')
        else:
            logger.error(f"An OS error occurred when trying to open the pickle file {file_path}")
        logger.error(''.join(traceback.format_tb(error.__traceback__)))
        sys.exit(1)

PickleLoader.load_pickle_files()

class Homophones:
    """
        Purpose
        ----------
        This Python class is used to query internal files containing
        English language homophones associated with a specific word.

        Usage Examples
        ----------
        >>> homophones = Homophones('horse')
        >>> results = homophones.find_homophones()

        Parameters
        ----------
        :param search_string: string containing the variable to obtain homophones for
        """

    def __init__(self,
                 search_string: str = ''):

        self._word = search_string

    def _validate_word(self) -> bool:
        """
        This function is designed to validate that the syntax for
        a string variable is in an acceptable format.

        :return: True or False
        :rtype: boolean
        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if not valid_word:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')
        return valid_word

    def _common_english_homophones(self) -> List[str]:
        """
        This function iterates through a list of known
        English language homophones.

        :return: list of homophones
        :rtype: list
        """
        homophones_list = []
        for homophones in _known_homophones_list:
            if any(word == self._word for word in homophones):
                homophones_list.extend(
                    f'{self._word} is a homophone of {word}' for word in homophones if word != self._word)
        return list(set(homophones_list))

    def _english_words_without_homophones(self) -> bool:
        """
        This function iterates through a list of English
        language words with no known homophones.

        :return: True or False
        :rtype: bool
        """
        return self._word in _no_homophones_list

    def find_homophones(self) -> Union[List[str], None]:
        """
        This function queries multiple lists to find English language homophones associated
        with the specific word provided to the Class Homophones.

        :return: list of homophones
        :rtype: Union[List[str]
        """
        if self._validate_word():
            known_english_homophones = self._common_english_homophones()
            if known_english_homophones:
                return known_english_homophones
            elif self._english_words_without_homophones() is False:
                colorized_text(text=f'No homophones for the word - {self._word}', color='magenta')
                return None
        return None
