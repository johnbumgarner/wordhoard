#!/usr/bin/env python3

"""
This Python script is designed to query a online repository for the
hypernyms associated with a specific word.
"""
__author__ = 'John Bumgarner'
__date__ = 'June 12, 2021'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"

##################################################################################
# Date Initially Completed: June 12, 2021
# Author: John Bumgarner
#
# Date Last Revised: July 4, 2021
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
from bs4 import BeautifulSoup
from wordhoard.utilities import basic_soup, caching, cleansing, word_verification

logger = logging.getLogger(__name__)


def _get_number_of_pages(soup):
    """
    This function determines the number of pages that
    contain hypernyms and hyperonyms for a specific word.

    :param soup: BeautifulSoup lxml
    :return: number of pages
    :rtype: int

    :raises

        AttributeError: Raised when an attribute reference or assignment fails.

        KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

        TypeError: Raised when an operation or function is applied to an object of inappropriate type.
    """
    try:
        number_of_pages = 0
        pages = soup.find('div', {'id': 'pages'})
        if pages is not None:
            list_of_pages = [num for page in pages for num in page if num.isdigit()]
            if len(list_of_pages) != 0:
                number_of_pages = int(list_of_pages[-1]) + 1
        return number_of_pages

    except AttributeError as e:
        logger.error('An AttributeError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
    except KeyError as e:
        logger.error('A KeyError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
    except TypeError as e:
        logger.error('A TypeError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))


def _get_hypernyms(soup):
    """
    This function queries a HTML table for hypernyms.

    :param soup: BeautifulSoup lxml
    :return: set of hypernyms and hyperonyms
    :rtype: set

    :raises

        AttributeError: Raised when an attribute reference or assignment fails.

        KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

        TypeError: Raised when an operation or function is applied to an object of inappropriate type.
    """
    try:
        sub_set = set()
        table = soup.find('table')
        if table:
            rows = table.find_all('tr', {'class': 'theentry'})
            if rows is not None:
                for row in rows:
                    cols = row.find('td', {'class': 'abbdef'}).find('a')
                    if cols is not None:
                        if cols.text != '»':
                            sub_set.add(str(cols.text).lower())
                        else:
                            sub_set.add('no hypernyms found')
            return sub_set

    except AttributeError as e:
        logger.error('An AttributeError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
    except KeyError as e:
        logger.error('A KeyError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
    except TypeError as e:
        logger.error('A TypeError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))


class Hypernyms(object):
    """
    This class is used to query online repositories for the hypernyms associated
    with a specific word.

    Usage:
      hypernym = Hypernyms(word)

      results = hypernym.find_hypernyms

    """

    def __init__(self, word):
        """
        :param word: string variable used to find hypernyms for
        """
        self._word = word

    def _validate_word(self):
        """
        This function is designed to validate that the syntax for
        a string variable is in an acceptable format.

        :return: True or False
        :rtype bool

        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if valid_word:
            return valid_word
        else:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')

    def _check_cache(self):
        check_cache = caching.cache_hypernyms(self._word)
        return check_cache

    def _update_cache(self, hypernym):
        caching.insert_word_cache_hypernyms(self._word, hypernym)
        return

    def find_hypernyms(self):
        """
        This function queries classicthesaurus_com for hypernyms associated
        with the specific word provided to the Class Hypernyms.

        :returns:
            hypernym: list of hypernyms

        :rtype: list

        :raises

            AttributeError: Raised when an attribute reference or assignment fails.

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

            TypeError: Raised when an operation or function is applied to an object of inappropriate type.

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        valid_word = self._validate_word()
        if valid_word:
            check_cache = self._check_cache()
            if check_cache is not False:
                hypernym = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
                return hypernym
            elif check_cache is False:
                try:
                    results_hypernyms = basic_soup.get_single_page_html(
                        f'https://www.classicthesaurus.com/{self._word}/broader')
                    soup = BeautifulSoup(results_hypernyms, "lxml")
                    hypernym = _get_hypernyms(soup)

                    number_of_pages = _get_number_of_pages(soup)
                    if number_of_pages >= 2:
                        for page in range(2, number_of_pages):
                            sub_html = requests.get(f'https://www.classicthesaurus.com/{self._word}/broader/{page}',
                                                    basic_soup.http_headers)
                            sub_soup = BeautifulSoup(sub_html.text, 'lxml')
                            additional_hypernym = _get_hypernyms(sub_soup)
                            if additional_hypernym:
                                hypernym.union(additional_hypernym)

                    self._update_cache(hypernym)
                    return sorted(hypernym)

                except bs4.FeatureNotFound as e:
                    logger.error('An error occurred in the following code segment:')
                    logger.error(''.join(traceback.format_tb(e.__traceback__)))
                except AttributeError as e:
                    logger.error('An AttributeError occurred in the following code segment:')
                    logger.error(''.join(traceback.format_tb(e.__traceback__)))
                except KeyError as e:
                    logger.error('A KeyError occurred in the following code segment:')
                    logger.error(''.join(traceback.format_tb(e.__traceback__)))
                except TypeError as e:
                    logger.error('A TypeError occurred in the following code segment:')
                    logger.error(''.join(traceback.format_tb(e.__traceback__)))
