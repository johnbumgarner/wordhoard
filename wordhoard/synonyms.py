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
# Date Last Revised: March 20, 2023
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
from wordhoard.utilities.cloudflare_bypass import Cloudflare
from wordhoard.utilities.colorized_text import colorized_text
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set, Sized, Tuple, Union
from wordhoard.utilities import caching, cleansing, word_verification
from wordhoard.utilities.cloudflare_checker import CloudflareVerification

logger = logging.getLogger(__name__)

class Synonyms(object):

    def __init__(self,
                 search_string: str = '',
                 output_format: str = 'list',
                 max_number_of_requests: int = 30,
                 rate_limit_timeout_period: int = 60,
                 user_agent: Optional[str] = None,
                 proxies: Optional[Dict[str, str]] = None):
        """
        This Python class is used to query multiple online repositories for the synonyms
        associated with a specific word.

        Usage Examples
        ----------

        >>> synonym = Synonyms('mother')
        >>> results = synonym.find_synonyms()

        >>> synonym = Synonyms(search_string='mother')
        >>> results = synonym.find_synonyms()

        Parameters
        ----------
        :param search_string: string containing the variable to obtain synonyms for

        :param output_format: Format to use for returned results.
               Default value: list; Acceptable values: dictionary or list

        :param max_number_of_requests: maximum number of requests for a specific timeout_period

        :param rate_limit_timeout_period: the time period before a session is placed in a temporary hibernation mode

        :param user_agent: string containing either a global user agent type or a specific user agent

        :param proxies: dictionary of proxies to use with Python Requests
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
        # Establishes a rate limit for making requests to the synonyms repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.find_synonyms = handler(limiter(self.find_synonyms))

    def _backoff_handler(self):
        if self._rate_limit_status is False:
            print(colorized_text(255, 0, 0,
                                 'The synonyms query rate limit was reached. The querying process is '
                                 'entering a temporary hibernation mode.'))
            logger.info('The synonyms query rate limit was reached.')
            self._rate_limit_status = True

    def _validate_word(self) -> bool:
        """
        This function is designed to validate that the syntax for
        a string variable is in an acceptable format.

        :return: True or False
        :rtype: bool
        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if valid_word:
            return True
        else:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')
            return False

    def _check_cache(self) -> Tuple[bool, Union[Dict[str, List[str]], None]]:
        check_cache = caching.cache_synonyms(self._word)
        return check_cache

    def _update_cache(self, pos_category: str, synonyms: Union[List[str], Set[str]]) -> None:
        caching.insert_word_cache_synonyms(self._word, pos_category, synonyms)
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
        tasks = [self._query_collins_dictionary, self._query_merriam_webster, self._query_synonym_com,
                 self._query_thesaurus_com, self._query_wordnet]

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

    def find_synonyms(self) -> Union[List[Sized], Dict[str, List[str]], str]:
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
        if self._output_format not in self._valid_output_formats:
            print(colorized_text(255, 0, 0,
                                 f'The provided output type --> {self._output_format} <-- is not one of the '
                                 f'acceptable types: dictionary, list or json.'))
        else:
            valid_word = self._validate_word()
            if valid_word is False:
                print(colorized_text(255, 0, 255,
                                  f'Please verify that the word {self._word} is spelled correctly.'))
            elif valid_word is True:
                check_cache = self._check_cache()
                if check_cache[0] is True:
                    part_of_speech = list(check_cache[1].keys())[0]
                    synonyms = cleansing.flatten_multidimensional_list(list(check_cache[1].values()))
                    if self._output_format == 'list':
                        return sorted(set([word.lower() for word in check_cache[1]]))
                    elif self._output_format == 'dictionary':
                        output_dict = {self._word: {'part_of_speech': part_of_speech, 'synonyms': sorted(set(
                            synonyms), key=len)}}
                        return output_dict
                    elif self._output_format == 'json':
                        json_object = json.dumps({self._word: {'part_of_speech': part_of_speech,
                                                               'synonyms': sorted(set(synonyms), key=len)}},
                                                 indent=4, ensure_ascii=False)
                        return json_object

                elif check_cache[0] is False:
                    query_results = self._run_query_tasks_in_parallel()

                    part_of_speech = ''.join(set([x[1] for x in query_results if x and x is not None]))

                    synonyms = ([x[0] for x in query_results if x and x is not None])
                    synonyms_results =  cleansing.flatten_multidimensional_list(synonyms)
                    # remove excess white spaces from the strings in the list
                    synonyms_results = cleansing.normalize_space(synonyms_results)
                    if not synonyms_results:
                        print(colorized_text(255, 0, 255,
                                             f'No synonyms were found for the word: {self._word} \n'
                                             f'Please verify that the word is spelled correctly.'))
                    else:
                        if self._output_format == 'list':
                            return sorted(set([word.lower() for word in synonyms_results]), key=len)
                        elif self._output_format == 'dictionary':
                            output_dict = {self._word: {'part_of_speech': part_of_speech, 'synonyms': sorted(set(
                                synonyms_results), key=len)}}
                            return output_dict
                        elif self._output_format == 'json':
                            json_object = json.dumps({self._word: {'part_of_speech': part_of_speech,
                                                                   'synonyms': sorted(set(synonyms_results), key=len)}},
                                                     indent=4, ensure_ascii=False)
                            return json_object


    def _query_collins_dictionary(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries collinsdictionary.com for synonyms associated
        with the specific word provided to the Class Synonyms.

        :returns:
            synonyms: list of synonyms

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
            response = self._request_http_response(f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{self._word}')

            if response.status_code == 404:
                logger.info(f'Collins Dictionary had no synonym reference for the word {self._word}')
                return None
            else:
                soup = BeautifulSoup(response.text, 'lxml')
                cloudflare_protection = CloudflareVerification('https://www.collinsdictionary.com',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    no_word_results = soup.find('h1',
                                           text=f'Sorry, no results for “{self._word}” in the English Thesaurus.')
                    if no_word_results:
                        logger.info(f'Collins Dictionary had no synonym reference for the word {self._word}')
                        return None
                    else:
                        part_of_speech_category = ''
                        # obtain the part of speech category for the specific word
                        if soup.find('span', {'class': 'headerSensePos'}):
                            tag_part_of_speech = soup.find('span', {'class': 'headerSensePos'})
                            if len(tag_part_of_speech.text) != 0:
                                part_of_speech_category = tag_part_of_speech.text.strip('()')
                            else:
                                part_of_speech_category = ''

                        synonyms = []
                        query_results = soup.find('div', {'class': 'blockSyn'})
                        if query_results:
                            for sub_syn in query_results.find_all('div', {'class', 'form type-syn'}):
                                child = sub_syn.findChild('span', {'class': 'orth'})
                                synonyms.append(child.text)
                            synonyms_list = sorted([x.lower().strip() for x in synonyms])
                            self._update_cache(part_of_speech_category, synonyms_list)
                            return synonyms_list, part_of_speech_category

                elif cloudflare_protection is True:
                    part_of_speech_category = ''

                    fresh_soup = Cloudflare(f'https://www.collinsdictionary.com/dictionary/english-thesaurus'
                                            f'/{self._word}').bypass()

                    # obtain the part of speech category for the specific word
                    if fresh_soup.find('span', {'class': 'headerSensePos'}):
                        tag_part_of_speech = fresh_soup.find('span', {'class': 'headerSensePos'})
                        if len(tag_part_of_speech.text) != 0:
                            part_of_speech_category = tag_part_of_speech.text.strip('()')
                        else:
                            part_of_speech_category = ''

                    synonyms = []
                    query_results = fresh_soup.find('div', {'class': 'blockSyn'})
                    if query_results:
                        for sub_syn in query_results.find_all('div', {'class', 'form type-syn'}):
                            child = sub_syn.findChild('span', {'class': 'orth'})
                            synonyms.append(child.text)

                        synonyms_list = sorted([x.lower().strip() for x in synonyms])
                        self._update_cache(part_of_speech_category, synonyms_list)
                        return synonyms_list, part_of_speech_category

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


    def _query_merriam_webster(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries merriam-webster.com for synonyms associated
        with the specific word provided to the Class Synonyms.

        :returns:
            synonyms: list of synonyms

        :rtype: list or None

        :raises:
           AttributeError: Raised when an attribute reference or assignment fails

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys

            TypeError: Raised when an operation or function is applied to an object of inappropriate type

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            response = self._request_http_response(f'https://www.merriam-webster.com/thesaurus/{self._word}')

            if response.status_code == 404:
                logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                return None
            else:
                soup = BeautifulSoup(response.text, "lxml")
                cloudflare_protection = CloudflareVerification('https://www.merriam-webster.com',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    pattern = regex.compile(r'Words fail us')
                    if soup.find(text=pattern):
                        logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                        return None
                    elif soup.find('h1', {'class': 'mispelled-word'}):
                        logger.info(f'Merriam-webster.com had no synonym reference for the word {self._word}')
                        return None
                    else:
                        synonyms_list = []
                        part_of_speech_category = ''

                        # obtain the part of speech category for the specific word
                        if soup.select('#thesaurus-entry-1-1 > div.row.entry-header > div > div > div.align-items-baseline.d-flex.flex-grow-1 > h2 > a'):
                            css_part_of_speech = soup.select(
                                '#thesaurus-entry-1-1 > div.row.entry-header > div > div > div.align-items-baseline.d-flex.flex-grow-1 > h2 > a')
                            if len(css_part_of_speech[0].text) != 0:
                                part_of_speech_category = css_part_of_speech[0].text
                            else:
                                part_of_speech_category = ''

                        if soup.find('p', {'class': 'function-label'}):
                            label = soup.find('p', {'class': 'function-label'})
                            if label.text.startswith('Synonyms'):
                                word_container = soup.find('div', {'class': 'thes-list-content synonyms_list'})
                                for list_item in word_container.find_all("li", {'class': 'thes-word-list-item'}):
                                    if list_item.find('span', {'class': 'lozenge color-4'}) or \
                                        list_item.find('span', {'class': 'lozenge color-3'}):
                                        link = list_item.find('a', href=True)
                                        synonyms_list.append(link.text.strip())
                                synonyms_list = sorted([x.lower().strip() for x in synonyms_list])
                                self._update_cache(part_of_speech_category, synonyms_list)
                            return synonyms_list, part_of_speech_category
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


    def _query_synonym_com(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries synonym.com for synonyms associated
        with the specific word provided to the Class Synonyms.

         :returns:
            synonyms: list of synonyms

        :rtype: list or None

        :raises:
            AttributeError: Raised when an attribute reference or assignment fails

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys

            TypeError: Raised when an operation or function is applied to an object of inappropriate type

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            response = self._request_http_response(f'https://www.synonym.com/synonyms/{self._word}')

            if response.status_code == 404:
                logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
                return None
            else:
                soup = BeautifulSoup(response.text, "lxml")
                cloudflare_protection = CloudflareVerification('https://www.synonym.com',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    status_tag = soup.find("meta", {"name": "pagetype"})
                    pattern = regex.compile(r'Oops, 404!')
                    if soup.find(text=pattern):
                        logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
                        return None
                    elif status_tag.attrs['content'] == 'Term':
                        part_of_speech_category = ''

                        if soup.find('div', {'data-section': 'synonyms'}):
                            synonyms_class = soup.find('div', {'data-section': 'synonyms'})
                            synonyms = [word.text for word in
                                        synonyms_class.find('ul', {'class': 'section-list'}).find_all('li')]
                            synonyms_list = sorted([x.lower().strip() for x in synonyms])

                            # obtain the part of speech category for the specific word
                            if soup.select('body > div.page-container > div.content-container > div.main-column > div.sections-wrapper > div:nth-child(1) > p > strong'):
                                css_part_of_speech = soup.select(
                                    'body > div.page-container > div.content-container > div.main-column > div.sections-wrapper > div:nth-child(1) > p > strong')
                                if len(css_part_of_speech[0].text) != 0:
                                    part_of_speech_category = css_part_of_speech[0].text.strip('.')
                                else:
                                    part_of_speech_category = ''

                            self._update_cache(part_of_speech_category, synonyms_list)
                            return synonyms_list, part_of_speech_category
                        else:
                            logger.info(f'Synonym.com had no synonym reference for the word {self._word}')
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


    def _query_thesaurus_com(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries thesaurus.com for synonyms associated
        with the specific word provided to the Class Synonyms.

        :returns:
            synonyms: list of synonyms

        :rtype: list or None

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
                logger.info(f'Thesaurus.com had no synonym reference for the word {self._word}')
                return None
            else:
                soup = BeautifulSoup(response.text, "lxml")
                cloudflare_protection = CloudflareVerification('https://www.thesaurus.com',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    status_tag = soup.find("h1")
                    if status_tag.text.startswith('0 results for'):
                        logger.info(f'Thesaurus.com had no synonym reference for the word {self._word}')
                        return None
                    else:
                        synonyms_list = []
                        part_of_speech_category = ''
                        # obtain the part of speech category for the specific word
                        if soup.select('#headword > div.css-bjn8wh.e1br8a1p0 > div > ul > li > a > em'):
                            css_part_of_speech = soup.select(
                            '#headword > div.css-bjn8wh.e1br8a1p0 > div > ul > li > a > em')
                            if len(css_part_of_speech[0].text) != 0:
                                part_of_speech_category = css_part_of_speech[0].text
                            else:
                                part_of_speech_category = ''
                        word_container = soup.find('div', {'data-testid': 'word-grid-container'})
                        for list_item in word_container.find('ul').find_all('li'):
                            for link in list_item.find_all('a', {'class': 'css-1kg1yv8 eh475bn0'}):
                                synonyms_list.append(link.text.strip())

                            synonyms_list = sorted([x.lower().strip() for x in  synonyms_list])
                        self._update_cache(part_of_speech_category, synonyms_list)
                        return synonyms_list, part_of_speech_category
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


    def _query_wordnet(self) -> Union[Tuple[List[str], str], None]:
        """
        This function queries wordnet for synonyms associated
        with the specific word provided to the Class Synonyms.

        :returns:
            synonyms: list of synonyms

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
            response = self._request_http_response(f'http://wordnetweb.princeton.edu/perl/webwn?s={self._word}')

            if response.status_code == 404:
                logger.info(f'Wordnet had no synonym reference for the word {self._word}')
                return None
            else:
                soup = BeautifulSoup(response.text, "lxml")
                cloudflare_protection = CloudflareVerification('http://wordnetweb.princeton.edu',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    pattern = regex.compile(r'Your search did not return any results')
                    if soup.find(text=pattern):
                        logger.info(f'Wordnet had no synonym reference for the word {self._word}')
                        return None
                    else:
                        synonyms_list = []
                        if soup.findAll('h3', text='Noun'):
                            part_of_speech_category = 'noun'
                            parent_node = soup.findAll("ul")[0].findAll('li')
                            for children in parent_node:
                                for child in children.find_all(href=True):
                                    if 'S:' not in child.contents[0]:
                                        synonyms_list.append(child.contents[0])
                            synonyms_list = sorted([x.lower().strip() for x in synonyms_list])
                            self._update_cache(part_of_speech_category, synonyms_list)
                            return synonyms_list, part_of_speech_category
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
