#!/usr/bin/env python3

"""
This Python script is designed to query a online repository for the
hypernyms associated with a specific word.
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
# Date Last Revised: April 04, 2022
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
import traceback
from bs4 import BeautifulSoup
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException
from wordhoard.utilities.basic_soup import Query
from wordhoard.utilities import caching, cleansing, word_verification
from wordhoard.utilities.cloudflare_checker import CloudflareVerification

logger = logging.getLogger(__name__)


def _colorized_text(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"


def _get_number_of_pages(soup):
    """
    This function determines the number of pages that
    contain hypernyms and hyperonyms for a specific word.

    :param soup: BeautifulSoup lxml
    :return: number of pages
    :rtype: int

    :raises

        AttributeError: Raised when an attribute reference or assignment fails.

        KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

        TypeError: Raised when an operation or function is applied to an object of inappropriate type.
    """
    try:
        number_of_pages = 0
        pages = soup.find('div', {'id': 'pages'})
        if pages is not None:
            list_of_pages = [num for page in pages for num in page if num.isdigit()]
            if len(list_of_pages) != 0:
                number_of_pages = int(list_of_pages[-1]) + 1
        return number_of_pages

    except AttributeError as e:
        logger.error('An AttributeError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
    except KeyError as e:
        logger.error('A KeyError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
    except TypeError as e:
        logger.error('A TypeError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))


def _get_hypernyms(soup):
    """
    This function queries a HTML table for hypernyms.

    :param soup: BeautifulSoup lxml
    :return: set of hypernyms and hyperonyms
    :rtype: set

    :raises
        AttributeError: Raised when an attribute reference or assignment fails.

        KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys.

        TypeError: Raised when an operation or function is applied to an object of inappropriate type.
    """
    try:
        sub_set = set()
        table = soup.find('table')
        if table:
            rows = table.find_all('tr', {'class': 'theentry'})
            if rows is not None:
                for row in rows:
                    cols = row.find('td', {'class': 'abbdef'}).find('a')
                    if cols is not None:
                        if cols.text != '»':
                            sub_set.add(str(cols.text).lower())
                        else:
                            sub_set.add('no hypernyms found')
            return sub_set

    except AttributeError as e:
        logger.error('An AttributeError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
    except KeyError as e:
        logger.error('A KeyError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
    except TypeError as e:
        logger.error('A TypeError occurred in the following code segment:')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))


class Hypernyms(object):

    def __init__(self,
                 search_string='',
                 output_format='list',
                 max_number_of_requests=30,
                 rate_limit_timeout_period=60,
                 user_agent=None,
                 proxies=None):

        """
        Purpose
        ----------
        This Python class is used to query online repositories for the hypernyms
        associated with a specific word.

        Usage Examples
        ----------

        >>> hypernym = Hypernyms('red')
        >>> results = hypernym.find_hypernyms()

        >>> hypernym = Hypernyms(search_string='red')
        >>> results = hypernym.find_hypernyms()

        Parameters
        ----------
        :param search_string: string containing the variable to obtain hypernyms for

        :param max_number_of_requests: maximum number of requests for a specific timeout_period

        :param rate_limit_timeout_period: the time period before a session is placed in a temporary hibernation mode

        :param user_agent: string containing either a global user agent type or a specific user agent

        :param proxies: dictionary of proxies to use with Python Requests
        """

        self._proxies = proxies
        self._word = search_string
        self._user_agent = user_agent
        self._output_format = output_format

        rate_limit_status = False
        self._rate_limit_status = rate_limit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(expo, RateLimitException, max_time=60, on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the antonyms repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.find_hypernyms = handler(limiter(self.find_hypernyms))

    def _backoff_handler(self):
        if self._rate_limit_status is False:
            print(_colorized_text(255, 0, 0,
                                  'The hypernym query rate limit was reached. The querying process is entering '
                                  'a temporary hibernation mode.'))
            logger.info('The hypernym query rate limit was reached.')
            self._rate_limit_status = True

    def _validate_word(self):
        """
        This function is designed to validate that the syntax for
        a string variable is in an acceptable format.

        :return: True or False
        :rtype bool

        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if valid_word:
            return valid_word
        else:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')

    def _check_cache(self):
        check_cache = caching.cache_hypernyms(self._word)
        return check_cache

    def _update_cache(self, hypernym):
        caching.insert_word_cache_hypernyms(self._word, hypernym)
        return

    def find_hypernyms(self):
        """
        Purpose
        ----------
        This function queries classicthesaurus_com for hypernyms associated
        with the specific word provided to the Class Hypernyms.

        Returns
        ----------
        :returns:
            hypernym: list of hypernyms

        :rtype: list

        Raises
        ----------
        :raises
            AttributeError: Raised when an attribute reference or assignment fails

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys

            TypeError: Raised when an operation or function is applied to an object of inappropriate type

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        valid_word = self._validate_word()
        if valid_word:
            check_cache = self._check_cache()
            if check_cache[0] is True:
                hypernym = cleansing.flatten_multidimensional_list(list(check_cache[1]))
                if self._output_format == 'list':
                    return sorted(hypernym)
                elif self._output_format == 'dictionary':
                    output_dict = {self._word: sorted(set(hypernym))}
                    return output_dict
                elif self._output_format == 'json':
                    json_object = json.dumps({'hypernyms': {self._word: sorted(set(hypernym))}},
                                             indent=4, ensure_ascii=False)
                    return json_object

            elif check_cache[0] is False:
                try:
                    response = ''
                    if self._proxies is None:
                        if self._user_agent is None:
                            response = Query(
                                f'https://www.classicthesaurus.com/{self._word}/broader').get_single_page_html()
                        elif self._user_agent is not None:
                            response = Query(f'https://www.classicthesaurus.com/{self._word}/broader',
                                             user_agent=self._user_agent).get_single_page_html()

                    elif self._proxies is not None:
                        if self._user_agent is None:
                            response = Query(f'https://www.classicthesaurus.com/{self._word}/broader',
                                             proxies=self._proxies).get_single_page_html()
                        elif self._user_agent is not None:
                            response = Query(f'https://www.classicthesaurus.com/{self._word}/broader',
                                             user_agent=self._user_agent, proxies=self._proxies).get_single_page_html()

                    if response.status_code == 404:
                        logger.info(f'Classic Thesaurus had no hypernyms reference for the word {self._word}')
                    else:
                        soup = BeautifulSoup(response.text, "lxml")
                        cloudflare_protection = CloudflareVerification('https://www.classicthesaurus.com',
                                                                       soup).cloudflare_protected_url()
                        if cloudflare_protection is False:
                            hypernym = _get_hypernyms(soup)
                            if 'no hypernyms found' in hypernym:
                                return _colorized_text(255, 0, 255,
                                                       f'No hypernyms were found for the word: {self._word} \n'
                                                       f'Please verify that the word is spelled correctly.')
                            else:
                                number_of_pages = _get_number_of_pages(soup)
                                if number_of_pages >= 2:
                                    for page in range(2, number_of_pages):
                                        sub_html = ''
                                        if self._proxies is None:
                                            if self._user_agent is None:
                                                sub_html = Query(
                                                    f'https://www.classicthesaurus.com/{self._word}/broader/{page}').get_single_page_html()
                                            elif self._user_agent is not None:
                                                sub_html = Query(
                                                    f'https://www.classicthesaurus.com/{self._word}/broader/{page}',
                                                    user_agent=self._user_agent).get_single_page_html()
                                        elif self._proxies is not None:
                                            if self._user_agent is None:
                                                sub_html = Query(
                                                    f'https://www.classicthesaurus.com/{self._word}/broader/{page}',
                                                    proxies=self._proxies).get_single_page_html()
                                            elif self._user_agent is not None:
                                                sub_html = Query(
                                                    f'https://www.classicthesaurus.com/{self._word}/broader/{page}',
                                                    user_agent=self._user_agent,
                                                    proxies=self._proxies).get_single_page_html()

                                        sub_soup = BeautifulSoup(sub_html.text, 'lxml')
                                        additional_hypernym = _get_hypernyms(sub_soup)
                                        if additional_hypernym:
                                            hypernym.union(additional_hypernym)
                                self._update_cache(hypernym)
                                if self._output_format == 'list':
                                    return sorted(set(hypernym))
                                elif self._output_format == 'dictionary':
                                    output_dict = {self._word: sorted(set(hypernym))}
                                    return output_dict
                                elif self._output_format == 'json':
                                    json_object = json.dumps({'hypernyms': {self._word: sorted(set(hypernym))}},
                                                             indent=4, ensure_ascii=False)
                                    return json_object
                        elif cloudflare_protection is True:
                            logger.info('-' * 80)
                            logger.info(f'The following URL has Cloudflare DDoS mitigation service protection.')
                            logger.info('https://www.classicthesaurus.com')
                            logger.info('-' * 80)
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
