#!/usr/bin/env python3

"""
This Python script provide colorized text in the error messages thrown by WordHoard.
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


def colorized_text(r: int, g: int, b: int, text: str) -> str:
    """
    This function provides error messages color.
    For example:
    rgb(255, 0, 0) is displayed as the color red
    rgb(0, 255, 0) is displayed as the color green
    :param r: red color value
    :param g: green color value
    :param b: below color value
    :param text: text to colorized
    :return: string of colorized text
    """
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
