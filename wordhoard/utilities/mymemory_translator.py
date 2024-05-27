#!/usr/bin/env python3

"""
This Python module is used to translate a specific word from it source language,
such as Spanish into American English using the MyMemory Translation service.
"""
__author__ = 'John Bumgarner'
__date__ = 'September 24, 2021'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"

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
# Date Completed: September 24, 2021
# Author: John Bumgarner
#
# Date Last Revised: May 25, 2024
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
# Standard library imports
import ast
import sys
import logging
import traceback
from string import punctuation
from typing import Dict, Optional, Tuple, Union

# Third-party imports
import requests
from requests.adapters import Retry
from requests.adapters import HTTPAdapter
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException

# Local or project-specific imports
from wordhoard.utilities.exceptions import RequestException
from wordhoard.utilities.colorized_text import colorized_text
from wordhoard.utilities.translator_languages import Languages
from wordhoard.utilities.user_agents import get_random_user_agent
from wordhoard.utilities.exceptions import InvalidLengthException
from wordhoard.utilities.exceptions import TooManyRequestsException
from wordhoard.utilities.exceptions import InvalidEmailAddressException
from wordhoard.utilities.exceptions import LanguageNotSupportedException
from wordhoard.utilities.email_address_verification import validate_address

logger = logging.getLogger(__name__)

