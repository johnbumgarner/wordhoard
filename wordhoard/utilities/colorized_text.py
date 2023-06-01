#!/usr/bin/env python3

"""
This Python script provide colorized text in the error messages thrown by WordHoard.
"""
__author__ = 'John Bumgarner'
__date__ = 'May 28, 2023'
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
# Date Completed: May 28, 2023
# Author: John Bumgarner
#
# Date Last Revised:
# Revised by:
##################################################################################

def colorized_text(text: str, color: str) -> None:
    """
    This function provides terminal error messages in color.
    :param text: text to colorized
    :param color: color value
    :return: print error in color
    """
    RESET = "\033[0m" # resets the terminal color to its default
    if color == 'red':
        print(f'\033[1;31m{text}{RESET}')
    elif color == 'blue':
        print(f'\033[1;34m{text}{RESET}')
    elif color == 'green':
        print(f'\033[1;32m{text}{RESET}')
    elif color == 'magenta':
        print(f'\033[1;35m{text}{RESET}')


