#!/usr/bin/env python3

"""
This Python script is used to validate the format of an email address.
"""
__author__ = 'John Bumgarner'
__date__ = 'February 09, 2023'
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
# Date Completed: February 09, 2023
# Author: John Bumgarner
#
# Date Last Revised: February 19, 2023
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import re as regex

def validate_address(email_address: str) -> bool:
    """
    This function is designed to validate the format of email address provided by
    an end user.

    :param email_address: input string
    :return: boolean
    """
    if regex.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email_address):
        return True
    else:
        return False
