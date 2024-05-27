#!/usr/bin/env python3

"""
This Python script is designed to query an online repository for the
hyponyms associated with a specific word.
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
# Date Last Revised: May 10, 2024
# Revised by: John Bumgarner
###################################################################################

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
from typing import List, Dict, Optional, Set, Tuple, Union

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

class SoupParser:
    """
        Utility class for parsing HTML content using BeautifulSoup.

        This class provides static methods to handle common exceptions during HTML parsing and extract specific elements
        such as the number of pages containing hyponyms and hyponyms themselves.

        Methods
        ----------
        - _handle_query_exceptions(error):
            Helper method to handle common exceptions in query methods.

        - get_number_of_pages(soup: BeautifulSoup) -> int:
            Determines the number of pages containing hyponyms for a specific word.

        - get_hyponyms(soup: BeautifulSoup) -> Set[str]:
            Parses hyponyms from the HTML response of classicthesaurus_com.
    """
    @staticmethod
    def _handle_query_exceptions(error):
        """
        Helper method to handle common exceptions in query methods.
        """
        logger.error('An error occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(error.__traceback__)))

    @staticmethod
    def get_number_of_pages(soup: BeautifulSoup) -> int:
        """
        This function determines the number of pages that contain hyponyms for a specific word.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: number of pages
        :rtype: int

        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        number_of_pages = 0
        try:
            pages = soup.find(name='div', attrs={'id': 'pages'})
            if pages is not None:
                list_of_pages = [num for page in pages for num in page if num.isdigit()]
                if len(list_of_pages) != 0:
                    number_of_pages = int(list_of_pages[-1]) + 1
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            SoupParser._handle_query_exceptions(error)
        return number_of_pages

    @staticmethod
    def get_hyponyms(soup: BeautifulSoup) -> Set[str]:
        """
        Parses hyponyms from the HTML response of classicthesaurus_com.

        :param soup: BeautifulSoup object containing the HTML response
        :param type soup: bs4.BeautifulSoup
        :return: set of hyponyms
        :rtype: Set[str]

        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        sub_set: set = set()
        try:
            table = soup.find(name='table')
            if table:
                rows = table.find_all(name='tr', attrs={'class': 'theentry'})
                if rows is not None:
                    for row in rows:
                        cols = row.find(name='td', attrs={'class': 'abbdef'}).find(name='a')
                        if cols and cols.text != '»':
                            sub_set.add(str(cols.text).lower())
        except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
            SoupParser._handle_query_exceptions(error)
        return sub_set

class Hyponyms:
    """
        This Python class is used to query online repositories for the hyponyms associated with a specific word.

        Usage Examples
        ----------
        >>> hyponyms = Hyponyms('horse')
        >>> results = hyponyms.find_hyponyms()

        Parameters
        ----------
        search_string : str, optional
            The word for which hyponyms are to be found.
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
            The word to find hyponymsfor.
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
        find_hyponyms() -> Union[List[Sized], Dict[str, List[str]], str]:
            Finds hyponyms for the specified word.
        _validate_word() -> bool:
            Validates the syntax of the word.
        _check_cache() -> Tuple[bool, Union[Dict[str, List[str]], None]]:
            Checks if hyponyms are cached.
        _update_cache(hyponyms: List[str]) -> None:
            Updates the cache with new hyponyms.
        _request_http_response(url: str) -> requests.models.Response:
            Makes an HTTP request and returns the response.
        _run_query_tasks_in_parallel() -> List[tuple[List[str], str]]:
            Runs query tasks in parallel using a ThreadPool.
        _query_output(self, hyponyms: list) -> Union[list, dict, str]:
            Process the output format based on the specified format.
        _handle_query_exceptions(error):
            Handles common exceptions in query methods.
    """
    def __init__(self,
                 search_string: str = '',
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

        rate_limit_status = False
        self._rate_limit_status = rate_limit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(wait_gen=expo,
                               exception=RateLimitException,
                               max_time=60,
                               on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the hyponyms repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.find_hyponyms = handler(limiter(self.find_hyponyms))

    def _backoff_handler(self, details) -> None:
        """
        Handles the backoff mechanism when the rate limit for querying hyponyms is reached.

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
            colorized_text(text='The hyponyms query rate limit was reached. The querying process is '
                                'entering a temporary hibernation mode.', color='red')
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')
            logger.info('The hyponyms query rate limit was reached.')
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

    def _check_cache(self) -> Tuple[bool, Union[List[str], None]]:
        check_cache = caching.cache_hyponyms(self._word)
        return check_cache

    def _update_cache(self, hyponyms: List[str]) -> None:
        caching.insert_word_cache_hyponyms(self._word, hyponyms)

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

    @staticmethod
    def _handle_query_exceptions(error):
        """
        Helper method to handle common exceptions in query methods.
        """
        logger.error('An error occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _query_output(self, hyponyms: list) -> Union[list, dict, str]:
        """
            Process the output format based on the specified format.

            :param hyponyms: List of synonyms to process.
            :param type hyponyms: list

            :returns: Processed output based on the specified output format:
                - If output format is 'list', returns a sorted list of lowercase hyponyms.
                - If output format is 'dictionary', returns a dictionary with the word and sorted hyponyms.
                - If output format is 'json', returns a JSON object with the word and sorted hyponyms.
            :rtype: Union[list, dict, str]
            """
        processed_output = None
        if self._output_format == 'list':
            processed_output = [word.lower() for word in hyponyms]
        elif self._output_format == 'dictionary':
            processed_output = {self._word: [word.lower() for word in hyponyms]}
        elif self._output_format == 'json':
            processed_output = json.dumps({'hyponyms': {self._word: [word.lower() for word in hyponyms]}},
                                          indent=4, ensure_ascii=False)
        return processed_output

    def find_hyponyms(self) -> Union[List[str], Dict[str, List[str]], str, None]:
        """
        This function queries classicthesaurus_com for hyponyms associated
        with the specific word provided to the Class Hyponyms.

        :returns: list of hyponyms
        :rtype: Union[Tuple[List[str], str]

        :raises:
            - AttributeError: When an attribute reference or assignment fails.
            - IndexError: When a sequence subscript is out of range.
            - KeyError: When a mapping key is not found in the set of existing keys.
            - TypeError: When an operation or function is applied to an inappropriate type.
            - bs4.FeatureNotFound: Raised by the BeautifulSoup constructor if no parser with the requested features is found.
        """
        if self._output_format not in self._valid_output_formats:
            colorized_text(text=f'The provided output type --> {self._output_format} <-- is not one of the '
                           f'acceptable types: dictionary, list or json.', color='red')
            sys.exit(1)
        else:
            valid_word = self._validate_word()
            if valid_word is False:
                colorized_text(text=f'Please verify that the word {self._word} is spelled correctly.', color='magenta')
            elif valid_word is True:
                check_cache = self._check_cache()
                if check_cache[0] is True:
                    hyponyms = cleansing.flatten_multidimensional_list(check_cache[1])
                    return self._query_output(hyponyms)
                elif check_cache[0] is False:
                    try:
                        response = self._request_http_response(url=f'https://www.classicthesaurus.com/{self._word}/narrower')
                        if response.status_code == 404:
                            logger.info(f'Classic Thesaurus had no hyponyms reference for the word {self._word}')
                            return None
                        else:
                            soup_object = BeautifulSoup(markup=response.text, features="lxml")
                            cloudflare_protection = CloudflareVerification(url='https://www.classicthesaurus.com',
                                                                           soup=soup_object).cloudflare_protected_url()
                            if cloudflare_protection is False:
                                hyponym = SoupParser.get_hyponyms(soup=soup_object)
                                if 'no hyponyms found' in hyponym:
                                    colorized_text(text=f'No hyponyms were found for the word: {self._word} \n'
                                                   f'Please verify that the word is spelled correctly.', color='blue')
                                    return None
                                else:
                                    number_of_pages = SoupParser.get_number_of_pages(soup=soup_object)
                                    if number_of_pages >= 2:
                                        for page in range(2, number_of_pages):
                                            sub_html = self._request_http_response(url=f'https://www.classicthesaurus.com/{self._word}/narrower/{page}')
                                            sub_soup = BeautifulSoup(markup=sub_html.text, features='lxml')
                                            additional_hyponym = SoupParser.get_hyponyms(soup=sub_soup)
                                            hyponym.union(additional_hyponym)
                                    self._update_cache(sorted(hyponym))
                                    return self._query_output(list(sorted(hyponym)))
                            elif cloudflare_protection is True:
                                return None
                    except (bs4.FeatureNotFound, AttributeError, IndexError, KeyError, TypeError) as error:
                        self._handle_query_exceptions(error)
