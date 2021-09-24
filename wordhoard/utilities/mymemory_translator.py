#!/usr/bin/env python3

"""
This Python script is used to translate a specific word from it source language,
such as Spanish into American English using the MyMemory translation service.
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
#
# Date Completed: September 24, 2021
# Author: John Bumgarner
#
# Date Last Revised:
# Revised by:
#
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import sys
import logging
import requests
import traceback
from string import punctuation
from backoff import on_exception, expo
from requests.adapters import HTTPAdapter
from ratelimit import limits, RateLimitException
from requests.packages.urllib3.util.retry import Retry
from wordhoard.utilities.exceptions import RequestError
from wordhoard.utilities.exceptions import NotValidLength
from wordhoard.utilities.exceptions import TooManyRequests
from wordhoard.utilities.user_agents import get_random_user_agent
from wordhoard.utilities.exceptions import LanguageNotSupportedException

logger = logging.getLogger(__name__)

rand_user_agent = get_random_user_agent()
http_headers = {'user-agent': rand_user_agent}


class Translator(object):

    def __init__(self,
                 source_language='',
                 str_to_translate='',
                 email_address=None
                 ):

        self._source_language = source_language
        self._str_to_translate = str_to_translate
        self._url_to_query = 'http://api.mymemory.translated.net/get'
        self._email_address = email_address
        self._headers = http_headers

        ratelimit_status = False
        self._rate_limit_status = ratelimit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(expo, RateLimitException, max_time=60, on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the MyMemory translation service
        limiter = limits(calls=30, period=60)
        self.translate_word = handler(limiter(self.translate_word))
        self.reverse_translate = handler(limiter(self.reverse_translate))

    def _colorized_text(self, r, g, b, text):
        return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"

    def _backoff_handler(self, details):
        if self._rate_limit_status is False:
            print(self._colorized_text(255, 0, 0,
                                       'The MyMemory translation service query rate Limit was reached. The querying '
                                       'process is entering a temporary hibernation mode.'))
            logger.info('The MyMemory translation service query rate limit was reached.')
            self._rate_limit_status = True

    def _mymemory_supported_languages(self):
        """
        This function determines if the requested source language is
        one supported languages for the MyMemory Translator.

        :return: language
        :rtype: string
        """
        # MyMemory Translator supported languages as of 09-03-2021
        supported_languages = {'af': 'afrikaans',
                               'sq': 'albanian',
                               'am': 'amharic',
                               'ar': 'arabic',
                               'hy': 'armenian',
                               'az': 'azerbaijani',
                               'eu': 'basque',
                               'be': 'belarusian',
                               'bn': 'bengali',
                               'bs': 'bosnian',
                               'bg': 'bulgarian',
                               'ca': 'catalan',
                               'ceb': 'cebuano',
                               'ny': 'chichewa',
                               'zh-CN': 'chinese (simplified)',
                               'zh-TW': 'chinese (traditional)',
                               'co': 'corsican',
                               'hr': 'croatian',
                               'cs': 'czech',
                               'da': 'danish',
                               'nl': 'dutch',
                               'en': 'english',
                               'eo': 'esperanto',
                               'et': 'estonian',
                               'tl': 'filipino',
                               'fi': 'finnish',
                               'fr': 'french',
                               'fy': 'frisian',
                               'gl': 'galician',
                               'ka': 'georgian',
                               'de': 'german',
                               'el': 'greek',
                               'gu': 'gujarati',
                               'ht': 'haitian creole',
                               'ha': 'hausa',
                               'haw': 'hawaiian',
                               'iw': 'hebrew',
                               'hi': 'hindi',
                               'hmn': 'hmong',
                               'hu': 'hungarian',
                               'is': 'icelandic',
                               'ig': 'igbo',
                               'id': 'indonesian',
                               'ga': 'irish',
                               'it': 'italian',
                               'ja': 'japanese',
                               'jw': 'javanese',
                               'kn': 'kannada',
                               'kk': 'kazakh',
                               'km': 'khmer',
                               'rw': 'kinyarwanda',
                               'ko': 'korean',
                               'ku': 'kurdish',
                               'ky': 'kyrgyz',
                               'lo': 'lao',
                               'la': 'latin',
                               'lv': 'latvian',
                               'lt': 'lithuanian',
                               'lb': 'luxembourgish',
                               'mk': 'macedonian',
                               'mg': 'malagasy',
                               'ms': 'malay',
                               'ml': 'malayalam',
                               'mt': 'maltese',
                               'mi': 'maori',
                               'mr': 'marathi',
                               'mn': 'mongolian',
                               'my': 'myanmar',
                               'ne': 'nepali',
                               'no': 'norwegian',
                               'or': 'odia',
                               'ps': 'pashto',
                               'fa': 'persian',
                               'pl': 'polish',
                               'pt': 'portuguese',
                               'pa': 'punjabi',
                               'ro': 'romanian',
                               'ru': 'russian',
                               'sm': 'samoan',
                               'gd': 'scots gaelic',
                               'sr': 'serbian',
                               'st': 'sesotho',
                               'sn': 'shona',
                               'sd': 'sindhi',
                               'si': 'sinhala',
                               'sk': 'slovak',
                               'sl': 'slovenian',
                               'so': 'somali',
                               'es': 'spanish',
                               'su': 'sundanese',
                               'sw': 'swahili',
                               'sv': 'swedish',
                               'tg': 'tajik',
                               'ta': 'tamil',
                               'tt': 'tatar',
                               'te': 'telugu',
                               'th': 'thai',
                               'tr': 'turkish',
                               'tk': 'turkmen',
                               'uk': 'ukrainian',
                               'ur': 'urdu',
                               'ug': 'uyghur',
                               'uz': 'uzbek',
                               'vi': 'vietnamese',
                               'cy': 'welsh',
                               'xh': 'xhosa',
                               'yi': 'yiddish',
                               'yo': 'yoruba',
                               'zu': 'zulu'}
        try:
            if self._source_language in supported_languages.keys():
                return self._source_language
            elif self._source_language in supported_languages.values():
                return self._source_language
            else:
                return None
        except LanguageNotSupportedException as error:
            """
            An exception is thrown if the user uses a language that is not supported by the translator
            """
            logger.info(f'The language provided is not one of the supported languages of the MyMemory '
                        f'translation service.')
            logger.info(f'Requested language: {self._source_language}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    # reference: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    @staticmethod
    def _requests_retry_session(retries=5,
                                backoff_factor=0.5,
                                status_forcelist=(500, 502, 504),
                                session=None,
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

    def _mymemory_translate(self, original_language):
        """
        This function is used to translated a word from it source language, such as Spanish
        into American English.

        :param original_language: language to translated from
        :return: translated word
        :rtype: string
        """
        try:
            if self._email_address is None:
                print(self._colorized_text(255, 0, 0,
                                           'A valid email address is required to use the MyMemory translation '
                                           'service.'))
                sys.exit(1)
            else:
                response = self._requests_retry_session().get(self._url_to_query,
                                                              params={'langpair': f'{original_language}|en-us',
                                                                      'q': self._str_to_translate,
                                                                      'de': self._email_address},
                                                              headers=self._headers)

                if response.status_code == 429:
                    raise TooManyRequests()
                elif response.status_code != 200:
                    raise RequestError()
                else:
                    data = response.json()
                    if not data:
                        return f'MyMemory could not translate the word {self._str_to_translate}.'

                    translation = data.get('responseData').get('translatedText')
                    if translation:
                        return str(translation).lower().rstrip(punctuation)

        except NotValidLength as error:
            """
            The exception is thrown if the provided text exceed the length limit of the translator
            """
            logger.error(f'The text length for the word: {self._str_to_translate} exceed the length limit of '
                         f'the MyMemory translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except TooManyRequests as error:
            """
            The exception is thrown if an error occurred during the request call, e.g a connection problem.
            """
            logger.error('Server Error: There has been too many requests to the server.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _mymemory_translate_reverse(self, return_all=False):
        """
        This function is used to translated a word from it source language, such as Spanish
        into American English.

        :return: translated word
        :rtype: string
        """
        try:
            if self._email_address is None:
                print(self._colorized_text(255, 0, 0,
                                           'A valid email address is required to use the MyMemory translation '
                                           'service.'))
                sys.exit(1)
            else:
                response = self._requests_retry_session().get(self._url_to_query,
                                                              params={'langpair': f'en-us|{self._source_language}',
                                                                      'q': self._str_to_translate,
                                                                      'de': self._email_address},
                                                              headers=self._headers)

                if response.status_code == 429:
                    raise TooManyRequests()
                elif response.status_code != 200:
                    raise RequestError()
                else:
                    data = response.json()
                    if not data:
                        return f'MyMemory could not translate the word {self._str_to_translate}.'

                    translation = data.get('responseData').get('translatedText')

                    if translation:
                        return str(translation).lower().strip(punctuation)

        except NotValidLength as error:
            """
            The exception is thrown if the provided text exceed the length limit of the translator
            """
            logger.error(f'The text length for the word: {self._str_to_translate} exceed the length limit of '
                         f'the MyMemory translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        except TooManyRequests as error:
            """
            The exception is thrown if an error occurred during the request call, e.g a connection problem.
            """
            logger.error('Server Error: There has been too many requests to the server.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def translate_word(self):
        """
        This function is used to translated a word from it source language, such as Spanish
        into American English.

        :return: translated word
        :rtype: string
        """
        supported_language = self._mymemory_supported_languages()
        if supported_language:
            return self._mymemory_translate(supported_language)
        elif not supported_language:
            logger.info(f'The language provided is not one of the supported languages for the MyMemory '
                        f'translation service.')
            logger.info(f'Requested language: {self._source_language}')
            return None

    def reverse_translate(self):
        """
        This function is used to translated a word from American English into
        another language, such as Spanish.

        :return: translated word
        :rtype: string
        """
        return self._mymemory_translate_reverse()
