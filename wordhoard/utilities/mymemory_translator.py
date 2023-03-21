#!/usr/bin/env python3

"""
This Python script is used to translate a specific word from it source language,
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
# Date Last Revised: February 12, 2023
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import sys
import logging
import requests
import traceback
from string import punctuation
from requests.adapters import Retry
from backoff import on_exception, expo
from requests.adapters import HTTPAdapter
from typing import Dict, Optional, Tuple, Union
from ratelimit import limits, RateLimitException
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


class Translator(object):

    def __init__(self,
                 source_language: str = '',
                 str_to_translate: str = '',
                 email_address: str = '',
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
        handler = on_exception(expo, RateLimitException, max_time=60, on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the MyMemory translation service
        limiter = limits(calls=30, period=60)
        self.translate_word = handler(limiter(self.translate_word))
        self.reverse_translate = handler(limiter(self.reverse_translate))

    def _backoff_handler(self):
        if self._rate_limit_status is False:
            print(colorized_text(255, 0, 0,
                                 'The MyMemory translation service query rate Limit was reached. The querying '
                                 'process is entering a temporary hibernation mode.'))
            logger.info('The MyMemory translation service query rate limit was reached.')
            self._rate_limit_status = True

    def _mymemory_supported_languages(self) -> Union[str, None]:
        """
        This function determines if the requested source language is
        one supported languages for the MyMemory Translator.

        :return: language
        :rtype: string
        """
        languages = Languages()
        mymemory_languages = languages.mymemory_supported_languages()
        supported_languages = eval(str(mymemory_languages))
        try:
            if self._source_language in supported_languages.keys():
                return self._source_language
            elif self._source_language in supported_languages.values():
                return self._source_language
            else:
                return None
        except LanguageNotSupportedException as error:
            """
             An exception is thrown if the user uses a language that is not supported by the MyMemory Translation 
             service.
            """
            logger.info(f'The language provided is not one of the supported languages of the MyMemory '
                        f'Translation service.')
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
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _mymemory_translate(self, original_language: str) -> Union[str, None]:
        """
        This function is used to translate a word from it source language, such as Spanish into American English.

        :param original_language: language to translated from
        :return: translated word
        :rtype: string or None
        """
        try:
            if validate_address(self._email_address) is False:
                print(colorized_text(255, 0, 0,
                                     'A valid email address is required to use the MyMemory Translation '
                                     'service.'))
                sys.exit(1)
            elif validate_address(self._email_address) is True:
                response = self._requests_retry_session().get(self._url_to_query,
                                                              params={'langpair': f'{original_language}|en-us',
                                                                      'q': self._str_to_translate,
                                                                      'de': self._email_address},
                                                              headers=self._headers,
                                                              proxies=self._proxies
                                                              )

                if response.status_code == 429:
                    # HTTP 429 -- Too Many Requests response status code indicates the user has
                    # sent too many requests in a given amount of time ("rate limiting")
                    raise TooManyRequestsException()
                elif response.status_code != 200:
                    raise RequestException()
                else:
                    data = response.json()
                    if not data:
                        print(colorized_text(255, 0, 0,f'MyMemory could not translate the word '
                                                       f'{self._str_to_translate}.'))
                        return None

                    else:
                        translation = data.get('responseData').get('translatedText')
                        if translation == 'INVALID EMAIL PROVIDED':
                            raise InvalidEmailAddressException()
                        elif translation:
                            return str(translation).lower().rstrip(punctuation)

        except InvalidEmailAddressException as error:
            """
            This exception is thrown when the email address provided for authentication to the MyMemory Translation 
            service is invalid. 
            
            Please note that the MyMemory Translation service only validates the format of the email address and 
            not the validity of the address provided.
            """
            print(colorized_text(255, 0, 0, 'The email address provided for authentication to the MyMemory '
                                            'Translation service is invalid.'))
            logger.error('Invalid Email Address Error:')
            logger.error('The email address provided for authentication to the MyMemory Translation service '
                         'is invalid.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except InvalidLengthException as error:
            """
            This exception is thrown if the provided text exceed the length limit of the MyMemory Translator service.
            """
            print(colorized_text(255, 0, 0, f'The text length for the word: {self._str_to_translate} '
                                            f'exceed the length limit of MyMemory translation service.'))
            logger.error(f'The text length for the word: {self._str_to_translate} exceed the length limit of '
                         f'MyMemory Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except TooManyRequestsException as error:
            """
            This exception is thrown when the maximum number of connection requests have been exceeded for a 
            specific time for the MyMemory Translation service.
            """
            print(colorized_text(255, 0, 0, 'There has been too many connection requests to the MyMemory '
                                            'Translation service.'))
            logger.error('Connection Request Error:')
            logger.error('There has been too many connection requests to the MyMemory Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except RequestException as error:
            """
            This exception is thrown when an ambiguous exception occurs during a connection to the 
            MyMemory Translation service.
            """
            print(colorized_text(255, 0, 0, 'An ambiguous connection exception has occurred when contacting the'
                                            'MyMemory Translation service.  Please check the WordHoard log file '
                                            'for additional information.'))
            logger.error('Connection Exception:')
            logger.error('An ambiguous connection exception has occurred when communicating with the '
                         'MyMemory Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _mymemory_translate_reverse(self) -> Union[str, None]:
        """
        This function is used to translate a word from it source language, such as Spanish into American English.

        :return: translated word
        :rtype: string or None
        """
        try:
            if validate_address(self._email_address) is False:
                print(colorized_text(255, 0, 0,
                                     'A valid email address is required to use the MyMemory Translation '
                                     'service.'))
                sys.exit(1)
            elif validate_address(self._email_address) is True:
                response = self._requests_retry_session().get(self._url_to_query,
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
                elif response.status_code != 200:
                    raise RequestException()
                else:
                    data = response.json()
                    if not data:
                        print(colorized_text(255, 0, 0, f'MyMemory could not translate the word '
                                                        f'{self._str_to_translate}.'))
                        return None

                    else:
                        translation = data.get('responseData').get('translatedText')
                        if translation == 'INVALID EMAIL PROVIDED':
                            raise InvalidEmailAddressException()
                        elif translation:
                            return str(translation).lower().rstrip(punctuation)

        except InvalidEmailAddressException as error:
            """
            This exception is thrown when the email address provided for authentication to the MyMemory Translation 
            service is invalid. 
            
            Please note that the MyMemory Translation service only validates the format of the email address and 
            not the validity of the address provided.
            """
            print(colorized_text(255, 0, 0, 'The email address provided for authentication to the MyMemory '
                                            'Translation is invalid.'))
            logger.error('Invalid Email Address Error:')
            logger.error('The email address provided for authentication to the MyMemory Translation '
                         'is invalid.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            sys.exit(1)

        except InvalidLengthException as error:
            """
            This exception is thrown if the provided text exceed the length limit of the MyMemory Translator service.
            """
            print(colorized_text(255, 0, 0, f'The text length for the word: {self._str_to_translate} '
                                            f'exceed the length limit of MyMemory translation service.'))
            logger.error(f'The text length for the word: {self._str_to_translate} exceed the length limit of '
                         f'MyMemory translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except TooManyRequestsException as error:
            """
            This exception is thrown when the maximum number of connection requests have been exceeded for a 
            specific time for the MyMemory Translation service.
            """
            print(colorized_text(255, 0, 0, 'There has been too many connection requests to the MyMemory '
                                            'Translation service.'))
            logger.error('Connection Request Error:')
            logger.error('There has been too many connection requests to the MyMemory Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except RequestException as error:
            """
            This exception is thrown when an ambiguous exception occurs during a connection to the 
            MyMemory Translation service.
            """
            print(colorized_text(255, 0, 0, 'An ambiguous connection exception has occurred when contacting the'
                                            'MyMemory Translation service.  Please check the WordHoard log file '
                                            'for additional information.'))
            logger.error('Connection Exception:')
            logger.error('An ambiguous connection exception has occurred when communicating with the '
                         'MyMemory Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

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
            print(colorized_text(255, 0, 0, f'The language provided is not one of the supported languages '
                                            f'for the MyMemory Translation service.'))
            print(colorized_text(255, 0, 0, f'Requested language: {self._source_language}'))
            print(colorized_text(255, 0, 0, f'Please review the languages supported by the MyMemory Translate service\n'
                                            f'https://wordhoard.readthedocs.io/en/latest/translations/mymemory_supported_translation_languages/'))

            return None

    def reverse_translate(self) -> Union[str, None]:
        """
        This function is used to translate a word from American English into another language, such as Spanish.

        :return: translated word
        :rtype: string or None
        """
        return self._mymemory_translate_reverse()
