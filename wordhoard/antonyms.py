#!/usr/bin/env python3

"""
This Python module is designed to query multiple online repositories for the
antonyms associated with a specific word.
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
from wordhoard.utilities.colorized_text import colorized_text
from wordhoard.utilities import caching, cleansing, word_verification
from wordhoard.utilities.cloudflare_checker import CloudflareVerification

logger = logging.getLogger(__name__)

class PartOfSpeech:
    """
        This utility class contains static methods to extract part of speech categories
        from HTML responses of various sources, which are Thesaurus.com, and WordHippo.

        Static Methods
        --------------
        _handle_query_exceptions(error):
            Helper method to handle common exceptions in query methods.

        part_of_speech_category_thesaurus_com(soup: BeautifulSoup) -> str:
            Extracts the part of speech category from the HTML response of Thesaurus.com.

        part_of_speech_category_wordhippo(soup: BeautifulSoup) -> str:
            Extracts the part of speech category from the HTML response of WordHippo.
        """

    @staticmethod
    def _handle_query_exceptions(error):
        """
        Helper method to handle common exceptions in query methods.
        """
        logger.error('An error occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(error.__traceback__)))

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
            start_pattern = r'window\.__staticRouterHydrationData\s*=\s*JSON\.parse\('
            end_pattern = r'\);'
            script_tag = soup.find(name='script', text=regex.compile(start_pattern))
            if script_tag:
                match = regex.search(pattern=f'{start_pattern}(.*?){end_pattern}', string=script_tag.string)
                if match:
                    json_data_str = match.group(1).strip('"\'')
                    json_data_str = json_data_str.replace('\\"', '"')
                    pos_pattern = r'"partOfSpeech":"([^"]*)","shortDefinitions"'
                    pos_match = regex.search(pattern=pos_pattern, string=json_data_str)
                    if pos_match:
                        part_of_speech_category = pos_match.group(1).strip()
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            PartOfSpeech._handle_query_exceptions(error)
        return part_of_speech_category

    @staticmethod
    def part_of_speech_category_wordhippo(soup: BeautifulSoup) -> str:
        """
        Extracts the part of speech category from the HTML response of WordHippo.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: Part of speech category
        :rtype: str
        """
        part_of_speech_category: str = ''
        try:
            if soup.find(name="div", attrs={'class': 'wordtype'}):
                part_of_speech_tag = soup.find(name="div", attrs={'class': 'wordtype'})
                if len(part_of_speech_tag.text) != 0:
                    part_of_speech_category = ''.join(filter(lambda x: x.isalpha(), part_of_speech_tag.text)).lower()
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            PartOfSpeech._handle_query_exceptions(error)
        return part_of_speech_category

class ParseWords:
    """
        A utility class for parsing antonyms from various online sources.

        This class contains static methods to parse antonyms from HTML responses of various sources,
        which are Thesaurus.com and WordHippo.

        Methods
        -------
        _handle_query_exceptions(error):
            Helper method to handle common exceptions in query methods.

        parse_thesaurus_com(soup: BeautifulSoup) -> list:
            Parses antonyms from the HTML response of Thesaurus.com.

        parse_wordhippo(soup: BeautifulSoup) -> list:
            Parses antonyms from the HTML response of WordHippo.
        """

    @staticmethod
    def _handle_query_exceptions(error):
        """
        Helper method to handle common exceptions in query methods.
        """
        logger.error('An error occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(error.__traceback__)))

    @staticmethod
    def parse_google_com(soup: BeautifulSoup, word: str) -> list:
        """
        Parses synonyms from the HTML response of Thesaurus.com.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :param word: word to search
        :param type word: string
        :return: List of synonyms extracted from the HTML response
        :rtype: list
        """
        antonyms_list: list = []
        try:
            div_element = soup.find(name='div', string=f'What is the opposite of {word}?')
            if div_element:
                next_div = div_element.find_next_sibling(name='div')
                table_tag = next_div.find(name='table')
                if table_tag:
                    td_elements = table_tag.find_all(name='td')
                    for td_element in td_elements:
                        antonyms_list.append(td_element.text)
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            ParseWords._handle_query_exceptions(error)
        return antonyms_list

    @staticmethod
    def parse_thesaurus_com(soup: BeautifulSoup) -> list:
        """
        Parses synonyms from the HTML response of Thesaurus.com.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: List of synonyms extracted from the HTML response
        :rtype: list
        """
        antonyms_list: list = []
        try:
            start_pattern = r'window\.__staticRouterHydrationData\s*=\s*JSON\.parse\('
            end_pattern = r'\);'
            script_tag = soup.find(name='script', string=regex.compile(start_pattern))
            if script_tag:
                match = regex.search(pattern=f'{start_pattern}(.*?){end_pattern}', string=script_tag.string)
                if match:
                    json_data_str = match.group(1).strip('"\'')
                    json_data_str = json_data_str.replace('\\"', '"')
                    antonym_section = regex.search(pattern=r'\[{"antonyms":.*?}\]', string=json_data_str)
                    if antonym_section:
                        antonyms_similarity_section = regex.search(pattern=r'\{"similarity":-10,[^}]*\}\]',
                                                                   string=antonym_section.group(0))
                        if antonyms_similarity_section:
                            target_pattern = r'"targetWord"\s*:\s*"([^"]+)"'
                            target_antonym = regex.search(pattern=target_pattern,
                                                          string=antonyms_similarity_section.group(0))
                            if target_antonym:
                                antonyms_list.append(target_antonym.group(1))
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            ParseWords._handle_query_exceptions(error)
        return antonyms_list

    @staticmethod
    def parse_wordhippo(soup: BeautifulSoup) -> list:
        """
        Parses synonyms from the HTML response of Wordhippo.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: List of antonyms extracted from the HTML response
        :rtype: list
        """
        antonyms_list: list = []
        try:
            related_tag = soup.find(name="div", attrs={'class': 'relatedwords'})
            if related_tag.find(name="div", attrs={'class': 'wb'}) is not None:
                for list_item in related_tag.find_all(name="div", attrs={'class': 'wb'}):
                    for link in list_item.find_all(name='a', href=True):
                        antonyms_list.append(link.text)
            else:
                for table_row in related_tag.find_all(name='td'):
                    for href_link in table_row.find(name='a', href=True):
                        antonyms_list.append(href_link.text)
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            ParseWords._handle_query_exceptions(error)
        return sorted([x.lower() for x in antonyms_list])

class Antonyms:
    """
        A Python class for querying multiple online repositories to find antonyms for a specific word.

        Usage Examples
        ----------
        >>> antonym = Antonyms('mother')
        >>> results = antonym.find_antonyms()

        Parameters
        ----------
        search_string : str, optional
            The word for which antonyms are to be found.
        sources: Optional[List[str]]
            The sources to search for antonyms.
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
            The word to find antonyms for.
         _sources : Optional[List[str]]
            The sources to search for antonyms.
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
        find_antonyms() -> Union[List[Sized], Dict[str, List[str]], str]:
            Finds antonyms for the specified word.
        _validate_word() -> bool:
            Validates the syntax of the word.
        _check_cache() -> Tuple[bool, Union[Dict[str, List[str]], None]]:
            Checks if antonyms are cached.
        _update_cache(pos_category: str, antonyms: Union[List[str], Set[str]]) -> None:
            Updates the cache with new antonyms.
        _request_http_response(url: str) -> requests.models.Response:
            Makes an HTTP request and returns the response.
        _run_query_tasks_in_parallel() -> List[tuple[List[str], str]]:
            Runs query tasks in parallel using a ThreadPool.
        _query_output(self, antonyms: list, part_of_speech: Union[set[str], str]) -> Union[list, dict, str]:
            Process the output format based on the specified format.
        _handle_query_exceptions(error):
            Handles common exceptions in query methods.
        _query_google_com() -> Union[Tuple[List[str], str], None]:
            Queries google.com for antonyms.
        _query_thesaurus_com() -> Union[Tuple[List[str], str], None]:
            Queries thesaurus.com for antonyms.
        _query_wordhippo() -> Union[Tuple[List[str], str], None]:
            Queries wordhippo for antonyms.
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
        # Establishes a rate limit for making requests to the antonyms repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self._run_query_tasks_in_parallel = handler(limiter(self._run_query_tasks_in_parallel))

    def _backoff_handler(self, details) -> None:
        """
        Handles the backoff mechanism when the rate limit for querying antonyms is reached.

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
            colorized_text(text='The antonyms query rate limit was reached. The querying process is '
                                'entering a temporary hibernation mode.', color='red')
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')
            logger.info('The antonyms query rate limit was reached.')
            self._rate_limit_status = True
        elif self._rate_limit_status is True:
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')

    def _validate_word(self) -> bool:
        """
        This function is designed to validate that the syntax for a string variable is in an acceptable format.

        :return: True or False
        :rtype: boolean
        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if not valid_word:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')
        return valid_word

    def _check_cache(self) -> Tuple[bool, Union[Dict[str, List[str]], None]]:
        check_cache = caching.cache_antonyms(self._word)
        return check_cache

    def _update_cache(self, pos_category: str, antonyms: Union[List[str], Set[str]]) -> None:
        caching.insert_word_cache_antonyms(self._word, pos_category, antonyms)

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
            sources = ['google', 'thesaurus.com', 'wordhippo']
        elif self._sources is not None:
            sources = self._sources
        else:
            colorized_text(text='Please verify that the sources that were provided are valid. \n'
                                'Valid Sources: \n'
                                '- google \n'
                                '- thesaurus.com \n'
                                '- wordhippo', color='red')

        primary_sources = {'google': self._query_google,
                           'thesaurus.com': self._query_thesaurus_com,
                           'wordhippo': self._query_wordhippo}

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

    def _query_output(self, antonyms: list, part_of_speech: Union[set[str], str]) -> Union[list, dict, str]:
        """
            Process the output format based on the specified format.

            :param antonyms: List of synonyms to process.
            :param type antonyms: list
            :param part_of_speech: Part of speech associated with the antonyms.
            :param part_of_speech: Union[set[str], str]

            :returns: Processed output based on the specified output format:
                - If output format is 'list', returns a sorted list of lowercase antonyms.
                - If output format is 'dictionary', returns a dictionary with the word,
                  part of speech, and sorted antonyms.
                - If output format is 'json', returns a JSON object with the word,
                  part of speech, and sorted antonyms.
            :rtype: Union[list, dict, str]
            """
        processed_output = None
        if self._output_format == 'list':
            processed_output = sorted({word.lower() for word in antonyms})
        elif self._output_format == 'dictionary':
            processed_output = {self._word: {'part_of_speech': ''.join(part_of_speech),
                                             'antonyms': sorted(set(antonyms))}}
        elif self._output_format == 'json':
            processed_output = json.dumps({self._word:
                                               {'part_of_speech': ''.join(part_of_speech),
                                                'antonyms': sorted(set(antonyms), key=len)}}, indent=4, ensure_ascii=False)
        return processed_output

    def find_antonyms(self) -> Union[List[Sized], Dict[str, List[str]], str]:
        """
        This function queries multiple online repositories to discover antonyms
        associated with the specific word provided to the Class Antonyms.
        The antonyms are deduplicated and sorted alphabetically.

        :returns: antonyms with parts of speech
        :rtype: Union[List[Sized], Dict[str, List[str]], str]
        """
        if self._output_format not in self._valid_output_formats:
            colorized_text(text=f'The provided output type --> {self._output_format} <-- is not one of the '
                                f'acceptable types: dictionary, list or json.', color='red')
            sys.exit(1)
        else:
            valid_word = self._validate_word()
            if valid_word is False:
                colorized_text(text=f'Please verify that the word --> {self._word} <-- is spelled correctly.',
                               color='magenta')
            elif valid_word is True:
                check_cache = self._check_cache()
                if check_cache[0] is True:
                    part_of_speech = list(check_cache[1].keys())[0]
                    antonyms = cleansing.flatten_multidimensional_list(list(check_cache[1].values()))
                    return self._query_output(antonyms, part_of_speech)
                elif check_cache[0] is False:
                    query_results = self._run_query_tasks_in_parallel()
                    part_of_speech = {x[1] for x in query_results if x and x is not None}
                    antonyms = ([x[0] for x in query_results if x and x is not None])
                    # flatten antonyms list
                    antonyms_results = cleansing.flatten_multidimensional_list(sorted(antonyms))
                    # remove excess white spaces from the strings in the list
                    antonyms_results = cleansing.normalize_space(sorted(antonyms_results))
                    if not antonyms_results:
                        colorized_text(text=f'No antonyms were found for the word: {self._word} \n'
                                       f'Please verify that the word is spelled correctly.', color='blue')
                    else:
                        return self._query_output(antonyms_results, part_of_speech)

    @staticmethod
    def _handle_query_exceptions(error):
        """
        Helper method to handle common exceptions in query methods.
        """
        logger.error('An error occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _query_google(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries google.com for antonyms associated with the specific word provided to the Class Antonyms.

        :returns: list of antonyms and parts of speech str
        :rtype: Union[Tuple[List[str], str]
        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        try:
            response = self._request_http_response(url=f'https://www.google.com/search?q=antonym+for+/{self._word}')

            if response.status_code == 404:
                logger.info(f'Google had no antonym reference for the word {self._word}')
                return None
            else:
                soup_object = BeautifulSoup(markup=response.text, features="lxml")
                antonyms_list = ParseWords.parse_google_com(soup= soup_object, word=self._word)
                if antonyms_list:
                    self._update_cache(pos_category='noun', antonyms=sorted(antonyms_list))
                    return antonyms_list, 'noun'
                else:
                    logger.info(f'Google had no antonym reference for the word {self._word}')
                    return None
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            self._handle_query_exceptions(error)

    def _query_thesaurus_com(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries thesaurus.com for antonyms associated with the specific word provided to the Class
        Antonyms.

        :returns: list of antonyms and parts of speech str
        :rtype: Union[Tuple[List[str], str]
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
                logger.info(f'Thesaurus.com had no antonym reference for the word {self._word}')
                return None
            else:
                soup_object = BeautifulSoup(markup=response.text, features="lxml")
                cloudflare_protection = CloudflareVerification(url='https://www.thesaurus.com', soup=soup_object).cloudflare_protected_url()
                if cloudflare_protection is False:
                    antonym_button_tag = soup_object.find(name='button', attrs={'data-linkmodule': 'antonym-module'})
                    if antonym_button_tag:
                        antonyms_list = ParseWords.parse_thesaurus_com(soup=soup_object)
                        part_of_speech_category = PartOfSpeech.part_of_speech_category_thesaurus_com(soup=soup_object)
                        self._update_cache(pos_category=part_of_speech_category, antonyms=sorted(antonyms_list))
                        return antonyms_list, part_of_speech_category
                    else:
                        logger.info(f'Thesaurus.com had no antonym reference for the word {self._word}')
                        return None
                elif cloudflare_protection is True:
                    return None

        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            self._handle_query_exceptions(error)

    def _query_wordhippo(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries wordhippo.com for antonyms associated with the
        specific word provided to the Class Antonyms.

        :returns: list of antonyms and part of speech string
        :rtype: Union[Tuple[List[str], str], None]
        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        try:
            response = self._request_http_response(url=f'https://www.wordhippo.com/what-is/the-opposite-of/{self._word}.html')

            if response.status_code == 404:
                logger.info(f'Wordhippo.com had no antonym reference for the word {self._word}')
                return None
            else:
                soup_object = BeautifulSoup(markup=response.text, features="lxml")
                cloudflare_protection = CloudflareVerification(url='https://www.wordhippo.com', soup=soup_object).cloudflare_protected_url()
                if cloudflare_protection is False:
                    pattern = regex.compile(pattern=r'We do not currently know of any antonyms for')
                    if soup_object.find(text=pattern):
                        logger.info(f'Wordhippo.com had no antonym reference for the word {self._word}')
                        return None
                    else:
                        part_of_speech_category = PartOfSpeech.part_of_speech_category_wordhippo(soup=soup_object)
                        antonyms_list = ParseWords.parse_wordhippo(soup=soup_object)
                        self._update_cache(pos_category=part_of_speech_category, antonyms=sorted(antonyms_list))
                        return antonyms_list, part_of_speech_category
                elif cloudflare_protection is True:
                    return None
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            self._handle_query_exceptions(error)
