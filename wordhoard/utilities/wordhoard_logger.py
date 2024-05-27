#!/usr/bin/env python3

"""
This Python script is used to enable logging within other script.
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
# Date Last Revised: September 4, 2021
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import logging

def enable_logging(logger) -> logging:
    """
    Enable logging for the specified logger.

    This function adds a file handler to the logger to write log messages to a file named 'wordhoard_error.yaml'.
    It also sets a specific logging format for the log messages.

    :param logger: The logger object to which logging will be enabled.
    :type logger: logging.Logger
    """
    log_name = 'wordhoard_error.yaml'
    log_handler = logging.FileHandler(f'{log_name}')
    logger.addHandler(log_handler)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
    log_handler.setFormatter(formatter)
