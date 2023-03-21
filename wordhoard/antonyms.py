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
# Date Completed: October 15, 2020
# Author: John Bumgarner
#
# Date Last Revised: March 19, 2023
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
import json
import logging
import requests
import traceback
import re as regex
from bs4 import BeautifulSoup
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException
from wordhoard.utilities.request_html import Query
from wordhoard.utilities.colorized_text import colorized_text
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set, Sized, Tuple, Union
from wordhoard.utilities import caching, cleansing, word_verification
from wordhoard.utilities.cloudflare_checker import CloudflareVerification


logger = logging.getLogger(__name__)


class Antonyms(object):

    def __init__(self,
                 search_string: str = '',
                 output_format: str = 'list',
                 max_number_of_requests: int = 30,
                 rate_limit_timeout_period: int = 60,
                 user_agent: Optional[str] = None,
                 proxies: Optional[Dict[str, str]] = None):
        """
        Purpose
        ----------

        This Python class is used to query multiple online repositories for the antonyms
        associated with a specific word.

        Usage Examples
        ----------

        >>> antonym = Antonyms('mother')
        >>> results = antonym.find_antonyms()

        >>> antonym = Antonyms(search_string='mother')
        >>> results = antonym.find_antonyms()

        Parameters
        ----------
        :param search_string: String containing the variable to obtain antonyms for

        :param output_format: Format to use for returned results.
               Default value: list; Acceptable values: dictionary or list

        :param max_number_of_requests: Maximum number of requests for a specific timeout_period

        :param rate_limit_timeout_period: The time period before a session is placed in a temporary hibernation mode

        :param user_agent: string containing either a global user agent type or a specific user agent

        :param proxies: Dictionary of proxies to use with Python Requests
        """

        self._proxies = proxies
        self._word = search_string
        self._user_agent = user_agent
        self._output_format = output_format
        self._valid_output_formats = {'dictionary', 'list', 'json'}

        rate_limit_status = False
        self._rate_limit_status = rate_limit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(expo, RateLimitException, max_time=60, on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the antonyms repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.find_antonyms = handler(limiter(self.find_antonyms))

    def _backoff_handler(self):
        if self._rate_limit_status is False:
            print(colorized_text(255, 0, 0,
                                 'The antonyms query rate limit was reached. The querying process is entering a '
                                 'temporary hibernation mode.'))
            logger.info('The antonyms query rate limit was reached.')
            self._rate_limit_status = True

    def _validate_word(self) -> bool:
        """
        This function is designed to validate that the syntax for a string variable is in an acceptable format.

        :return: True or False
        :rtype: boolean
        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if valid_word:
            return True
        else:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')
            return False

    def _check_cache(self) -> Tuple[bool, Union[Dict[str, List[str]], None]]:
        check_cache = caching.cache_antonyms(self._word)
        return check_cache

    def _update_cache(self, pos_category: str, antonyms: Union[List[str], Set[str]]) -> None:
        caching.insert_word_cache_antonyms(self._word, pos_category, antonyms)
        return

    def _request_http_response(self, url: str) -> requests.models.Response:
        """
        This function queries the requested online repository and returns the
        response for this specific query.

        :param url: the URL for the online repository being queried
        :return: response content
        :rtype: requests.models.Response
        """
        if self._proxies is None and self._user_agent is None:
            response = Query(url).get_website_html()
            return response
        elif self._proxies is None and self._user_agent is not None:
            response = Query(url, self._user_agent).get_website_html()
            return response
        elif self._proxies is not None and self._user_agent is None:
            response = Query(url, user_agent=None, proxies=self._proxies).get_website_html()
            return response
        elif self._proxies is not None and self._user_agent is not None:
            response = Query(url, user_agent=self._user_agent, proxies=self._proxies).get_website_html()
            return response

    def _run_query_tasks_in_parallel(self) -> List[str]:
        """
        Runs the query tasks in parallel using a ThreadPool.

        :return: list
        :rtype: nested list
        """
        tasks = [self._query_thesaurus_com, self._query_wordhippo]

        with ThreadPoolExecutor(max_workers=5) as executor:
            running_tasks = []
            finished_tasks = []
            try:
                for task in tasks:
                    submitted_task = executor.submit(task)
                    running_tasks.append(submitted_task)
                for finished_task in as_completed(running_tasks):
                    finished_tasks.append(finished_task.result())
                return finished_tasks
            except Exception as error:
                logger.error('An unknown error occurred in the following code segment:')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def find_antonyms(self) -> Union[List[Sized], Dict[str, List[str]], str]:
        """
        Purpose
        ----------
        This function queries multiple online repositories to discover antonyms
        associated with the specific word provided to the Class Antonyms.
        The antonyms are deduplicated and sorted alphabetically.

        Returns
        ----------
        :returns:
            antonyms: list of antonyms

        :rtype: list
        """
        if self._output_format not in self._valid_output_formats:
            print(colorized_text(255, 0, 0,
                                 f'The provided output type --> {self._output_format} <-- is not one of the '
                                 f'acceptable types: dictionary, list or json.'))
        else:
            valid_word = self._validate_word()
            if valid_word is False:
                print(colorized_text(255, 0, 255, f'Please verify that the word {self._word} is spelled correctly.'))
            elif valid_word is True:
                check_cache = self._check_cache()
                if check_cache[0] is True:
                    part_of_speech = list(check_cache[1].keys())[0]
                    antonyms = cleansing.flatten_multidimensional_list(list(check_cache[1].values()))
                    if self._output_format == 'list':
                        return antonyms
                    elif self._output_format == 'dictionary':
                        output_dict = {self._word: {'part_of_speech': part_of_speech,
                                                    'antonyms': sorted(set(antonyms), key=len)}}
                        return output_dict
                    elif self._output_format == 'json':
                        json_object = json.dumps({self._word: {'part_of_speech': part_of_speech,
                                                               'antonyms': sorted(set(antonyms), key=len)}},
                                                 indent=4, ensure_ascii=False)
                        return json_object

                elif check_cache[0] is False:
                    query_results = self._run_query_tasks_in_parallel()

                    part_of_speech = ''.join(set([x[1] for x in query_results if x and x is not None]))

                    antonyms = ([x[0] for x in query_results if x and x is not None])
                    # flatten antonyms list
                    antonyms_results = cleansing.flatten_multidimensional_list(antonyms)
                    # remove excess white spaces from the strings in the list
                    antonyms_results = cleansing.normalize_space(antonyms_results)

                    if len(antonyms_results) != 0:
                        if self._output_format == 'list':
                            return sorted(set(antonyms_results))
                        elif self._output_format == 'dictionary':
                            output_dict = {self._word: {'part_of_speech': part_of_speech,
                                                        'antonyms': sorted(set(antonyms_results), key=len)}}
                            return output_dict
                        elif self._output_format == 'json':
                            json_object = json.dumps({self._word: {'part_of_speech': part_of_speech,
                                                                   'antonyms': sorted(set(antonyms_results), key=len)}},
                                                     indent=4, ensure_ascii=False)

                            return json_object
                    else:
                        print(colorized_text(255, 0, 255,
                                             f'antonyms were found for the word: {self._word} \n'
                                             f'Please verify that the word is spelled correctly.'))

    def _query_thesaurus_com(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries thesaurus.com for antonyms associated
        with the specific word provided to the Class Antonyms.

        :returns:
            antonyms: list of antonyms

        :rtype: list

        :raises:
            AttributeError: Raised when an attribute reference or assignment fails

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys

            TypeError: Raised when an operation or function is applied to an object of inappropriate type

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            response = self._request_http_response(f'https://www.thesaurus.com/browse/{self._word}')

            if response.status_code == 404:
                logger.info(f'Thesaurus.com had no antonym reference for the word {self._word}')
                return None
            else:
                soup = BeautifulSoup(response.text, "lxml")
                cloudflare_protection = CloudflareVerification('https://www.thesaurus.com',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    antonyms_list = []
                    part_of_speech_category = ''

                    if soup.find("div", {'id': 'antonyms'}):
                        parent_tag = soup.find_all("div", {'data-testid': 'word-grid-container'})[1]
                        for link in parent_tag.find_all('a', {'class': 'css-pc0050'}):
                            antonyms_list.append(link.text.strip())
                        antonyms = sorted([x.lower() for x in antonyms_list])

                        # obtain the part of speech category for the specific word
                        if soup.select('#headword > div.css-bjn8wh.e1br8a1p0 > div > ul > li > a > em'):
                            css_part_of_speech = soup.select(
                                '#headword > div.css-bjn8wh.e1br8a1p0 > div > ul > li > a > em')
                            if len(css_part_of_speech[0].text) != 0:
                                part_of_speech_category = css_part_of_speech[0].text.rstrip('.')
                            else:
                                part_of_speech_category = ''

                        self._update_cache(part_of_speech_category, antonyms)
                        return antonyms_list, part_of_speech_category
                    else:
                        logger.info(f'Thesaurus.com had no antonym reference for the word {self._word}')
                        return None
                elif cloudflare_protection is True:
                    return None

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

    def _query_wordhippo(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries wordhippo.com for antonyms associated with the specific word provided
        to the Class Antonyms.

        :returns:
            antonyms: list of antonyms

        :rtype: list

        :raises:
            AttributeError: Raised when an attribute reference or assignment fails

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys

            TypeError: Raised when an operation or function is applied to an object of inappropriate type

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            response = self._request_http_response(f'https://www.wordhippo.com/what-is/the-opposite-of/{self._word}.html')

            if response.status_code == 404:
                logger.info(f'Wordhippo.com had no antonym reference for the word {self._word}')
                return None
            else:
                soup = BeautifulSoup(response.text, "lxml")
                cloudflare_protection = CloudflareVerification('https://www.wordhippo.com',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    pattern = regex.compile(r'We do not currently know of any antonyms for')
                    if soup.find(text=pattern):
                        logger.info(f'Wordhippo.com had no antonym reference for the word {self._word}')
                        return None
                    else:
                        antonyms_list = []
                        part_of_speech_category = ''

                        # obtain the part of speech category for the specific word
                        if soup.find("div", {'class': 'wordtype'}):
                            part_of_speech_tag = soup.find("div", {'class': 'wordtype'})
                            if len(part_of_speech_tag.text) != 0:
                                part_of_speech_category = ''.join(filter(str.isalpha, part_of_speech_tag.text)).lower()
                            else:
                                part_of_speech_category = ''

                        related_tag = soup.find("div", {'class': 'relatedwords'})
                        if related_tag.find("div", {'class': 'wb'}) is not None:
                            for list_item in related_tag.find_all("div", {'class': 'wb'}):
                                for link in list_item.find_all('a', href=True):
                                    antonyms_list.append(link.text)
                            antonyms = sorted([x.lower() for x in antonyms_list])
                            self._update_cache(part_of_speech_category, antonyms)
                            return antonyms, part_of_speech_category
                        else:
                            for table_row in related_tag.find_all('td'):
                                for href_link in table_row.find('a', href=True):
                                    antonyms_list.append(href_link.text)
                            antonyms = sorted([x.lower() for x in antonyms_list])
                            self._update_cache(part_of_speech_category, antonyms)
                            return antonyms, part_of_speech_category
                elif cloudflare_protection is True:
                    return None

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
