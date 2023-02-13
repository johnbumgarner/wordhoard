#!/usr/bin/env python3

"""
This Python script provides various Exceptions Classes, which are used in the WordHoard Translation modules.
"""
__author__ = 'John Bumgarner'
__date__ = 'February 04, 2023'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2023 John Bumgarner"

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
# Date Completed: February 04, 2023
# Author: John Bumgarner
#
# Date Last Revised:
# Revised by:
##################################################################################


class ElementNotFoundException(Exception):
    """
    The exception is thrown if the requested HTML element was not found in the body element being
    parsed by BeautifulSoup.
    """
    pass


class InvalidEmailAddressException(Exception):
    """
    This exception is thrown when the email address provided for authentication to the MyMemory Translation
    service is invalid.
    """
    pass


class InvalidLengthException(Exception):
    """
    This exception is thrown if the provided text exceed the length limit of the the Translator service being used.
    """
    pass


class LanguageNotSupportedException(Exception):
    """
    This exception is thrown when the requested langauge is not supported by the Translator service being used.
    """
    pass


class QuotaExceededException(Exception):
    """
    This exception is thrown when the translation quota for a specific time period for the Translator service
    being used has been exceeded.
    """
    pass


class TooManyRequestsException(Exception):
    """
    This exception is thrown when the maximum number of connection requests have been exceeded for a specific time
    period for the Translator service being used.
    """
    pass


class RequestException(Exception):
    """
    This exception is thrown when an ambiguous exception occurs during a connection to the Translator service
    being used.
    """
    pass
