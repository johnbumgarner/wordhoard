#!/usr/bin/env python3

"""
This Python script is designed to query a online repository for the
hyponyms associated with a specific word.
"""
__author__ = 'John Bumgarner'
__date__ = 'June 11, 2021'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"

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
from wordhoard.utilities import basic_soup, caching, wordhoard_logger, word_verification

logger = logging.getLogger(__name__)
wordhoard_logger.enable_logging(logger)

rand_user_agent = basic_soup.rand_user_agent
http_headers = {'user-agent': rand_user_agent}

def _get_number_of_pages(soup):
    """
    This function determines the number of pages
    that contain hyponyms for a specific word.

    :param soup: BeautifulSoup lxml
    :return: number of pages
    :rtype: int
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


def _get_hyponyms(soup):
    """
    This function queries a table for hyponyms.

    :param soup: BeautifulSoup lxml
    :return: set of hyponyms
    :rtype: set
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
                            sub_set.add('no hyponyms found')
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


def find_hyponyms(single_word):
    """
    This function queries classicthesaurus_com for hyponyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of hyponyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_hyponyms(single_word, 'classicthesaurus_com')
        if not check_cache:
            try:
                results_hyponyms = basic_soup.get_single_page_html(f'https://www.classicthesaurus.com/{single_word}/narrower')
                soup = BeautifulSoup(results_hyponyms, "lxml")
                hyponym = _get_hyponyms(soup)

                number_of_pages = _get_number_of_pages(soup)
                if number_of_pages >= 2:
                    for page in range(2, number_of_pages):
                        sub_html = requests.get(f'https://www.classicthesaurus.com/{single_word}/narrower/{page}',
                                                headers=http_headers)
                        sub_soup = BeautifulSoup(sub_html.text, 'lxml')
                        additional_hyponym = _get_hyponyms(sub_soup)
                        hyponym.union(additional_hyponym)

                return sorted(hyponym)

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
        else:
            logger.error(f'The word {single_word} was not in a valid format.')
            logger.error(f'Please verify that the word {single_word} is spelled correctly.')

