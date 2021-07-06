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


class Synonyms(object):
    """
    This class is used to query multiple online repositories for the synonyms associated
    with a specific word.

    Usage: synonym = Synonyms(word)
           results = synonym.find_synonyms()
    """

    def __init__(self, word):
        """
        :param word: string containing the variable to search for
        """
        self._word = word

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

    def _check_cache(self):
        check_cache = caching.cache_synonyms(self._word)
        return check_cache

    def _update_cache(self, synonyms):
        caching.insert_word_cache_synonyms(self._word, synonyms)
        return

    def find_synonyms(self):
        """
        This function queries multiple online repositories to discover synonyms
        associated with the specific word provided to the Class Synonyms.
        The synonyms are deduplicated and sorted alphabetically.

        :returns:
            synonyms: list of synonyms

        :rtype: list
        """
        valid_word = self._validate_word()
        if valid_word:
            check_cache = self._check_cache()
            if check_cache is False:
                synonyms_01 = self._query_collins_dictionary()
                synonyms_02 = self._query_synonym_com()
                synonyms_03 = self._query_thesaurus_plus()
                synonyms_04 = self._query_wordnet()
                synonyms = ([x for x in [synonyms_01, synonyms_02, synonyms_03, synonyms_04] if x is not None])
                synonyms_results = cleansing.flatten_multidimensional_list(synonyms)
                return sorted(set(synonyms_results))
            else:
                synonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
                return synonyms

    def _query_collins_dictionary(self):
        """
        This function queries collinsdictionary.com for synonyms associated
        with the specific word provided to the Class Synonyms.

         :returns:
            synonyms: list of synonyms

        :rtype: list

        :raises
            AttributeError: Raised when an attribute reference or assignment fails.

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

            TypeError: Raised when an operation or function is applied to an object of inappropriate type.

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            synonyms = []
            results_synonym = basic_soup.get_single_page_html(
                f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}')
            soup = BeautifulSoup(results_synonym, 'lxml')
            word_found = soup.find('h1', text=f'Sorry, no results for “{self._word}” in the English Thesaurus.')
            if word_found:
                logger.error(f'Collins Dictionary had no reference for the word {self._word}')
                logger.error(f'Please verify that the word {self._word} is spelled correctly.')
            else:
                query_results = basic_soup.query_html(results_synonym, 'div', 'class', 'blockSyn')
                content_descendants = query_results.descendants
                for item in content_descendants:
                    if item.name == 'div' and item.get('class', 'form type-syn orth'):
                        children = item.findChild('span', {'class': 'orth'})
                        if children is not None:
                            synonyms.append(children.text)

                self._update_cache(synonyms)
                return sorted(synonyms)
        except bs4.FeatureNotFound as error:
            logger.error('A BeautifulSoup error occurred in the following code segment:')
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

    def _query_synonym_com(self):
        """
        This function queries synonym.com for synonyms associated
        with the specific word provided to the Class Synonyms.

         :returns:
            synonyms: list of synonyms

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
            results_synonym = basic_soup.get_single_page_html(
                f'https://www.synonym.com/synonyms/{self._word}')
            soup = BeautifulSoup(results_synonym, "lxml")
            description_tag = soup.find("meta", property="og:description")
            if 'find any words based on your search' in description_tag['content']:
                logger.error(f'synonym.com had no reference for the word {self._word}')
                logger.error(f'Please verify that the word {self._word} is spelled correctly.')
            else:
                find_synonyms = regex.split(r'\|', description_tag['content'])
                synonyms_list = find_synonyms[2].lstrip().replace('synonyms:', '').split(',')
                synonyms = [cleansing.normalize_space(i) for i in synonyms_list]
                self._update_cache(synonyms)
                return sorted(synonyms)
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

    def _query_thesaurus_plus(self):
        """
        This function queries thesaurus.plus for synonyms associated
        with the specific word provided to the Class Synonyms.

        :returns:
            synonyms: list of synonyms

        :rtype: list

        :raises

            IndexError: Raised when a sequence subscript is out of range.

            requests.ConnectionError: Raised when a connection error has occurred.

            requests.HTTPError: Raised when an HTTP error has occurred.

            requests.RequestException: Raised when an unknown error has occurred.

            requests.Timeout: Raised when the request timed out.

        """
        try:
            synonyms_list = []
            results_synonym = basic_soup.get_single_page_html(
                f'https://thesaurus.plus/synonyms/{self._word}/category/noun')
            soup = BeautifulSoup(results_synonym, "lxml")
            no_word = soup.find('title', text='404. Page not found')
            if no_word:
                logger.error(f'thesaurus.plus has no reference for the word {self._word}')
                logger.error(f'Please verify that the word {self._word} is spelled correctly.')
            else:
                synonyms = []
                parent_node = soup.find('ul', {'class': 'list paper'}).findAll('li')[1:]
                for children in parent_node:
                    for child in children.findAll('div', {'class': 'action_pronounce'}):
                        split_dictionary = str(child.attrs).split(',')
                        synonyms_list.append(split_dictionary[1].replace("'data-term':", "").replace("'", ""))
                        synonyms = sorted([cleansing.normalize_space(i) for i in synonyms_list])
                self._update_cache(synonyms)
                return synonyms
        except IndexError as error:
            logger.error('A IndexError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
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

    def _query_wordnet(self):
        """
        This function queries wordnet for synonyms associated
        with the specific word provided to the Class Synonyms.

        :returns:
            synonyms: list of synonyms

        :rtype: list

        :raises

            IndexError: Raised when a sequence subscript is out of range.

            requests.ConnectionError: Raised when a connection error has occurred.

            requests.HTTPError: Raised when an HTTP error has occurred.

            requests.RequestException: Raised when an unknown error has occurred.

            requests.Timeout: Raised when the request timed out.

        """
        try:
            synonyms = []
            results = requests.get(f'http://wordnetweb.princeton.edu/perl/webwn?s={self._word}',
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
                self._update_cache(synonyms)
                return synonyms
            else:
                logger.error(f'Wordnet had no reference for the word {self._word}')
                logger.error(f'Please verify that the word {self._word} is spelled correctly.')
        except IndexError as error:
            logger.error('A IndexError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
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
