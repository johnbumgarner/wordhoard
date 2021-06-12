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
import logging


def enable_logging(logger):
    console = logging.StreamHandler()
    logger.addHandler(console)
    console.setLevel(logging.INFO)

    log_name = 'wordhoard_error.yaml'
    log_handler = logging.FileHandler(f'{log_name}')
    logger.addHandler(log_handler)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
    log_handler.setFormatter(formatter)
    log_handler.setLevel(logging.ERROR)







