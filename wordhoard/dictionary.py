#!/usr/bin/env python3

"""
This Python script is designed to query multiple online repositories for the
definition associated with a given word.
"""
__author__ = 'John Bumgarner'
__date__ = 'October 15, 2020'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"

##################################################################################
# Date Completed: October 15, 2020
# Author: John Bumgarner
#
# Date Last Revised: July 3, 2021
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
import bs4
import logging
import requests
import traceback
import re as regex
from bs4 import BeautifulSoup
from wordhoard.utilities import basic_soup, caching, cleansing, word_verification

logger = logging.getLogger(__name__)


class Definitions:
    """
    This class is used to query multiple online repositories for the
    definition associated with a specific word.

    Usage:
      definition = Definitions(word)
      results = definition.find_definitions()
    """

    def __init__(self, search_string):
        """
        :param search_string: string containing the variable to search for
        """
        self._word = search_string

    def _validate_word(self):
        """
        This function is designed to validate that the syntax for
        a string variable is in an acceptable format.

        :return: True or False
        :rtype: bool
        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if valid_word:
            return valid_word
        else:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')

    def _update_cache(self, definition):
        caching.insert_word_cache_definition(self._word, definition)
        return

    def find_definitions(self):
        """
        This function queries multiple online repositories to discover
        definitions related with the specific word provided to the
        Class Definitions.

        :return: list of definitions
        :rtype: list
        """
        valid_word = self._validate_word()
        if valid_word:
            check_cache = caching.cache_antonyms(self._word)
            if check_cache is False:
                definition_01 = self._query_synonym_com()
                definition_02 = self._query_collins_dictionary()
                definition_03 = self._query_thesaurus_com()
                definitions = ([x for x in [definition_01, definition_02, definition_03] if x is not None])
                return sorted(set(definitions))
            else:
                definitions = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
                return definitions

    def _query_synonym_com(self):
        """
        This function queries synonym_com for a definition associated
        with the specific word provided to the Class Definitions.

         :returns:
            definition: definition for a word

        :rtype: string

        :raises
            AttributeError: Raised when an attribute reference or assignment fails.

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

            TypeError: Raised when an operation or function is applied to an object of inappropriate type.

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            results_definition = basic_soup.get_single_page_html(
                f'https://www.synonym.com/synonyms/{self._word}')
            soup = BeautifulSoup(results_definition, "lxml")
            description_tag = soup.find("meta", property="og:description")
            if 'find any words based on your search' not in description_tag['content']:
                find_definition = regex.split(r'\|', description_tag['content'])
                definition_list = find_definition[1].lstrip().replace('definition:', '').split(',')
                definition = [cleansing.normalize_space(i) for i in definition_list]
                definition_list_to_string = ' '.join([str(elem) for elem in definition])
                self._update_cache(definition_list_to_string)
                return definition_list_to_string
            else:
                logger.error(f'synonym.com had no reference for the word {self._word}')
        except bs4.FeatureNotFound as error:
            logger.error('An error occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except AttributeError as error:
            logger.error('An AttributeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except KeyError as error:
            logger.error('A KeyError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except TypeError as error:
            logger.error('A TypeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _query_collins_dictionary(self):
        """
        This function queries collinsdictionary.com for a definition associated
        with the specific word provided to the Class Definitions.

         :returns:
            definition: definition for a word

        :rtype: str

        :raises
            AttributeError: Raised when an attribute reference or assignment fails.

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

            TypeError: Raised when an operation or function is applied to an object of inappropriate type.

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            results_definition = basic_soup.get_single_page_html(
                f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}')
            query_results = basic_soup.query_html(results_definition, 'div', 'class',
                                                  'form type-def titleTypeSubContainer')
            if query_results is not None:
                definition = query_results.findNext('div', {'class': 'def'})
                self._update_cache(definition.text)
                return definition.text
            else:
                logger.error(f'Collins Dictionary had no reference for the word {self._word}')
        except bs4.FeatureNotFound as error:
            logger.error('An error occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except AttributeError as error:
            logger.error('An AttributeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except KeyError as error:
            logger.error('A KeyError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except TypeError as error:
            logger.error('A TypeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _query_thesaurus_com(self):
        """
        This function queries thesaurus.com for a definition associated
        with the specific word provided to the Class Definitions.

        :returns:
            definition: definition for a word

        :rtype: str

        :raises

            IndexError: Raised when a sequence subscript is out of range.

            requests.ConnectionError: Raised when a connection error has occurred.

            requests.HTTPError: Raised when an HTTP error has occurred.

            requests.RequestException: Raised when an unknown error has occurred.

            requests.Timeout: Raised when the request timed out.
        """
        try:
            req = requests.get(f'https://tuna.thesaurus.com/pageData/{self._word}',
                               headers=basic_soup.http_headers,
                               allow_redirects=True, verify=True, timeout=30)
            if req.json()['data'] is not None:
                definition = req.json()['data']['definitionData']['definitions'][0]['definition']
                self._update_cache(definition)
                return definition
            else:
                logger.error(f'thesaurus.com had no reference for the word {self._word}')
        except requests.HTTPError as error:
            logger.error('A HTTP error has occurred.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except requests.ConnectionError as error:
            if requests.codes:
                'Failed to establish a new connection'
                logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except requests.Timeout as error:
            logger.error('A connection timeout has occurred.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except requests.RequestException as error:
            logger.error('An ambiguous exception occurred.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
