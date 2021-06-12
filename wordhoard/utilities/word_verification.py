#!/usr/bin/env python3

"""
This Python script is to validate the syntax of words to query.
"""
__author__ = 'John Bumgarner'
__date__ = 'October 15, 2020'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2020 John Bumgarner"

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
# Date Completed: October 15, 2020
# Author: John Bumgarner
#
# Date Revised:
# Revised by:
#
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import re as regex


def validate_word_syntax(word):
    """
    This function is designed to validate that the syntax for
    a string variable is acceptable.

    A validate format is English words that only contain alpha
    characters and hyphens.

    :param word: string to validate
    :return: boolean true or false
    """
    if len(word) == 0:
        return False
    else:
        temp = regex.match(r'^[a-zA-Z-\s]*$', word.strip())
        if temp:
            return True
        else:
            return False
