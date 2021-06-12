#!/usr/bin/env python3

"""
This Python script is designed to query multiple online repositories for the
synonyms associated with the given word.
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


def query_collins_dictionary_synonym(single_word):
    """
    This function queries collinsdictionary.com for synonyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of synonyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_synonyms(single_word, 'collins_dictionary')
        if not check_cache:
            try:
                synonyms = []
                results_synonym = basic_soup.get_single_page_html(
                    f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{single_word}')
                soup = BeautifulSoup(results_synonym, 'lxml')
                word_found = soup.find('h1', text=f'Sorry, no results for “{single_word}” in the English Thesaurus.')
                if word_found:
                    logger.error(f'Collins Dictionary had no reference for the word {single_word}')
                    logger.error(f'Please verify that the word {single_word} is spelled correctly.')
                else:
                    query_results = basic_soup.query_html(results_synonym, 'div', 'class', 'blockSyn')
                    content_descendants = query_results.descendants
                    for item in content_descendants:
                        if item.name == 'div' and item.get('class', 'form type-syn orth'):
                            children = item.findChild('span', {'class': 'orth'})
                            if children is not None:
                                synonyms.append(children.text)
                    caching.insert_word_cache_synonyms(single_word, 'collins_dictionary', synonyms)
                    return sorted(synonyms)
            except bs4.FeatureNotFound as e:
                logger.error('A BeautifulSoup error occurred in the following code segment:')
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
            synonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return synonyms
    else:
        logger.error(f'The word "{single_word}" was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')


def query_synonym_com(single_word):
    """
    This function queries synonym.com for synonyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of synonyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_synonyms(single_word, 'synonym_com')
        if not check_cache:
            try:
                results_synonym = basic_soup.get_single_page_html(f'https://www.synonym.com/synonyms/{single_word}')
                soup = BeautifulSoup(results_synonym, "lxml")
                description_tag = soup.find("meta", property="og:description")
                if 'find any words based on your search' in description_tag['content']:
                    logger.error(f'synonym.com had no reference for the word {single_word}')
                    logger.error(f'Please verify that the word {single_word} is spelled correctly.')
                else:
                    find_synonyms = regex.split(r'\|', description_tag['content'])
                    synonyms_list = find_synonyms[2].lstrip().replace('synonyms:', '').split(',')
                    synonyms = [cleansing.normalize_space(i) for i in synonyms_list]
                    caching.insert_word_cache_synonyms(single_word, 'synonym_com', sorted(synonyms))
                    return sorted(synonyms)
            except bs4.FeatureNotFound as e:
                logger.error('An error occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except AttributeError as e:
                logger.error('An AttributeError occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except IndexError as e:
                logger.error('An IndexError occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except KeyError as e:
                logger.error('A KeyError occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except TypeError as e:
                logger.error('A TypeError occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
        else:
            synonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return synonyms
    else:
        logger.error(f'The word "{single_word}" was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')


def query_thesaurus_com(single_word):
    """
    This function queries thesaurus.com for synonyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of synonyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_synonyms(single_word, 'thesaurus_com')
        if not check_cache:
            try:
                req = requests.get(f'https://tuna.thesaurus.com/pageData/{single_word}',
                                   headers=basic_soup.http_headers,
                                   allow_redirects=True,
                                   verify=True, timeout=30)
                if '{"data":null}' not in req.text:
                    dict_synonyms = req.json()['data']['definitionData']['definitions'][0]['synonyms']
                    synonyms = sorted([r["term"] for r in dict_synonyms])
                    caching.insert_word_cache_synonyms(single_word, 'thesaurus_com', synonyms)
                    return synonyms
                else:
                    logger.error(f'The word "{single_word}" has no synonyms on thesaurus.com.')
                    logger.error(f'Please verify that the word {single_word} is spelled correctly.')
            except requests.HTTPError as e:
                logger.error('A HTTP error has occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.ConnectionError as e:
                if requests.codes:
                    'Failed to establish a new connection'
                    logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.Timeout as e:
                logger.error('A connection timeout has occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.RequestException as e:
                logger.error('An ambiguous exception occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
        else:
            synonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return synonyms
    else:
        logger.error(f'The word "{single_word}" was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')


def query_thesaurus_plus(single_word):
    """
    This function queries thesaurus.plus for synonyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of synonyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_synonyms(single_word, 'thesaurus_plus')
        if not check_cache:
            try:
                synonyms_list = []
                results_synonym = basic_soup.get_single_page_html(f'https://thesaurus.plus/synonyms/{single_word}/category/noun')
                soup = BeautifulSoup(results_synonym, "lxml")
                no_word = soup.find('title', text='404. Page not found')
                if no_word:
                    logger.error(f'thesaurus.plus has no reference for the word {single_word}')
                    logger.error(f'Please verify that the word {single_word} is spelled correctly.')
                else:
                    synonyms = []
                    parent_node = soup.find('ul', {'class': 'list paper'}).findAll('li')[1:]
                    for children in parent_node:
                        for child in children.findAll('div', {'class': 'action_pronounce'}):
                            split_dictionary = str(child.attrs).split(',')
                            synonyms_list.append(split_dictionary[1].replace("'data-term':", "").replace("'", ""))
                            synonyms = sorted([cleansing.normalize_space(i) for i in synonyms_list])
                    caching.insert_word_cache_synonyms(single_word, 'thesaurus_plus', synonyms)
                    return synonyms
            except IndexError as e:
                logger.error('A IndexError occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.HTTPError as e:
                logger.error('A HTTP error has occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.ConnectionError as e:
                if requests.codes:
                    'Failed to establish a new connection'
                    logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.Timeout as e:
                logger.error('A connection timeout has occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.RequestException as e:
                logger.error('An ambiguous exception occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
        else:
            synonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return synonyms
    else:
        logger.error(f'The word "{single_word}" was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')


def query_wordnet(single_word):
    """
    This function queries wordnet for synonyms
    related to the 'single_word' parameter.

    :param single_word: string variable to search for
    :return: list of synonyms
    :rtype: list
    """
    valid_word = word_verification.validate_word_syntax(single_word)
    if valid_word:
        check_cache = caching.cache_synonyms(single_word, 'wordnet')
        if not check_cache:
            try:
                synonyms = []
                results = requests.get(f'http://wordnetweb.princeton.edu/perl/webwn?s={single_word}',
                                       headers=basic_soup.http_headers,
                                       allow_redirects=True, verify=True, timeout=30)
                soup = BeautifulSoup(results.text, "lxml")
                if soup.findAll('h3', text='Noun'):
                    parent_node = soup.findAll("ul")[0].findAll('li')
                    for children in parent_node:
                        for child in children.find_all(href=True):
                            if 'S:' not in child.contents[0]:
                                synonyms.append(child.contents[0])
                    synonyms = sorted([x.lower() for x in synonyms])
                    caching.insert_word_cache_synonyms(single_word, 'wordnet', synonyms)
                    return synonyms
                else:
                    logger.error(f'Wordnet had no reference for the word {single_word}')
                    logger.error(f'Please verify that the word {single_word} is spelled correctly.')
            except IndexError as e:
                logger.error('A IndexError occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.HTTPError as e:
                logger.error('A HTTP error has occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.ConnectionError as e:
                if requests.codes:
                    'Failed to establish a new connection'
                    logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.Timeout as e:
                logger.error('A connection timeout has occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
            except requests.RequestException as e:
                logger.error('An ambiguous exception occurred.')
                logger.error(''.join(traceback.format_tb(e.__traceback__)))
        else:
            synonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
            return synonyms
    else:
        logger.error(f'The word "{single_word}" was not in a valid format.')
        logger.error(f'Please verify that the word {single_word} is spelled correctly.')
