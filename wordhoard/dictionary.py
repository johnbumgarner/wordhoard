#!/usr/bin/env python3

"""
This Python module is designed to query multiple online repositories for the
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
# Date Last Revised: May 25, 2024
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
import sys
import json
import logging
import traceback
import re as regex
from collections.abc import Sized
from concurrent.futures.thread import BrokenThreadPool
from concurrent.futures import ThreadPoolExecutor, as_completed, BrokenExecutor
from typing import Dict, List, Optional, Set, Tuple, Union

# Third-party imports
import bs4
import requests
from bs4 import BeautifulSoup
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException

# Local or project-specific imports
from wordhoard.utilities.request_html import Query
from wordhoard.utilities.cloudflare_bypass import Cloudflare
from wordhoard.utilities.colorized_text import colorized_text
from wordhoard.utilities import caching, cleansing, word_verification
from wordhoard.utilities.cloudflare_checker import CloudflareVerification

logger = logging.getLogger(__name__)

class PartOfSpeech:
    """
        This utility class contains static methods to extract part of speech categories
        from HTML responses of various sources, which are Collins Dictionary, Merriam-Webster,
        Synonym.com and Thesaurus.com.

        Static Methods
        --------------
        _handle_query_exceptions(error):
            Helper method to handle common exceptions in query methods.

        part_of_speech_category_collins_dictionary(soup: BeautifulSoup) -> str:
            Extracts the part of speech category from the HTML response of Collins Dictionary.

        part_of_speech_category_merriam_webster(soup: BeautifulSoup) -> str:
            Extracts the part of speech category from the HTML response of Merriam-Webster.

        part_of_speech_category_synonym_com(soup: BeautifulSoup) -> str:
            Extracts the part of speech category from the HTML response of Synonym.com.

        part_of_speech_category_thesaurus_com(soup: BeautifulSoup) -> str:
            Extracts the part of speech category from the HTML response of Thesaurus.com.

        """
    @staticmethod
    def _handle_query_exceptions(error):
        """
        Helper method to handle common exceptions in query methods.
        """
        logger.error('An error occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(error.__traceback__)))

    @staticmethod
    def part_of_speech_category_collins_dictionary(soup: BeautifulSoup) -> str:
        """
        Extracts the part of speech category from the HTML response of Collins Dictionary.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: Part of speech category
        :rtype: str
        """
        part_of_speech_category: str = ''
        try:
            if soup.find(name='span', attrs={'class': 'headerSensePos'}):
                tag_part_of_speech = soup.find(name='span', attrs={'class': 'headerSensePos'})
                if tag_part_of_speech and len(tag_part_of_speech.text) != 0:
                    part_of_speech_category = tag_part_of_speech.text.strip('()')
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            PartOfSpeech._handle_query_exceptions(error)
        return part_of_speech_category

    @staticmethod
    def part_of_speech_category_merriam_webster(soup: BeautifulSoup) -> str:
        """
        Extracts the part of speech category from the HTML response of Merriam-Webster.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: Part of speech category
        :rtype: str
        """
        part_of_speech_category: str = ''
        try:
            if soup.select(selector='#dictionary-entry-1 > div.row.entry-header > div > '
                                    'div.entry-header-content.d-flex.flex-wrap.align-items-baseline.flex-row.mb-0 > '
                                    'h2 > a'):
                css_part_of_speech = soup.select(selector= '#dictionary-entry-1 > div.row.entry-header > div > '
                                                           'div.entry-header-content.d-flex.flex-wrap.align-items-baseline.flex-row.mb-0 > h2 > a')
                if len(css_part_of_speech[0].text) != 0:
                    part_of_speech_category = css_part_of_speech[0].text.split()[0]
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            PartOfSpeech._handle_query_exceptions(error)
        return part_of_speech_category.strip()

    @staticmethod
    def part_of_speech_category_synonym_com(soup: BeautifulSoup) -> str:
        """
        Extracts the part of speech category from the HTML response of Synonym.com.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: Part of speech category
        :rtype: str
        """
        part_of_speech_category: str = ''
        try:
            if soup.select(selector= 'body > div.page-container > div.content-container > div.main-column > '
                                     'div.sections-wrapper > div:nth-child(1) > p > strong'):
                css_part_of_speech = soup.select(selector= 'body > div.page-container > div.content-container > '
                                                           'div.main-column > div.sections-wrapper > div:nth-child(1) > '
                                                           'p > strong')
                if len(css_part_of_speech[0].text) != 0:
                    part_of_speech_category = css_part_of_speech[0].text.rstrip('.')
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            PartOfSpeech._handle_query_exceptions(error)
        return part_of_speech_category.strip()

    @staticmethod
    def part_of_speech_category_thesaurus_com(soup: BeautifulSoup) -> str:
        """
        Extracts the part of speech category from the HTML response of Thesaurus.com.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: Part of speech category
        :rtype: str
        """
        part_of_speech_category: str = ''
        try:
            synonym_section = soup.find(name='section', attrs={'data-type': 'synonym-antonym-module'})
            synonym_div_tags = synonym_section.find_all(name='div',
                                                        attrs={'data-type': 'synonym-and-antonym-card'})
            if synonym_div_tags:
                part_of_speech_category = synonym_div_tags[0].find('p').text.split(' ', 1)[0]
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            PartOfSpeech._handle_query_exceptions(error)
        return part_of_speech_category.strip()

class ParseDefinitions:
    """
        This utility class contains static methods to parse definitions from HTML responses of various sources,
        which are Merriam_Webster, Synonym.com and Thesaurus.com.

        Static Methods
        --------------
        _handle_query_exceptions(error):
            Helper method to handle common exceptions in query methods.

        parse_merriam_webster(soup: BeautifulSoup) -> list:
            Parses definitions from the HTML response of Merriam_Webster.

        parse_synonym_com(soup: BeautifulSoup) -> list:
            Parses definitions from the HTML response of Synonym.com.

        parse_thesaurus_com(soup: BeautifulSoup) -> list:
            Parses definitions from the HTML response of Thesaurus.com.
        """

    @staticmethod
    def _handle_query_exceptions(error):
        """
        Helper method to handle common exceptions in query methods.
        """
        logger.error('An error occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(error.__traceback__)))

    @staticmethod
    def parse_collins_dictionary(soup: BeautifulSoup, word: str) -> list:
        """
        Parses definitions from the HTML response of Collins Dictionary.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :param word: word to search
        :param type word: string
        :return: List of definitions extracted from the HTML response
        :rtype: list
        """
        definition_list: list = []
        try:
            query_results = soup.find(name='div', attrs={'class': 'form type-def titleTypeSubContainer'})
            if query_results is not None:
                definition = query_results.findNext(name='div', attrs={'class': 'def'})
                definition_list.append(definition.text.strip())
            elif query_results is None:
                logger.error(f'Collins Dictionary had no definition reference for the word {word}')
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            ParseDefinitions._handle_query_exceptions(error)
        return definition_list

    @staticmethod
    def parse_merriam_webster(soup: BeautifulSoup) -> list:
        """
        Parses definitions from the HTML response of Merriam-Webster.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: List of definitions extracted from the HTML response
        :rtype: list
        """
        definition_list: list = []
        try:
            dictionary_entry = soup.find(name='div', attrs={'id': 'dictionary-entry-1'})
            definition_container = dictionary_entry.find(name='div', attrs={'class': 'vg'})
            definition_entries = definition_container.find(name='div', attrs={'class': 'sb-0 sb-entry'})
            for definition_entry in definition_entries.find_all(name='span', attrs={'class': 'dtText'}):
                definition_list.append(definition_entry.text.lower().replace(':', '').strip())
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            ParseDefinitions._handle_query_exceptions(error)
        return definition_list

    @staticmethod
    def parse_synonym_com(soup: BeautifulSoup) -> list:
        """
        Parses definitions from the HTML response of synonym.com.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: List of definitions extracted from the HTML response
        :rtype: list
        """
        definition_list: list = []
        try:
            dictionary_entries = soup.find(name='h3', attrs={'class': 'section-title'})
            dictionary_entry = dictionary_entries.find_next(name='p').text
            remove_brackets = regex.sub(pattern=r'.*?\[.*?\]', repl='', string=dictionary_entry)
            remove_spaces = cleansing.remove_excess_whitespace(remove_brackets)
            definition_list.append(remove_spaces)
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            ParseDefinitions._handle_query_exceptions(error)
        return definition_list

    @staticmethod
    def parse_thesaurus_com(soup: BeautifulSoup) -> list:
        """
        Parses definitions from the HTML response of Thesaurus.com.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: List of definitions extracted from the HTML response
        :rtype: list
        """
        definition_list: list = []
        try:
            synonym_section = soup.find(name='section', attrs={'data-type': 'synonym-antonym-module'})
            synonym_div_tags = synonym_section.find_all(name='div',
                                                    attrs={'data-type': 'synonym-and-antonym-card'})
            if synonym_div_tags:
                definition = synonym_div_tags[0].find(name='p').text.split(' ', 1)[1]
                definition_list.append(definition.strip())
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            ParseDefinitions._handle_query_exceptions(error)
        return definition_list

class Definitions:
    """
        This Python class is used to query multiple online repositories for the definition
        associated with a specific word.

        Usage Examples
        ----------
        >>> definition = Definitions('mother')
        >>> results = definition.find_definitions()

        Parameters
        ----------
        search_string : str, optional
            The word for which definitions are to be found.
        sources: Optional[List[str]]
            The sources to search for definitions.
        output_format : str, optional
            Format for returned results. Default is 'list'. Acceptable values are 'dictionary', 'list', or 'json'.
        max_number_of_requests : int, optional
            Maximum number of requests within a specified time period.
        rate_limit_timeout_period : int, optional
            Time period before temporary hibernation due to rate limiting.
        user_agent : str, optional
            User agent string for HTTP requests.
        proxies : dict, optional
            Dictionary of proxies for Python Requests.

        Attributes
        ----------
        _proxies : Optional[Dict[str, str]]
            Proxies to use with Python Requests.
        _word : str
            The word to find definitions for.
        _sources : Optional[List[str]]
            The sources to search for definitions.
        _user_agent : Optional[str]
            User agent for HTTP requests.
        _output_format : str
            Format for returned results.
        _valid_output_formats : Set[str]
            Set of valid output formats.
        _rate_limit_status : bool
            Status indicating whether rate limit is reached.

        Methods
        -------
        find_definitions() -> Union[List[Sized], Dict[str, List[str]], str]:
            Finds definitions for the specified word.
        _validate_word() -> bool:
            Validates the syntax of the word.
        _check_cache() -> Tuple[bool, Union[Dict[str, List[str]], None]]:
            Checks if definitions are cached.
        _update_cache(pos_category: str, synonyms: Union[List[str], Set[str]]) -> None:
            Updates the cache with new definitions.
        _request_http_response(url: str) -> requests.models.Response:
            Makes an HTTP request and returns the response.
        _run_query_tasks_in_parallel() -> List[tuple[List[str], str]]:
            Runs query tasks in parallel using a ThreadPool.
        _query_output(self, antonyms: list, part_of_speech: Union[set[str], str]) -> Union[list, dict, str]:
            Process the output format based on the specified format.
        _handle_query_exceptions(error):
            Handles common exceptions in query methods.
        _query_collins_dictionary() -> Union[Tuple[List[str], str], None]:
            Queries collinsdictionary.com for definitions.
        _query_merriam_webster() -> Union[Tuple[List[str], str], None]:
            Queries merriam-webster.com for definitions.
        _query_synonym_com() -> Union[Tuple[List[str], str], None]:
            Queries synonym.com for definitions.
        _query_thesaurus_com() -> Union[Tuple[List[str], str], None]:
            Queries thesaurus.com for definitions.
        """
    def __init__(self,
                 search_string: str = '',
                 sources: Optional[List[str]] = None,
                 output_format: str = 'list',
                 max_number_of_requests: int = 30,
                 rate_limit_timeout_period: int = 60,
                 user_agent: Optional[str] = None,
                 proxies: Optional[Dict[str, str]] = None):

        self._proxies = proxies
        self._word = search_string
        self._user_agent = user_agent
        self._output_format = output_format
        self._valid_output_formats = {'dictionary', 'list', 'json'}
        self._sources = sources

        rate_limit_status = False
        self._rate_limit_status = rate_limit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(wait_gen=expo,
                               exception=RateLimitException,
                               max_time=60,
                               on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the definition repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self._run_query_tasks_in_parallel = handler(limiter(self._run_query_tasks_in_parallel))

    def _backoff_handler(self, details) -> None:
        """
        Handles the backoff mechanism when the rate limit for querying definition is reached.

        This method is triggered when the rate limit is encountered. It logs the rate limit event and displays
        colorized messages indicating that the process is entering a temporary hibernation mode. If the rate
        limit has already been reached, it continues to display colorized backoff messages for subsequent
        retries.

        :param details: A dictionary containing information about the backoff event, including:
                        - 'wait' (float): The number of seconds to wait before retrying.
                        - 'tries' (int): The number of retry attempts made so far.
                        - Additional details such as 'target', 'args', 'kwargs', 'elapsed', and 'exception' which provide
                          context about the event (not used in this method but part of the details dictionary).

        type details: Dict

        Side Effects:
        - Displays colorized text messages to indicate the backoff status.
        - Logs an info message when the rate limit is initially reached.
        - Sets the `_rate_limit_status` attribute to True when the rate limit is first encountered.

        :returns: None
        :rtype: NoneType
        """
        if self._rate_limit_status is False:
            colorized_text(text='The definition query rate limit was reached. The querying process is '
                                'entering a temporary hibernation mode.', color='red')
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')
            logger.info('The definition query rate limit was reached.')
            self._rate_limit_status = True
        elif self._rate_limit_status is True:
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')

    def _validate_word(self) -> bool:
        """
        This function is designed to validate that the syntax for a string variable is in an acceptable format.

        :return: True or False
        :rtype: bool
        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if not valid_word:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')
        return valid_word

    def _check_cache(self) -> Tuple[bool, Union[Dict[str, List[str]], None]]:
        check_cache = caching.cache_definition(self._word)
        return check_cache

    def _update_cache(self, pos_category: str, definition: Union[List[str], Set[str]]) -> None:
        caching.insert_word_cache_definition(self._word, pos_category, definition)

    def _request_http_response(self, url: str) -> requests.models.Response:
        """
        This function queries the requested online repository and returns the
        response for this specific query.

        :param url: the URL for the online repository being queried
        :return: response content
        :rtype: requests.models.Response
        """
        response = None
        if self._proxies is None and self._user_agent is None:
            response = Query(url_to_scrape=url).get_website_html()
        elif self._proxies is None and self._user_agent is not None:
            response = Query(url_to_scrape=url, user_agent=self._user_agent).get_website_html()
        elif self._proxies is not None and self._user_agent is None:
            response = Query(url_to_scrape=url, user_agent=None, proxies=self._proxies).get_website_html()
        elif self._proxies is not None and self._user_agent is not None:
            response = Query(url_to_scrape=url, user_agent=self._user_agent, proxies=self._proxies).get_website_html()
        return response

    def _run_query_tasks_in_parallel(self) -> List[tuple[List[str], str]]:
        """
        Runs the query tasks in parallel using a ThreadPool.

        :return: list
        :rtype: nested list
        """
        sources: list = []
        if self._sources is None:
            sources = ['collins', 'merriam-webster', 'synonym.com', 'thesaurus.com']
        elif self._sources is not None:
            sources = self._sources
        else:
            colorized_text(text='Please verify that the sources that were provided are valid. \n'
                                'Valid Sources: \n'
                                '- collins \n'
                                '- merriam-webster \n'
                                '- synonym.com \n'
                                '- thesaurus.com', color='red')

        primary_sources = {'collins': self._query_collins_dictionary,
                           'merriam-webster': self._query_merriam_webster,
                           'synonym.com': self._query_synonym_com,
                           'thesaurus.com': self._query_thesaurus_com,}

        tasks = [v for k, v in primary_sources.items() if k in sources]

        with ThreadPoolExecutor(max_workers=5) as executor:
            running_tasks = []
            finished_tasks = []
            try:
                for task in tasks:
                    submitted_task = executor.submit(task)
                    running_tasks.append(submitted_task)
                for finished_task in as_completed(running_tasks):
                    finished_tasks.append(finished_task.result())
            except (BrokenExecutor, BrokenThreadPool, TimeoutError) as error:
                self._handle_query_exceptions(error)
            return finished_tasks

    def _query_output(self, definitions: list, part_of_speech: Union[set[str], str]) -> Union[list, dict, str]:
        """
            Process the output format based on the specified format.

            :param definitions: List of synonyms to process.
            :param type definitions: list
            :param part_of_speech: Part of speech associated with the definitions.
            :param part_of_speech: Union[set[str], str]

            :returns: Processed output based on the specified output format:
                - If output format is 'list', returns a sorted list of lowercase definitions.
                - If output format is 'dictionary', returns a dictionary with the word,
                  part of speech, and sorted definitions.
                - If output format is 'json', returns a JSON object with the word,
                  part of speech, and sorted definitions.
            :rtype: Union[list, dict, str]
            """
        processed_output = None
        if self._output_format == 'list':
            processed_output = sorted({word.lower() for word in definitions})
        elif self._output_format == 'dictionary':
            processed_output = {self._word: {'part_of_speech': ''.join(part_of_speech),
                                             'definitions': sorted(set(definitions))}}
        elif self._output_format == 'json':
            processed_output = json.dumps({self._word:
                                               {'part_of_speech': ''.join(part_of_speech),
                                                'definitions': sorted(set(definitions), key=len)}}, indent=4, ensure_ascii=False)
        return processed_output

    def find_definitions(self) -> Union[List[Sized], Dict[str, List[str]], str]:
        """
        This function queries multiple online repositories to discover definitions related
        with the specific word provided to the Class Definitions.

        :return: list of definitions
        :rtype: list

        """
        if self._output_format not in self._valid_output_formats:
            colorized_text(f'The provided output type --> {self._output_format} <-- is not one of the '
                           f'acceptable types: dictionary, list or json.', 'red')
            sys.exit(1)
        else:
            valid_word = self._validate_word()
            if valid_word is False:
                colorized_text(f'Please verify that the word {self._word} is spelled correctly.', 'magenta')
            elif valid_word is True:
                check_cache = self._check_cache()
                if check_cache[0] is True:
                    part_of_speech = list(check_cache[1].keys())[0]
                    definitions = cleansing.flatten_multidimensional_list(list(check_cache[1].values()))
                    return self._query_output(definitions, part_of_speech)
                elif check_cache[0] is False:
                    query_results = self._run_query_tasks_in_parallel()
                    part_of_speech = {x[1] for x in query_results if x and x is not None}
                    definitions = ([x[0] for x in query_results if x and x is not None])
                    # flatten definitions list
                    definitions = cleansing.flatten_multidimensional_list(definitions)
                    # remove excess white spaces from the strings in the list
                    definitions = [regex.sub(' +', " ", x) for x in definitions]
                    if not definitions:
                        colorized_text(text=f'No definitions were found for the word: {self._word} \n'
                                       f'Please verify that the word is spelled correctly.', color='blue')
                    else:
                        return self._query_output(definitions, part_of_speech)

    @staticmethod
    def _handle_query_exceptions(error):
        """
        Helper method to handle common exceptions in query methods.
        """
        logger.error('An error occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _query_collins_dictionary(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries collinsdictionary.com for a definition associated
        with the specific word provided to the Class Definitions.

        :returns:definition for a word
        :rtype: Union[Tuple[List[str], str], None]
        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        try:
            response = self._request_http_response(url=f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}')

            if response.status_code == 404:
                logger.error(f'Collins Dictionary had no definition reference for the word {self._word}')
                return None
            else:
                soup_object = BeautifulSoup(markup=response.text, features="lxml")
                cloudflare_protection = CloudflareVerification(url='https://www.collinsdictionary.com',
                                                               soup=soup_object).cloudflare_protected_url()

                if cloudflare_protection is False:
                    definition_list = ParseDefinitions.parse_collins_dictionary(soup=soup_object, word=self._word)
                    part_of_speech_category = PartOfSpeech.part_of_speech_category_collins_dictionary(soup=soup_object)
                    self._update_cache(pos_category=part_of_speech_category, definition=definition_list)
                    return definition_list, part_of_speech_category
                elif cloudflare_protection is True:
                    soup_object = Cloudflare(url=f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}').bypass()
                    if soup_object:
                        definition_list = ParseDefinitions.parse_collins_dictionary(soup=soup_object, word=self._word)
                        part_of_speech_category = PartOfSpeech.part_of_speech_category_collins_dictionary(soup_object)
                        self._update_cache(pos_category=part_of_speech_category, definition=definition_list)
                        return definition_list, part_of_speech_category
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            self._handle_query_exceptions(error)

    def _query_merriam_webster(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries merriam-webster.com for a definition associated
        with the specific word provided to the Class Definitions

        :returns:definition for a word
        :rtype: Union[Tuple[List[str], str], None]
        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        try:
            response = self._request_http_response(url=f'https://www.merriam-webster.com/dictionary/{self._word}')

            if response.status_code == 404:
                logger.info(f'Merriam-webster.com has no definition reference for the word {self._word}')
                return None
            else:
                soup_object = BeautifulSoup(markup=response.text, features="lxml")
                cloudflare_protection = CloudflareVerification(url='https://www.merriam-webster.com',
                                                               soup=soup_object).cloudflare_protected_url()

                if cloudflare_protection is False:
                    pattern = regex.compile(pattern=r'Words fail us')
                    if soup_object.find(text=pattern):
                        logger.info(f'Merriam-webster.com has no reference for the word {self._word}')
                        return None
                    elif soup_object.find(name='h1', attrs={'class': 'mispelled-word'}):
                        logger.info(f'Merriam-webster.com has no definition reference for the word {self._word}')
                        return None
                    else:
                        definition_list = ParseDefinitions.parse_merriam_webster(soup=soup_object)
                        part_of_speech_category = PartOfSpeech.part_of_speech_category_merriam_webster(soup=soup_object)
                        self._update_cache(pos_category=part_of_speech_category, definition=definition_list)
                        return definition_list, part_of_speech_category
                elif cloudflare_protection is True:
                    return None
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            self._handle_query_exceptions(error)

    def _query_synonym_com(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries synonym.com for a definition associated
        with the specific word provided to the Class Definitions

        :returns:definition for a word
        :rtype: Union[Tuple[List[str], str], None]
        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        try:
            response = self._request_http_response(url=f'https://www.synonym.com/synonyms/{self._word}')

            if response.status_code == 404:
                logger.info(f'Synonym.com had no definition reference for the word {self._word}')
                return None
            else:
                soup_object = BeautifulSoup(markup=response.text, features="lxml")
                cloudflare_protection = CloudflareVerification(url='https://www.synonym.com',
                                                               soup= soup_object).cloudflare_protected_url()
                if cloudflare_protection is False:
                    status_tag =  soup_object.find(name="meta", attrs={"name": "pagetype"})
                    pattern = regex.compile(pattern=r'Oops, 404!')
                    if  soup_object.find(text=pattern):
                        logger.info(f'Synonym.com had no definition reference for the word {self._word}')
                        return None
                    elif status_tag.attrs['content'] == 'Term':
                        definition_list = ParseDefinitions.parse_synonym_com(soup=soup_object)
                        part_of_speech_category = PartOfSpeech.part_of_speech_category_synonym_com(soup=soup_object)
                        self._update_cache(pos_category=part_of_speech_category, definition=definition_list)
                        return definition_list, part_of_speech_category
                elif cloudflare_protection is True:
                    return None
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            self._handle_query_exceptions(error)

    def _query_thesaurus_com(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries thesaurus.com for a definition associated
        with the specific word provided to the Class Definitions.

        :returns:definition for a word
        :rtype: Union[Tuple[List[str], str], None]
        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        try:
            response = self._request_http_response(url=f'https://www.thesaurus.com/browse/{self._word}')

            if response.status_code == 404:
                logger.info(f'Thesaurus.com had no definition reference for the word {self._word}')
                return None
            else:
                soup_object = BeautifulSoup(markup=response.text, features="lxml")
                cloudflare_protection = CloudflareVerification(url='https://www.thesaurus.com',
                                                               soup=soup_object).cloudflare_protected_url()
                if cloudflare_protection is False:
                    status_tag = soup_object.find(name="h1")
                    if status_tag.text.startswith('0 results for'):
                        logger.info(f'Thesaurus.com had no definition reference for the word {self._word}')
                        return None
                    else:
                        definition_list = ParseDefinitions.parse_thesaurus_com(soup=soup_object)
                        part_of_speech_category = PartOfSpeech.part_of_speech_category_thesaurus_com(soup=soup_object)
                        self._update_cache(pos_category=part_of_speech_category, definition=definition_list)
                        return definition_list, part_of_speech_category
                elif cloudflare_protection is True:
                    return None
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            self._handle_query_exceptions(error)
