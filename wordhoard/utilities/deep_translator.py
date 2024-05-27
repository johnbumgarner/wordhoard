#!/usr/bin/env python3

"""
This Python module is used to translate a specific word from it source language,
such as Spanish into American English using the Deep Translation service.
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
# Date Last Revised: May 12, 2024
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
# Standard library imports
import ast
import logging
import traceback
from typing import Union

# Third-party imports
import deepl
from backoff import on_exception, expo
from ratelimit import limits, RateLimitException
from deepl.exceptions import AuthorizationException
from deepl.exceptions import QuotaExceededException
from deepl.exceptions import TooManyRequestsException

# Local or project-specific imports
from wordhoard.utilities.colorized_text import colorized_text
from wordhoard.utilities.translator_languages import Languages
from wordhoard.utilities.exceptions import LanguageNotSupportedException

logger = logging.getLogger(__name__)


class Translator:
    """
        This class handles translation operations using the DeepL translation service. It supports translating words
        from one language to another, handling rate limits, and dealing with various exceptions that may occur during
        translation requests.

        Args:
            source_language (str): The source language for translation. Defaults to an empty string.
            str_to_translate (str): The text to translate. Defaults to an empty string.
            api_key (str): The API key for accessing the DeepL translation service. Defaults to an empty string.

        Attributes:
            _source_language (str): The source language for translation.
            _str_to_translate (str): The text to translate.
            _api_key (str): The API key for accessing the DeepL translation service.
            _rate_limit_status (bool): A flag indicating the rate limit status for translation requests.

        Methods:
            __init__: Initializes the Translator object with source language, text to translate, and API key.
            _backoff_handler: Handles rate limit exceeded situations by logging and setting rate_limit_status.
            _deep_supported_languages: Checks if the source language is supported by DeepL translation service.
            _handle_standard_exceptions: Handles standard exceptions like TypeError and ValueError during translation.
            _handle_custom_exceptions: Handles custom exceptions specific to DeepL translation service.
            _deep_translate: Translates text from the source language to American English using DeepL service.
            _deep_translate_reverse: Translates text from American English to the source language using DeepL service.
            translate_word: Translates text from the source language to American English, handling unsupported languages.
            reverse_translate: Translates text from American English to the source language.

        Note:
            This class relies on the `deepl` module for translation functionality. Ensure that the module is installed
            and configured correctly for translation operations.
        """
    def __init__(self,
                 source_language: str = '',
                 str_to_translate: str = '',
                 max_number_of_requests: int = 30,
                 rate_limit_timeout_period: int = 60,
                 api_key: str = ''
                 ):

        self._source_language = source_language
        self._str_to_translate = str_to_translate
        self._api_key = api_key

        ratelimit_status = False
        self._rate_limit_status = ratelimit_status

        # Retries the requests after a certain time period has elapsed
        handler = on_exception(wait_gen=expo,
                               exception=RateLimitException,
                               max_time=60,
                               on_backoff=self._backoff_handler)
        # Establishes a rate limit for making requests to the Deep translation service
        limiter = limits(calls=max_number_of_requests, period=rate_limit_timeout_period)
        self.translate_word = handler(limiter(self.translate_word))
        self.reverse_translate = handler(limiter(self.reverse_translate))

    def _backoff_handler(self, details) -> None:
        """
        Handles the backoff mechanism when the rate limit for querying the Deep translation service is reached.

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
            colorized_text(text='The Deep translation service query rate limit was reached. '
                                'The querying process is entering a temporary hibernation mode.', color='red')
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')
            logger.info('The Deep translation service query rate limit was reached.')
            self._rate_limit_status = True
        elif self._rate_limit_status is True:
            colorized_text(text=f"Backing off {details['wait']:.1f} seconds afters {details['tries']} tries.",
                           color='blue')

    def _deep_supported_languages(self) -> Union[str, None]:
        """
        This function determines if the requested source language is
        one of the supported languages for the Deep translation service.

        :return: language
        :rtype: string
        """
        languages = Languages()
        deep_languages = languages.deep_supported_languages()
        deep_languages_str = str(deep_languages)
        supported_languages = ast.literal_eval(deep_languages_str)
        try:
            if self._source_language in supported_languages.keys():
                return self._source_language
            elif self._source_language in supported_languages.values():
                return self._source_language
            else:
                return None
        except LanguageNotSupportedException as error:
            logger.info('The language provided is not one of the supported languages for the Deep Translation service.')
            logger.info(f'Requested language: {self._source_language}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _handle_standard_exceptions(self, error):
        """
            Helper method to handle standard exceptions
        """
        if isinstance(error, TypeError):
            logger.error(f'A TypeError occurred when attempting to translate the word {self._str_to_translate}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        elif isinstance(error, ValueError):
            if str(error) == "auth_key must not be empty":
                colorized_text(text='An Authorization failure has occurred when using the Deep translation service.  '
                                    'Please verify your authentication key', color='red')
                logger.error('An Authorization key cannot be empty when using the Deep translation service.')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))
            elif str(error) == 'text must not be empty':
                colorized_text(text='An empty string was passed to the Deep translation service.', color='red')
                logger.error('An empty string was passed to the Deep translation service.')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))
            else:
                logger.error(f'An unknown ValueError occurred when attempting to translate the word'
                             f' {self._str_to_translate}')
                logger.error(''.join(traceback.format_tb(error.__traceback__)))

    @staticmethod
    def _handle_custom_exceptions(error):
        """
        Helper method to handle custom exceptions
        """
        if isinstance(error, AuthorizationException):
            colorized_text(text='The authentication key used for Deep Translation service is invalid.\nPlease verify '
                                'that the authentication key used is valid.', color='red')
            logger.error('Authorization Error:')
            logger.error('An authorization error has occurred when using the Deep Translation service.')
            logger.error('Please verify that the authentication key used is valid.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        elif isinstance(error, QuotaExceededException):
            colorized_text(text='The quota for the Deep Translation service for this billing period has '
                                'been exceeded.', color='red')
            logger.error('The quota for the the Deep Translation service for this billing period has been exceeded.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
        elif isinstance(error, TooManyRequestsException):
            colorized_text(text='There has been too many connection requests to the Deep Translation service.',
                           color='red')
            logger.error('Connection Request Error:')
            logger.error('There has been too many connection requests to the Deep Translation service.')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))

    def _deep_translate(self, original_language: str) -> str:
        """
        This function is used to translate a word from it source language, such as Spanish
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
        except (AuthorizationException, QuotaExceededException, TooManyRequestsException) as error:
            self._handle_custom_exceptions(error)
        except (TypeError, ValueError) as error:
            self._handle_standard_exceptions(error)

    def _deep_translate_reverse(self) -> str:
        """
        This function is used to translate a word from it source language, such as Spanish into American English.

        :return: translated word
        :rtype: string
        """
        try:
            translator = deepl.Translator(auth_key=self._api_key)
            result = translator.translate_text(text=self._str_to_translate,
                                               target_lang=self._source_language,
                                               source_lang='EN')
            translated_text = result.text
            return translated_text

        except (AuthorizationException, QuotaExceededException, TooManyRequestsException) as error:
            self._handle_custom_exceptions(error)
        except (TypeError, ValueError) as error:
            self._handle_standard_exceptions(error)

    def translate_word(self) -> Union[str, None]:
        """
        This function is used to translate a word from it source language, such as Spanish into American English.

        :return: translated word
        :rtype: string
        """
        supported_language = self._deep_supported_languages()
        if supported_language:
            return self._deep_translate(supported_language)
        elif not supported_language:
            colorized_text(text='The language provided is not one of the supported languages for the Deep Translation service.',
                           color='red')
            colorized_text(text=f'Requested language: {self._source_language}', color='red')
            colorized_text(text='Please review the languages supported by the Deep Translate service\n'
                           'https://wordhoard.readthedocs.io/en/latest/translations'
                           '/deepl_supported_translation_languages/', color='green')
            return None

    def reverse_translate(self) -> str:
        """
        This function is used to translate a word from American English into another language, such as Spanish.

        :return: translated word
        :rtype: string
        """
        return self._deep_translate_reverse()
