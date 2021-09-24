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
# Date Last Revised: September 7, 2021
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


class Synonyms(object):
    """
    This class is used to query multiple online repositories for the synonyms associated
    with a specific word.
    """

    def __init__(self, search_string='', max_number_of_requests=30, rate_limit_timeout_period=60, proxies=None):
        """
        Usage Examples
        ----------

        >>> synonym = Synonyms('mother')
        >>> results = synonym.find_synonyms()

        >>> synonym = Synonyms(search_string='mother')
        >>> results = synonym.find_synonyms()

        Parameters
        ----------
        :param search_string: string containing the variable to obtain synonyms for
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
        # Establishes a rate limit for making requests to the synonyms repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.find_synonyms = handler(limiter(self.find_synonyms))

    def _colorized_text(self, r, g, b, text):
        return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"

    def _backoff_handler(self, details):
        if self._rate_limit_status is False:
            print(self._colorized_text(255, 0, 0,
                                       'The synonyms query rate Limit was reached. The querying process is entering a '
                                       'temporary hibernation mode.'))
            logger.info('The synonyms query rate limit was reached.')
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

    def _check_cache(self):
        check_cache = caching.cache_synonyms(self._word)
        return check_cache

    def _update_cache(self, synonyms):
        caching.insert_word_cache_synonyms(self._word, synonyms)
        return

    def find_synonyms(self):
        """
        Purpose
        ----------
        This function queries multiple online repositories to discover synonyms
        associated with the specific word provided to the Class Synonyms.
        The synonyms are deduplicated and sorted alphabetically.

        Returns
        ----------
        :returns:
            synonyms: list of synonyms

        :rtype: list
        """
        valid_word = self._validate_word()
        if valid_word:
            check_cache = self._check_cache()
            if check_cache is False:
                synonyms_01 = self._query_collins_dictionary()
                synonyms_02 = self._query_merriam_webster()
                synonyms_03 = self._query_synonym_com()
                synonyms_04 = self._query_thesaurus_com()
                synonyms_05 = self._query_wordnet()
                synonyms = ([x for x in [synonyms_01, synonyms_02, synonyms_03, synonyms_04, synonyms_05]
                             if x is not None])
                synonyms_results = cleansing.flatten_multidimensional_list(synonyms)
                if not synonyms_results:
                    return f'No synonyms were found for the word: {self._word}'
                else:
                    return sorted(set([word.lower() for word in synonyms_results]))
            else:
                synonyms = cleansing.flatten_multidimensional_list([val for val in check_cache.values()])
                return sorted(set(synonyms))
        else:
            return f'Please verify that the word {self._word} is spelled correctly.'

    def _query_collins_dictionary(self):
        """
        This function queries collinsdictionary.com for synonyms associated
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
            synonyms = []
            if self._proxies is None:
                response = Query(f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}').get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Collins Dictionary had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, 'lxml')
                    word_found = soup.find('h1', text=f'Sorry, no results for “{self._word}” in the English Thesaurus.')
                    if word_found:
                        logger.info(f'Collins Dictionary had no synonym reference for the word {self._word}')
                    else:
                        if soup.find('div', {'class': 'blockSyn'}):
                            query_results = soup.find('div', {'class': 'blockSyn'})
                            for primary_syn in query_results.find_all('div', {'class', 'form type-syn orth'}):
                                synonyms.append(primary_syn.text)

                            for sub_syn in query_results.find_all('div', {'class', 'form type-syn'}):
                                child = sub_syn.findChild('span', {'class': 'orth'})
                                synonyms.append(child.text)

                        synonyms = sorted([x.lower() for x in synonyms])
                        self._update_cache(synonyms)
                        return sorted(synonyms)

            elif self._proxies is not None:
                response = Query(f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}',
                                 self._proxies).get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Collins Dictionary had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, 'lxml')
                    word_found = soup.find('h1', text=f'Sorry, no results for “{self._word}” in the English Thesaurus.')
                    if word_found:
                        logger.info(f'Collins Dictionary had no synonym reference for the word {self._word}')
                    else:
                        if soup.find('div', {'class': 'blockSyn'}):
                            query_results = soup.find('div', {'class': 'blockSyn'})
                            for primary_syn in query_results.find_all('div', {'class', 'form type-syn orth'}):
                                synonyms.append(primary_syn.text)

                            for sub_syn in query_results.find_all('div', {'class', 'form type-syn'}):
                                child = sub_syn.findChild('span', {'class': 'orth'})
                                synonyms.append(child.text)

                        synonyms = sorted([x.lower() for x in synonyms])
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

    def _query_merriam_webster(self):
        """
        This function queries merriam-webster.com for synonyms associated
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
            synonyms_list = []
            if self._proxies is None:
                response = Query(f'https://www.merriam-webster.com/thesaurus/{self._word}').get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    pattern = regex.compile(r'Words fail us')
                    if soup.find(text=pattern):
                        logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                    elif soup.find('h1', {'class': 'mispelled-word'}):
                        logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                    else:
                        synonyms = []
                        if soup.find('p', {'class': 'function-label'}):
                            label = soup.find('p', {'class': 'function-label'})
                            if label.text.startswith('Synonyms for'):
                                parent_tag = soup.find("span", {'class': 'thes-list syn-list'})
                                word_container = parent_tag.find('div', {'class': 'thes-list-content synonyms_list'})
                                for list_item in word_container.find_all("ul", {'class': 'mw-list'}):
                                    for link in list_item.find_all('a', href=True):
                                        synonyms_list.append(link.text)
                                synonyms = sorted([cleansing.normalize_space(i) for i in synonyms_list])
                                synonyms = sorted([x.lower() for x in synonyms])
                            self._update_cache(synonyms)
                            return synonyms
            elif self._proxies is not None:
                response = Query(f'https://www.merriam-webster.com/thesaurus/{self._word}',
                                 self._proxies).get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    pattern = regex.compile(r'Words fail us')
                    if soup.find(text=pattern):
                        logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                    elif soup.find('h1', {'class': 'mispelled-word'}):
                        logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                    else:
                        synonyms = []
                        if soup.find('p', {'class': 'function-label'}):
                            label = soup.find('p', {'class': 'function-label'})
                            if label.text.startswith('Synonyms for'):
                                parent_tag = soup.find("span", {'class': 'thes-list syn-list'})
                                word_container = parent_tag.find('div', {'class': 'thes-list-content synonyms_list'})
                                for list_item in word_container.find_all("ul", {'class': 'mw-list'}):
                                    for link in list_item.find_all('a', href=True):
                                        synonyms_list.append(link.text)
                                synonyms = sorted([cleansing.normalize_space(i) for i in synonyms_list])
                                synonyms = sorted([x.lower() for x in synonyms])
                            self._update_cache(synonyms)
                            return synonyms
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
            if self._proxies is None:
                response = Query(f'https://www.synonym.com/synonyms/{self._word}').get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    status_tag = soup.find("meta", {"name": "pagetype"})
                    pattern = regex.compile(r'Oops, 404!')
                    if soup.find(text=pattern):
                        logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
                    elif status_tag.attrs['content'] == 'Term':
                        if soup.find('div', {'data-section': 'synonyms'}):
                            synonyms_class = soup.find('div', {'data-section': 'synonyms'})
                            synonyms = [word.text for word in
                                        synonyms_class.find('ul', {'class': 'section-list'}).find_all('li')]
                            synonyms = sorted([x.lower() for x in synonyms])
                            self._update_cache(synonyms)
                            return sorted(synonyms)
                        else:
                            logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
            elif self._proxies is not None:
                response = Query(f'https://www.synonym.com/synonyms/{self._word}',
                                 self._proxies).get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    status_tag = soup.find("meta", {"name": "pagetype"})
                    pattern = regex.compile(r'Oops, 404!')
                    if soup.find(text=pattern):
                        logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
                    elif status_tag.attrs['content'] == 'Term':
                        if soup.find('div', {'data-section': 'synonyms'}):
                            synonyms_class = soup.find('div', {'data-section': 'synonyms'})
                            synonyms = [word.text for word in
                                        synonyms_class.find('ul', {'class': 'section-list'}).find_all('li')]
                            synonyms = sorted([x.lower() for x in synonyms])
                            self._update_cache(synonyms)
                            return sorted(synonyms)
                        else:
                            logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
        except bs4.FeatureNotFound as error:
            logger.error('An error occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except AttributeError as error:
            logger.info('\n')
            logger.info(self._word)
            logger.error('An AttributeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            logger.info('\n')
        except IndexError as error:
            logger.error('An IndexError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except KeyError as error:
            logger.error('A KeyError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except TypeError as error:
            logger.error('A TypeError occurred in the following code segment:')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _query_thesaurus_com(self):
        """
        This function queries thesaurus.com for synonyms associated
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
            synonyms_list = []
            if self._proxies is None:
                response = Query(f'https://www.thesaurus.com/browse/{self._word}').get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Thesaurus.com had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    status_tag = soup.find("h1")
                    if status_tag.text.startswith('0 results for'):
                        logger.info(f'Thesaurus.com had no synonym reference for the word {self._word}')
                    else:
                        synonyms = []
                        word_container = soup.find('div', {'data-testid': 'word-grid-container'})
                        for list_item in word_container.find('ul').find_all('li'):
                            for link in list_item.find_all('a', href=True):
                                synonyms_list.append(link.text)
                            synonyms = sorted([cleansing.normalize_space(i) for i in synonyms_list])
                            synonyms = sorted([x.lower() for x in synonyms])
                        self._update_cache(synonyms)
                        return synonyms
            elif self._proxies is not None:
                response = Query(f'https://www.thesaurus.com/browse/{self._word}',
                                 self._proxies).get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Thesaurus.com had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    status_tag = soup.find("h1")
                    if status_tag.text.startswith('0 results for'):
                        logger.info(f'Thesaurus.com had no synonym reference for the word {self._word}')
                    else:
                        synonyms = []
                        word_container = soup.find('div', {'data-testid': 'word-grid-container'})
                        for list_item in word_container.find('ul').find_all('li'):
                            for link in list_item.find_all('a', href=True):
                                synonyms_list.append(link.text)
                            synonyms = sorted([cleansing.normalize_space(i) for i in synonyms_list])
                            synonyms = sorted([x.lower() for x in synonyms])
                        self._update_cache(synonyms)
                        return synonyms
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

    def _query_wordnet(self):
        """
        This function queries wordnet for synonyms associated
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
            synonyms = []
            if self._proxies is None:
                response = Query(f'http://wordnetweb.princeton.edu/perl/webwn?s={self._word}').get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Wordnet had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    pattern = regex.compile(r'Your search did not return any results')
                    if soup.find(text=pattern):
                        logger.info(f'Wordnet had no synonym reference for the word {self._word}')
                    else:
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
                            logger.info(f'Wordnet had no synonym reference for the word {self._word}')
            elif self._proxies is not None:
                response = Query(f'http://wordnetweb.princeton.edu/perl/webwn?s={self._word}',
                                 self._proxies).get_single_page_html()
                if response.status_code == 404:
                    logger.info(f'Wordnet had no synonym reference for the word {self._word}')
                else:
                    soup = BeautifulSoup(response.text, "lxml")
                    pattern = regex.compile(r'Your search did not return any results')
                    if soup.find(text=pattern):
                        logger.info(f'Wordnet had no synonym reference for the word {self._word}')
                    else:
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
                            logger.info(f'Wordnet had no synonym reference for the word {self._word}')
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
