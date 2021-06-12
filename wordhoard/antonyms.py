#!/usr/bin/env python3

"""
This Python script is designed to query multiple online repositories for the
antonyms associated with a specific word.
"""
__author__ = 'John Bumgarner'
__date__ = 'October 15, 2020'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2020 John Bumgarner"

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
from wordhoard.utilities import basic_soup, caching, cleansing, wordhoard_logger, word_verification

logger = logging.getLogger(__name__)
wordhoard_logger.enable_logging(logger)


def query_synonym_com(single_word):
    """
    This function queries synonym.com for antonyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of antonyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_antonyms(single_word, 'synonym_com')
        if not check_cache:
            try:
                results_antonyms = basic_soup.get_single_page_html(f'https://www.synonym.com/synonyms/{single_word}')
                soup = BeautifulSoup(results_antonyms, "lxml")
                description_tag = soup.find("meta", property="og:description")
                if 'find any words based on your search' in description_tag['content']:
                    logger.error(f'synonym.com had no reference for the word {single_word}')
                else:
                    find_antonyms = regex.split(r'\|', description_tag['content'])
                    antonyms_list = find_antonyms[3].lstrip().replace('antonyms:', '').split(',')
                    antonyms = sorted([cleansing.normalize_space(i) for i in antonyms_list])
                    if antonyms:
                        caching.insert_word_cache_antonyms(single_word, 'synonym_com', antonyms)
                        return antonyms
                    else:
                        logger.error(f'The word {single_word} no antonyms on synonym.com.')
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
        else:
            antonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return antonyms
    else:
        logger.error(f'The word {single_word} was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')


def query_thesaurus_com(single_word):
    """
    This function queries thesaurus.com for antonyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of antonyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_antonyms(single_word, 'thesaurus_com')
        if not check_cache:
            try:
                req = requests.get(f'https://tuna.thesaurus.com/pageData/{single_word}',
                                   headers=basic_soup.http_headers,
                                   allow_redirects=True, verify=True, timeout=30)
                if '{"data":null}' not in req.text:
                    dict_antonyms = req.json()['data']['definitionData']['definitions'][0]['antonyms']
                    if dict_antonyms:
                        antonyms = sorted([r["term"] for r in dict_antonyms])
                        caching.insert_word_cache_antonyms(single_word, 'thesaurus_com', antonyms)
                        return antonyms
                    else:
                        logger.error(f'The word {single_word} has no antonyms on thesaurus.com.')
                else:
                    logger.error(f'The word {single_word} was not found on thesaurus.com.')
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
        else:
            antonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return antonyms
    else:
        logger.error(f'The word {single_word} was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')


def query_thesaurus_plus(single_word):
    """
    This function queries thesaurus.plus for antonyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of antonyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_antonyms(single_word, 'thesaurus_plus')
        if not check_cache:
            try:
                results_antonym = basic_soup.get_single_page_html(f'https://thesaurus.plus/antonyms/{single_word}')
                soup = BeautifulSoup(results_antonym, "lxml")
                no_word = soup.find('title', text='404. Page not found')
                if no_word:
                    logger.error(f'thesaurus.plus has no reference for the word {single_word}')
                else:
                    antonyms_list = []
                    antonyms = []
                    parent_node = soup.find('ul', {'class': 'list paper'}).findAll('li')
                    for children in parent_node:
                        for child in children.findAll('div', {'class': 'action_pronounce'}):
                            split_dictionary = str(child.attrs).split(',')
                            antonyms_list.append(split_dictionary[1].replace("'data-term':", "").replace("'", ""))
                            antonyms = sorted([cleansing.normalize_space(i) for i in antonyms_list])
                    caching.insert_word_cache_antonyms(single_word, 'thesaurus_plus', antonyms)
                    return antonyms
            except IndexError as error:
                logger.error('A IndexError occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))
                logger.info(f'Please verify that the word {single_word} is spelled correctly.')
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
        else:
            antonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return antonyms
    else:
        logger.error(f'The word {single_word} was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')

