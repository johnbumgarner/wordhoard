#!/usr/bin/env python3

"""
This Python script is designed to query multiple online repositories for the
definition associated with a given word.
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
    This function queries synonym.com for a definition
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: definition for the word
    :rtype: string
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_definition(single_word, 'synonym_com')
        if not check_cache:
            try:
                results_definition = basic_soup.get_single_page_html(f'https://www.synonym.com/synonyms/{single_word}')
                soup = BeautifulSoup(results_definition, "lxml")
                description_tag = soup.find("meta", property="og:description")
                if 'find any words based on your search' not in description_tag['content']:
                    find_definition = regex.split(r'\|', description_tag['content'])
                    definition_list = find_definition[1].lstrip().replace('definition:', '').split(',')
                    definition = [cleansing.normalize_space(i) for i in definition_list]
                    definition_list_to_string = ' '.join([str(elem) for elem in definition])
                    caching.insert_word_cache_definition(single_word, 'synonym_com', definition_list_to_string)
                    return definition_list_to_string
                else:
                    logger.error(f'synonym.com had no reference for the word {single_word}')
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
            definition = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return definition
    else:
        logger.error(f'The word "{single_word}" was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')


def query_collins_dictionary_synonym(single_word):
    """
    This function queries collinsdictionary.com for a definition
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: definition for the word
    :rtype: string
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_definition(single_word, 'collins_dictionary')
        if not check_cache:
            try:
                results_definition = basic_soup.get_single_page_html(
                    f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{single_word}')
                query_results = basic_soup.query_html(results_definition, 'div', 'class',
                                                      'form type-def titleTypeSubContainer')
                if query_results is not None:
                    definition = query_results.findNext('div', {'class': 'def'})
                    caching.insert_word_cache_definition(single_word, 'collins_dictionary', definition.text)
                    return definition.text
                else:
                    logger.error(f'Collins Dictionary had no reference for the word {single_word}')
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
            definition = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return definition
    else:
        logger.error(f'The word "{single_word}" was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')


def query_thesaurus_com(single_word):
    """
    This function queries thesaurus.com for a definition
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: definition for the word
    :rtype: string
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_definition(single_word, 'thesaurus_com')
        if not check_cache:
            try:
                req = requests.get(f'https://tuna.thesaurus.com/pageData/{single_word}',
                                   headers=basic_soup.http_headers,
                                   allow_redirects=True, verify=True, timeout=30)
                if req.json()['data'] is not None:
                    definition = req.json()['data']['definitionData']['definitions'][0]['definition']
                    caching.insert_word_cache_definition(single_word, 'thesaurus_com', definition)
                    return definition
                else:
                    logger.error(f'thesaurus.com had no reference for the word {single_word}')
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
            definition = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return definition
    else:
        logger.error(f'The word "{single_word}" was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')

