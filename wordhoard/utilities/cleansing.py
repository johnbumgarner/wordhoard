#!/usr/bin/env python3

"""
This Python script is used to clean and flatten query result lists.
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


def normalize_space(list_of_words):
    """
    This function is designed to remove all leading and
    trailing whitespace surrounding words contained in
    a list.
    :param list_of_words: list of words
    :return: list of words
    """
    return ' '.join(list_of_words.split()).lower()


def flatten_multidimensional_list(list_of_lists):
    """
    This function is used to flatten a multidimensional list into
    a single list.

    :return: a multidimensional list that has been flattened
    :rtype: list
    """
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten_multidimensional_list(list_of_lists[0]) + flatten_multidimensional_list(list_of_lists[1:])
    return list_of_lists[:1] + flatten_multidimensional_list(list_of_lists[1:])
