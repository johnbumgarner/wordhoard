#!/usr/bin/env python3

"""
This Python script is used to translate a specific word from it source language,
such as Spanish into American English using the Deep translation service.
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
import deepl
import logging
import traceback
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException
from deepl.exceptions import QuotaExceededException
from deepl.exceptions import TooManyRequestsException
from wordhoard.utilities.exceptions import LanguageNotSupportedException

logger = logging.getLogger(__name__)


class Translator(object):

    def __init__(self,
                 source_language='',
                 str_to_translate='',
                 api_key=''
                 ):

        self._source_language = source_language
        self._str_to_translate = str_to_translate
        self._api_key = api_key

        ratelimit_status = False
        self._rate_limit_status = ratelimit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(expo, RateLimitException, max_time=60, on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the Deep translation service
        limiter = limits(calls=60, period=60)
        self.translate_word = handler(limiter(self.translate_word))
        self.reverse_translate = handler(limiter(self.reverse_translate))

    def _colorized_text(self, r, g, b, text):
        return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"

    def _backoff_handler(self, details):
        if self._rate_limit_status is False:
            print(self._colorized_text(255, 0, 0,
                                       'The Deep translation service query rate Limit was reached. The querying '
                                       'process is entering a temporary hibernation mode.'))
            logger.info('The Deep translation service query rate limit was reached.')
            self._rate_limit_status = True

    def _deep_supported_languages(self):
        """
        This function determines if the requested source language is
        one of the supported languages for the Deep translation service.

        :return: language
        :rtype: string
        """
        # Deep Translator supported languages listed in as of 09-22-2021
        supported_languages = {'bg': 'bulgarian',
                               'zh': 'chinese',
                               'cs': 'czech',
                               'da': 'danish',
                               'nl': 'dutch',
                               'en': 'english',
                               'et': 'estonian',
                               'fi': 'finnish',
                               'fr': 'french',
                               'de': 'german',
                               'el': 'greek',
                               'hu': 'hungarian',
                               'it': 'italian',
                               'ja': 'japanese',
                               'lo': 'laotian',
                               'lv': 'latvian',
                               'mt': 'maltese',
                               'pl': 'polish',
                               'pt': 'portuguese',
                               'ro': 'romanian',
                               'ru': 'russian',
                               'sk': 'slovakian',
                               'sl': 'slovenian',
                               'es': 'spanish',
                               'sv': 'swedish'}
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
            logger.info(f'The language provided is not one of the supported languages for the Deep translation service')
            logger.info(f'Requested language: {self._source_language}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _deep_translate(self, original_language):
        """
        This function is used to translated a word from it source language, such as Spanish
        into American English.

        :param original_language: language to translated from
        :return: translated word
        :rtype: string
        """
        try:
            translator = deepl.Translator(auth_key=self._api_key)
            result = translator.translate_text(self._str_to_translate,
                                               target_lang='EN-US',
                                               source_lang=original_language)
            translated_text = result.text
            return translated_text

        except QuotaExceededException as error:
            """
            The exception is thrown when the Quota for this billing period has been exceeded.
            """
            print(self._colorized_text(255, 0, 0, 'The quota for the the Deep translation service for this billing '
                                                  'period has been exceeded.'))
            logger.error('The quota for the the Deep translation service for this billing period has been exceeded.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except TooManyRequestsException as error:
            """
            The exception is thrown if an error occurred during the request call, e.g a connection problem.
            """
            logger.error('Server Error: There has been too many requests to the server.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except TypeError as error:
            """
            The exception is thrown when an operation or function is applied to an object of inappropriate type.
            """
            logger.error(f'A TypeError occurred when attempting to translate the word {self._str_to_translate}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except ValueError as error:
            """
            The exception is thrown when an operation or function receives an argument that 
            has the right type but an inappropriate value.
            """
            if str(error) == "auth_key must not be empty":
                print(self._colorized_text(255, 0, 0, 'An Authorization failure has occurred when using the Deep '
                                                      'translation service.  Please verify your authentication key'))
                logger.error('An Authorization key cannot be empty when using the Deep translation service.')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))
            elif str(error) == 'text must not be empty':
                print(self._colorized_text(255, 0, 0, 'An empty string was passed to the Deep translation service.'))
                logger.error('An empty string was passed to the Deep translation service.')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))
            else:
                logger.error(f'An unknown ValueError occurred when attempting to translate the word'
                             f' {self._str_to_translate}')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _deep_translate_reverse(self):
        """
        This function is used to translated a word from it source language, such as Spanish
        into American English.

        :return: translated word
        :rtype: string
        """
        try:
            translator = deepl.Translator(auth_key=self._api_key)
            result = translator.translate_text(self._str_to_translate,
                                               target_lang=self._source_language,
                                               source_lang='EN')
            translated_text = result.text
            return translated_text

        except QuotaExceededException as error:
            """
            The exception is thrown when the Quota for this billing period has been exceeded.
            """
            print(self._colorized_text(255, 0, 0, 'The quota for the the Deep translation service for this billing '
                                                  'period has been exceeded.'))
            logger.error('The quota for the the Deep translation service for this billing period has been exceeded.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except TooManyRequestsException as error:
            """
            The exception is thrown if an error occurred during the request call, e.g a connection problem.
            """
            logger.error('Server Error: There has been too many requests to the server.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except TypeError as error:
            """
            The exception is thrown when an operation or function is applied to an object of inappropriate type.
            """
            logger.error(f'A TypeError occurred when attempting to translate the word {self._str_to_translate}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

        except ValueError as error:
            """
            The exception is thrown when an operation or function receives an argument that 
            has the right type but an inappropriate value.
            """
            if str(error) == "auth_key must not be empty":
                print(self._colorized_text(255, 0, 0, 'An Authorization failure has occurred when using the Deep '
                                                      'translation service.  Please verify your authentication key'))
                logger.error('An Authorization key cannot be empty when using the Deep translation service.')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))
            elif str(error) == 'text must not be empty':
                print(self._colorized_text(255, 0, 0, 'An empty string was passed to the Deep translation service.'))
                logger.error('An empty string was passed to the Deep translation service.')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))
            else:
                logger.error(f'An unknown ValueError occurred when attempting to translate the word'
                             f' {self._str_to_translate}')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def translate_word(self):
        """
        This function is used to translated a word from it source language, such as Spanish
        into American English.

        :return: translated word
        :rtype: string
        """
        supported_language = self._deep_supported_languages()
        if supported_language:
            return self._deep_translate(supported_language)
        elif not supported_language:
            print(self._colorized_text(255, 0, 0, f'The language provided is not one of the supported languages '
                                                  f'for the Deep translation service'))
            logger.info(f'The language provided is not one of the supported languages for the Deep translation '
                        f'service.')
            logger.info(f'Requested language: {self._source_language}')
            return None

    def reverse_translate(self):
        """
        This function is used to translated a word from American English into
        another language, such as Spanish.

        :return: translated word
        :rtype: string
        """
        return self._deep_translate_reverse()
