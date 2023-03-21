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
# Date Completed: October 15, 2020
# Author: John Bumgarner
#
# Date Revised: March 04, 2023
# Revised by: John Bumgarner
##################################################################################
from typing import List, Union

def normalize_space(list_of_words: List) -> List:
    """
    This function is designed to remove all leading and
    trailing whitespace surrounding words contained in
    a list.

    :param list_of_words: list of words
    :return: list of words
    """
    normalize_list = [x.strip() for x in list_of_words]
    return normalize_list

def remove_excess_whitespace(input_string: str) -> str:
    """
    This function uses the join() and split() methods together to remove duplicate spaces
    and newline characters from a string.

    :param input_string:
    :return: str
    """
    return ' '.join(input_string.split())

def flatten_multidimensional_list(list_of_lists: Union[List[str], List[List[str]]]) -> List:
    """
    This function is used to flatten a multidimensional list into a single list.

    :return: a multidimensional list that has been flattened
    :rtype: list
    """
    if any(isinstance(i, List) for i in list_of_lists):
        flattened_list = [element for sub_list in list_of_lists for element in sub_list]
        return flattened_list
    else:
        return list_of_lists