class Translator:
    """
        This class provides translation capabilities using the MyMemory Translation service.
        It supports translating words from one language to another and handling various exceptions
        that may occur during translation requests.

        Args:
            source_language (str): The source language for translation. Defaults to an empty string.
            str_to_translate (str): The text to translate. Defaults to an empty string.
            email_address (str): The email address for authentication. Defaults to an empty string.
            proxies (Optional[Dict[str, str]]): Dictionary of proxy servers. Defaults to None.

        Attributes:
            _source_language (str): The source language for translation.
            _str_to_translate (str): The text to translate.
            _url_to_query (str): The API endpoint for translation requests.
            _email_address (str): The email address for authentication.
            _proxies (Optional[Dict[str, str]]): Dictionary of proxy servers.
            _headers (Dict[str, str]): HTTP headers for requests.
            _rate_limit_status (bool): A flag indicating the rate limit status for translation requests.

        Methods:
            __init__: Initializes the Translator object with source language, text to translate, email address, and proxies.
            _backoff_handler: Handles rate limit exceeded situations by logging and setting rate_limit_status.
            _mymemory_supported_languages: Checks if the source language is supported by MyMemory Translation service.
            _requests_retry_session: Configures a retry session for handling HTTP request retries.
            _handle_custom_exceptions: Handles custom exceptions specific to MyMemory Translation service.
            _mymemory_translate: Translates text from the source language to English using MyMemory Translation service.
            _mymemory_translate_reverse: Translates text from English to the source language using MyMemory Translation service.
            translate_word: Translates text from the source language to English, handling unsupported languages.
            reverse_translate: Translates text from English to the source language.

        Note:
            This class requires the 'requests', 'backoff', and 'ratelimit' modules for handling HTTP requests
            and rate limiting. Ensure these modules are installed and configured correctly for translation operations.
        """
    def __init__(self,
                 source_language: str = '',
                 str_to_translate: str = '',
                 email_address: str = '',
                 max_number_of_requests: int = 30,
                 rate_limit_timeout_period: int = 60,
                 proxies: Optional[Dict[str, str]] = None
                 ):

        self._source_language = source_language
        self._str_to_translate = str_to_translate
        self._url_to_query = 'http://api.mymemory.translated.net/get'
        self._email_address = email_address
        self._proxies = proxies

        rand_user_agent = get_random_user_agent()
        http_headers = {'user-agent': rand_user_agent}
        self._headers = http_headers

        ratelimit_status = False
        self._rate_limit_status = ratelimit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(wait_gen=expo,
                               exception=RateLimitException,
                               max_time=60,
                               on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the MyMemory translation service
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.translate_word = handler(limiter(self.translate_word))
        self.reverse_translate = handler(limiter(self.reverse_translate))

    def _backoff_handler(self, details) -> None:
        """
        Handles the backoff mechanism when the rate limit for querying the MyMemory translation service is reached.

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
            colorized_text(text='The MyMemory translation service query rate limit was reached. '
                                'The querying process is entering a temporary hibernation mode.', color='red')
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')
            logger.info('The MyMemory translation service query rate limit was reached.')
            self._rate_limit_status = True
        elif self._rate_limit_status is True:
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')

    def _mymemory_supported_languages(self) -> Union[str, None]:
        """
        This function determines if the requested source language is
        one supported languages for the MyMemory Translator.

        :return: language
        :rtype: string
        """
        languages = Languages()
        mymemory_languages = languages.mymemory_supported_languages()
        mymemory_languages_str = str(mymemory_languages)
        supported_languages = ast.literal_eval(mymemory_languages_str)
        try:
            if self._source_language in supported_languages.keys():
                return self._source_language
            elif self._source_language in supported_languages.values():
                return self._source_language
            else:
                return None
        except LanguageNotSupportedException as error:
            logger.info('The language provided is not one of the supported languages of the MyMemory Translation service.')
            logger.info(f'Requested language: {self._source_language}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    # reference: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    @staticmethod
    def _requests_retry_session(retries: int = 5,
                                backoff_factor: float = 0.5,
                                status_forcelist: Tuple[int] = (500, 502, 503, 504),
                                session: requests.sessions.Session = None,
                                ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        http_adapter = HTTPAdapter(max_retries=retry)
        session.mount(prefix='http://', adapter=http_adapter)
        session.mount(prefix='https://', adapter=http_adapter)
        return session

    def _handle_custom_exceptions(self, error):
        """
        Helper method to handle custom exceptions
        """
        if isinstance(error, InvalidEmailAddressException):
            colorized_text(text='The email address provided for authentication to the MyMemory Translation service '
                                'is invalid.', color='red')
            logger.error('Invalid Email Address Error:')
            logger.error('The email address provided for authentication to the MyMemory Translation service '
                         'is invalid.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        elif isinstance(error, InvalidLengthException):
            colorized_text(text=f'The text length for the word: "{self._str_to_translate}" exceed the length limit '
                                f'of MyMemory translation service.', color='red')
            logger.error(f'The text length for the word: "{self._str_to_translate}" exceed the length limit of '
                         f'MyMemory Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        elif isinstance(error, RequestException):
            colorized_text(text='An ambiguous connection exception has occurred when contacting the MyMemory Translation '
                     'service. Please check the WordHoard log file for additional information.', color='red')
            logger.error('Connection Exception:')
            logger.error('An ambiguous connection exception has occurred when communicating with the '
                         'MyMemory Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        elif isinstance(error, TooManyRequestsException):
            colorized_text(text='There has been too many connection requests to the MyMemory Translation service.',
                           color='red')
            logger.error('Connection Request Error:')
            logger.error('There has been too many connection requests to the MyMemory Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _mymemory_translate(self, original_language: str) -> Union[str, None]:
        """
        This function is used to translate a word from it source language, such as Spanish into American English.

        :param original_language: language to translated from
        :return: translated word
        :rtype: string or None
        """
        try:
            if not validate_address(email_address=self._email_address):
                colorized_text(text='A valid email address is required to use the MyMemory Translation service.',
                               color='red')
                sys.exit(1)

            response = self._requests_retry_session().get(self._url_to_query,
                                                          params={'langpair': f'{original_language}|en-us',
                                                                  'q': self._str_to_translate,
                                                                  'de': self._email_address},
                                                          headers=self._headers,
                                                          proxies=self._proxies)

            if response.status_code == 429:
                # HTTP 429 -- Too Many Requests response status code indicates the user has
                # sent too many requests in a given amount of time ("rate limiting")
                raise TooManyRequestsException()
            if response.status_code not in (200, 429):
                raise RequestException()

            data = response.json()
            if not data:
                colorized_text(text=f'MyMemory could not translate the word "{self._str_to_translate}".',
                               color='magenta')
                return None

            translation = data.get('responseData').get('translatedText')
            if translation != 'INVALID EMAIL PROVIDED':
                return str(translation).lower().rstrip(punctuation)
            elif translation == 'INVALID EMAIL PROVIDED':
                raise InvalidEmailAddressException()

        except (InvalidEmailAddressException, InvalidLengthException, TooManyRequestsException, RequestException) as error:
            self._handle_custom_exceptions(error)

    def _mymemory_translate_reverse(self) -> Union[str, None]:
        """
        This function is used to translate a word from it source language, such as Spanish into American English.

        :return: translated word
        :rtype: string or None
        """
        try:
            if not validate_address(email_address=self._email_address):
                colorized_text(text='A valid email address is required to use the MyMemory Translation service.',
                               color='red')
                sys.exit(1)

            response = self._requests_retry_session().get(url=self._url_to_query,
                                                          params={'langpair': f'en-us|{self._source_language}',
                                                                  'q': self._str_to_translate,
                                                                  'de': self._email_address},
                                                          headers=self._headers,
                                                          proxies=self._proxies
                                                          )

            if response.status_code == 429:
                # HTTP 429 -- Too Many Requests response status code indicates the user has
                # sent too many requests in a given amount of time ("rate limiting")
                raise TooManyRequestsException()
            if response.status_code not in (200, 429):
                raise RequestException()

            data = response.json()
            if not data:
                colorized_text(text=f'MyMemory could not translate the word "{self._str_to_translate}".',
                               color='magenta')
                return None

            translation = data.get('responseData').get('translatedText')
            if translation != 'INVALID EMAIL PROVIDED':
                return str(translation).lower().rstrip(punctuation)
            elif translation == 'INVALID EMAIL PROVIDED':
                raise InvalidEmailAddressException()

        except (InvalidEmailAddressException, InvalidLengthException, TooManyRequestsException, RequestException) as error:
            self._handle_custom_exceptions(error)

    def translate_word(self) -> Union[str, None]:
        """
        This function is used to translate a word from it source language, such as Spanish into American English.

        :return: translated word
        :rtype: string
        """
        supported_language = self._mymemory_supported_languages()
        if supported_language:
            return self._mymemory_translate(supported_language)
        elif not supported_language:
            colorized_text(text='The language provided is not one of the supported languages for the MyMemory '
                           'Translation service.', color='red')
            colorized_text(text=f'Requested language: {self._source_language}', color='red')
            colorized_text(text='Please review the languages supported by the MyMemory Translate service\n'
                           'https://wordhoard.readthedocs.io/en/latest/translations'
                           '/mymemory_supported_translation_languages/', color='green')

            return None

    def reverse_translate(self) -> Union[str, None]:
        """
        This function is used to translate a word from American English into another language, such as Spanish.

        :return: translated word
        :rtype: string or None
        """
        return self._mymemory_translate_reverse()
