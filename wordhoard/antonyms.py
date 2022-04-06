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
import re as regex
from bs4 import BeautifulSoup
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException
from wordhoard.utilities.basic_soup import Query
from wordhoard.utilities import caching, cleansing, word_verification
from wordhoard.utilities.cloudflare_checker import CloudflareVerification

logger = logging.getLogger(__name__)


def _colorized_text(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"


class Antonyms(object):

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

        rate_limit_status = False
        self._rate_limit_status = rate_limit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(expo, RateLimitException, max_time=60, on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the antonyms repositories
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.find_antonyms = handler(limiter(self.find_antonyms))

    def _backoff_handler(self):
        if self._rate_limit_status is False:
            print(_colorized_text(255, 0, 0,
                                  'The antonyms query rate limit was reached. The querying process is entering a '
                                  'temporary hibernation mode.'))
            logger.info('The antonyms query rate limit was reached.')
            self._rate_limit_status = True

    def _validate_word(self):
        """
        This function is designed to validate that the syntax for
        a string variable is in an acceptable format.

        :return: True or False
        :rtype: boolean
        """
        valid_word = word_verification.validate_word_syntax(self._word)
        if valid_word:
            return valid_word
        else:
            logger.error(f'The word {self._word} was not in a valid format.')
            logger.error(f'Please verify that the word {self._word} is spelled correctly.')

    def _check_cache(self):
        check_cache = caching.cache_antonyms(self._word)
        return check_cache

    def _update_cache(self, antonyms):
        caching.insert_word_cache_antonyms(self._word, antonyms)
        return

    def find_antonyms(self):
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
        valid_word = self._validate_word()
        if valid_word:
            check_cache = self._check_cache()
            if check_cache[0] is True:
                antonyms = cleansing.flatten_multidimensional_list(check_cache[1])
                if self._output_format == 'list':
                    return sorted(set(antonyms))
                elif self._output_format == 'dictionary':
                    output_dict = {self._word: sorted(set(antonyms))}
                    return output_dict
                elif self._output_format == 'json':
                    json_object = json.dumps({'antonyms': {self._word: sorted(set(antonyms))}},
                                             indent=4, ensure_ascii=False)
                    return json_object

            elif check_cache[0] is False:
                antonyms_01 = self._query_thesaurus_com()
                antonyms_02 = self._query_wordhippo()
                antonyms = ([x for x in [antonyms_01, antonyms_02] if x is not None])
                antonyms_results = cleansing.flatten_multidimensional_list(antonyms)
                if len(antonyms_results) != 0:
                    if self._output_format == 'list':
                        return sorted(set(antonyms_results))
                    elif self._output_format == 'dictionary':
                        output_dict = {self._word: sorted(set(antonyms_results))}
                        return output_dict
                    elif self._output_format == 'json':
                        json_object = json.dumps({'antonyms': {self._word: sorted(set(antonyms_results))}},
                                                 indent=4, ensure_ascii=False)
                        return json_object
                else:
                    return _colorized_text(255, 0, 255,
                                           f'antonyms were found for the word: {self._word} \n'
                                           f'Please verify that the word is spelled correctly.')
        else:
            return _colorized_text(255, 0, 255, f'Please verify that the word {self._word} is spelled correctly.')

    def _query_thesaurus_com(self):
        """
        This function queries thesaurus.com for antonyms associated
        with the specific word provided to the Class Antonyms.

        :returns:
            antonyms: list of antonyms

        :rtype: list

        :raises
            AttributeError: Raised when an attribute reference or assignment fails

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys

            TypeError: Raised when an operation or function is applied to an object of inappropriate type

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            antonyms = []
            response = ''
            if self._proxies is None:
                if self._user_agent is None:
                    response = Query(f'https://www.thesaurus.com/browse/{self._word}').get_single_page_html()
                elif self._user_agent is not None:
                    response = Query(f'https://www.thesaurus.com/browse/{self._word}',
                                     user_agent=self._user_agent).get_single_page_html()
            elif self._proxies is not None:
                if self._user_agent is None:
                    response = Query(f'https://www.thesaurus.com/browse/{self._word}',
                                     proxies=self._proxies).get_single_page_html()
                elif self._user_agent is not None:
                    response = Query(f'https://www.thesaurus.com/browse/{self._word}',
                                     user_agent=self._user_agent, proxies=self._proxies, ).get_single_page_html()

            if response.status_code == 404:
                logger.info(f'Thesaurus.com had no antonym reference for the word {self._word}')
            else:
                soup = BeautifulSoup(response.text, "lxml")
                cloudflare_protection = CloudflareVerification('https://www.thesaurus.com',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    if soup.find("div", {'id': 'antonyms'}):
                        parent_tag = soup.find_all("div", {'data-testid': 'word-grid-container'})[1]
                        for link in parent_tag.find_all('a', {'class': 'css-pc0050'}):
                            antonyms.append(link.text.strip())
                        antonyms = sorted([x.lower() for x in antonyms])
                        self._update_cache(antonyms)
                        return antonyms
                    else:
                        logger.info(f'Thesaurus.com had no antonym reference for the word {self._word}')
                elif cloudflare_protection is True:
                    logger.info('-' * 80)
                    logger.info(f'The following URL has Cloudflare DDoS mitigation service protection.')
                    logger.info('https://www.thesaurus.com')
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

    def _query_wordhippo(self):
        """
        This function queries wordhippo.com for antonyms associated
        with the specific word provided to the Class Antonyms.

        :returns:
            antonyms: list of antonyms

        :rtype: list

        :raises
            AttributeError: Raised when an attribute reference or assignment fails

            IndexError: Raised when a sequence subscript is out of range

            KeyError: Raised when a mapping (dictionary) key is not found in the set of existing keys

            TypeError: Raised when an operation or function is applied to an object of inappropriate type

            bs4.FeatureNotFound: raised by the BeautifulSoup constructor if no parser with the requested features
            is found
        """
        try:
            antonyms = []
            response = ''
            if self._proxies is None:
                if self._user_agent is None:
                    response = Query(
                        f'https://www.wordhippo.com/what-is/the-opposite-of/{self._word}.html').get_single_page_html()
                elif self._user_agent is not None:
                    response = Query(f'https://www.wordhippo.com/what-is/the-opposite-of/{self._word}.html',
                                     user_agent=self._user_agent).get_single_page_html()
            elif self._proxies is not None:
                if self._user_agent is None:
                    response = Query(f'https://www.wordhippo.com/what-is/the-opposite-of/{self._word}.html',
                                     proxies=self._proxies).get_single_page_html()
                elif self._user_agent is not None:
                    response = Query(f'https://www.wordhippo.com/what-is/the-opposite-of/{self._word}.html',
                                     user_agent=self._user_agent, proxies=self._proxies).get_single_page_html()

            if response.status_code == 404:
                logger.info(f'Wordhippo.com had no antonym reference for the word {self._word}')
            else:
                soup = BeautifulSoup(response.text, "lxml")
                cloudflare_protection = CloudflareVerification('https://www.wordhippo.com',
                                                               soup).cloudflare_protected_url()
                if cloudflare_protection is False:
                    pattern = regex.compile(r'We do not currently know of any antonyms for')
                    if soup.find(text=pattern):
                        logger.info(f'Wordhippo.com had no antonym reference for the word {self._word}')
                    else:
                        related_tag = soup.find("div", {'class': 'relatedwords'})
                        if related_tag.find("div", {'class': 'wb'}) is not None:
                            for list_item in related_tag.find_all("div", {'class': 'wb'}):
                                for link in list_item.find_all('a', href=True):
                                    antonyms.append(link.text)
                            antonyms = sorted([x.lower() for x in antonyms])
                            self._update_cache(antonyms)
                            return antonyms
                        else:
                            for table_row in related_tag.find_all('td'):
                                for href_link in table_row.find('a', href=True):
                                    antonyms.append(href_link.text)
                            antonyms = sorted([x.lower() for x in antonyms])
                            self._update_cache(antonyms)
                            return antonyms
                elif cloudflare_protection is True:
                    logger.info('-' * 80)
                    logger.info(f'The following URL has Cloudflare DDoS mitigation service protection.')
                    logger.info('https://www.wordhippo.com')
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
