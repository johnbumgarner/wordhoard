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
# Date Last Revised: September 17, 2021
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
import traceback
import re as regex
from bs4 import BeautifulSoup
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException
from wordhoard.utilities.basic_soup import Query
from wordhoard.utilities import caching, cleansing, word_verification

logger = logging.getLogger(__name__)


class Definitions(object):
    """
    This class is used to query multiple online repositories for the
    definition associated with a specific word.

    """

    def __init__(self, search_string='', max_number_of_requests=30, rate_limit_timeout_period=60, proxies=None):
        """
        Usage Examples
        ----------

        >>> definition = Definitions('mother')
        >>> results = definition.find_definitions()

        >>> definition = Definitions(search_string='mother')
        >>> results = definition.find_definitions()

        Parameters
        ----------
        :param search_string: string containing the variable to obtain definition for
        :param max_number_of_requests: maximum number of requests for a specific timeout_period
        :param rate_limit_timeout_period: the time period before a session is placed in a temporary hibernation mode
        :param proxies: dictionary of proxies to use with Python Requests
        """

        self._word = search_string
        self._proxies = proxies

        ratelimit_status = False
        self._rate_limit_status = ratelimit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(expo, RateLimitException, max_time=60, on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the antonyms repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.find_definitions = handler(limiter(self.find_definitions))

    def _colorized_text(self, r, g, b, text):
        return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"

    def _backoff_handler(self, details):
        if self._rate_limit_status is False:
            print(self._colorized_text(255, 0, 0,
                                       'The definition query rate Limit was reached. The querying process is entering '
                                       'a temporary hibernation mode.'))
            logger.info('The definition query rate limit was reached.')
            self._rate_limit_status = True

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
        Purpose
        ----------
        This function queries multiple online repositories to discover
        definitions related with the specific word provided to the
        Class Definitions.

        Returns
        ----------
        :return: list of definitions
        :rtype: list
        """
        valid_word = self._validate_word()
        if valid_word:
            check_cache = caching.cache_antonyms(self._word)
            if check_cache is False:
                definition_01 = self._query_collins_dictionary()
                definition_02 = self._query_merriam_webster()
                definition_03 = self._query_synonym_com()
                definitions = ([x for x in [definition_01, definition_02, definition_03] if x is not None])
                definitions = cleansing.flatten_multidimensional_list(definitions)
                if not definitions:
                    return f'No definitions were found for the word: {self._word}'
                else:
                    return sorted(set(definitions))
            else:
                definitions = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
                return sorted(set(definitions))
        else:
            return f'Please verify that the word {self._word} is spelled correctly.'

    def _query_collins_dictionary(self):
        """
        This function queries collinsdictionary.com for a definition associated
        with the specific word provided to the Class Definitions.

         :returns:
            definition: definition for a word

        :rtype: str

        :raises
            AttributeError: Raised when an attribute reference or assignment fails.

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

            TypeError: Raised when an operation or function is applied to an object of inappropriate type.

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            if self._proxies is None:
                response = Query(
                    f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}').get_single_page_html()
                if response.status_code == 404:
                    logger.error(f'Collins Dictionary had no definition reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    query_results = soup.find('div', {'class': 'form type-def titleTypeSubContainer'})
                    if query_results is not None:
                        definition = query_results.findNext('div', {'class': 'def'})
                        self._update_cache(definition.text)
                        return definition.text
                    else:
                        logger.error(f'Collins Dictionary had no definition reference for the word {self._word}')
            elif self._proxies is not None:
                response = Query(f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}',
                                 self._proxies).get_single_page_html()
                if response.status_code == 404:
                    logger.error(f'Collins Dictionary had no definition reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    query_results = soup.find('div', {'class': 'form type-def titleTypeSubContainer'})
                    if query_results is not None:
                        definition = query_results.findNext('div', {'class': 'def'})
                        self._update_cache(definition.text)
                        return definition.text
                    else:
                        logger.error(f'Collins Dictionary had no definition reference for the word {self._word}')
        except bs4.FeatureNotFound as error:
            logger.error('An error occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except AttributeError as error:
            logger.error('An AttributeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except IndexError as error:
            logger.error('An IndexError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except KeyError as error:
            logger.error('A KeyError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except TypeError as error:
            logger.error('A TypeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _query_merriam_webster(self):
        """
        This function queries merriam-webster.com for a definition associated
        with the specific word provided to the Class Definitions

        :returns:
            definitions: definition for a word

        :rtype: list

        :raises
            AttributeError: Raised when an attribute reference or assignment fails.

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

            TypeError: Raised when an operation or function is applied to an object of inappropriate type.

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            if self._proxies is None:
                response = Query(f'https://www.merriam-webster.com/dictionary/{self._word}').get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Merriam-webster.com has no definition reference for the word {self._word}')
                else:
                    definition_list = []
                    soup = BeautifulSoup(response.text, "lxml")
                    pattern = regex.compile(r'Words fail us')
                    if soup.find(text=pattern):
                        logger.info(f'Merriam-webster.com has no reference for the word {self._word}')
                    elif soup.find('h1', {'class': 'mispelled-word'}):
                        logger.info(f'Merriam-webster.com has no definition reference for the word {self._word}')
                    else:
                        dictionary_entry = soup.find('div', {'id': 'dictionary-entry-1'})
                        definition_container = dictionary_entry.find('div', {'class': 'vg'})
                        definition_entries = definition_container.find_all('span', {'class': 'sb-0'})[0]
                        for definition_entry in definition_entries.find_all('span', {'class': 'dtText'}):
                            definition_list.append(definition_entry.text.lower().replace(':', '').strip())
                        definitions = sorted([cleansing.normalize_space(i) for i in definition_list])
                        self._update_cache(definitions)
                        return definitions
            elif self._proxies is not None:
                response = Query(f'https://www.merriam-webster.com/dictionary/{self._word}',
                                 self._proxies).get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Merriam-webster.com has no definition reference for the word {self._word}')
                else:
                    definition_list = []
                    soup = BeautifulSoup(response.text, "lxml")
                    pattern = regex.compile(r'Words fail us')
                    if soup.find(text=pattern):
                        logger.info(f'Merriam-webster.com has no reference for the word {self._word}')
                    elif soup.find('h1', {'class': 'mispelled-word'}):
                        logger.info(f'Merriam-webster.com has no definition reference for the word {self._word}')
                    else:
                        dictionary_entry = soup.find('div', {'id': 'dictionary-entry-1'})
                        definition_container = dictionary_entry.find('div', {'class': 'vg'})
                        definition_entries = definition_container.find_all('span', {'class': 'sb-0'})[0]
                        for definition_entry in definition_entries.find_all('span', {'class': 'dtText'}):
                            definition_list.append(definition_entry.text.lower().replace(':', '').strip())
                        definitions = sorted([cleansing.normalize_space(i) for i in definition_list])
                        self._update_cache(definitions)
                        return definitions
        except bs4.FeatureNotFound as error:
            logger.error('An error occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except AttributeError as error:
            logger.error('An AttributeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except IndexError as error:
            logger.error('An IndexError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except KeyError as error:
            logger.error('A KeyError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except TypeError as error:
            logger.error('A TypeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _query_synonym_com(self):
        """
        This function queries synonym.com for a definition associated
        with the specific word provided to the Class Definitions

        :returns:
            definitions: definition for a word

        :rtype: list

        :raises
            AttributeError: Raised when an attribute reference or assignment fails.

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

            TypeError: Raised when an operation or function is applied to an object of inappropriate type.

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            if self._proxies is None:
                response = Query(f'https://www.synonym.com/synonyms/{self._word}').get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Synonym.com had no definition reference for the word {self._word}')
                else:
                    definition_list = []
                    soup = BeautifulSoup(response.text, "lxml")
                    status_tag = soup.find("meta", {"name": "pagetype"})
                    pattern = regex.compile(r'Oops, 404!')
                    if soup.find(text=pattern):
                        logger.info(f'Synonym.com had no definition reference for the word {self._word}')
                    elif status_tag.attrs['content'] == 'Term':
                        dictionary_entries = soup.find('h3', {'class': 'section-title'})
                        dictionary_entry = dictionary_entries.find_next('p').text
                        remove_brackets = regex.sub(r'.*?\[.*?\]', '', dictionary_entry)
                        definition_list.append(remove_brackets.strip())
                        definitions = sorted([x.lower() for x in definition_list])
                        self._update_cache(definitions)
                        return sorted(definitions)
            elif self._proxies is not None:
                response = Query(f'https://www.synonym.com/synonyms/{self._word}',
                                 self._proxies).get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Synonym.com had no definition reference for the word {self._word}')
                else:
                    definition_list = []
                    soup = BeautifulSoup(response.text, "lxml")
                    status_tag = soup.find("meta", {"name": "pagetype"})
                    pattern = regex.compile(r'Oops, 404!')
                    if soup.find(text=pattern):
                        logger.info(f'Synonym.com had no definition reference for the word {self._word}')
                    elif status_tag.attrs['content'] == 'Term':
                        dictionary_entries = soup.find('h3', {'class': 'section-title'})
                        dictionary_entry = dictionary_entries.find_next('p').text
                        remove_brackets = regex.sub(r'.*?\[.*?\]', '', dictionary_entry)
                        definition_list.append(remove_brackets.strip())
                        definitions = sorted([x.lower() for x in definition_list])
                        self._update_cache(definitions)
                        return sorted(definitions)
        except bs4.FeatureNotFound as error:
            logger.error('An error occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except AttributeError as error:
            logger.error('An AttributeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except IndexError as error:
            logger.error('An IndexError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except KeyError as error:
            logger.error('A KeyError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except TypeError as error:
            logger.error('A TypeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
