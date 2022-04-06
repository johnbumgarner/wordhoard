#!/usr/bin/env python3

"""
This Python script obtains a random user agent from a pre-built dictionary.
"""
__author__ = 'John Bumgarner'
__date__ = 'September 12, 2021'
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
#
# Date Completed: September 12, 2021
# Author: John Bumgarner
#
# Date Last Revised:
# Revised by:
#
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import os
import sys
import random
import pickle
import logging
import traceback

logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

######################################################################
# Array of common user agents to use for the HTTP connection
# source:  http://http://www.useragentstring.com
# source:  https://deviceatlas.com/blog/list-of-user-agent-strings
# source:  https://developers.whatismybrowser.com/useragents/explore
########################################################################
try:
    _common_user_agents = os.path.join(BASE_DIR, 'files/common_user_agents.pkl')
    with open(_common_user_agents, 'rb') as _infile:
        _user_agents_list = pickle.load(_infile)
        _infile.close()
except FileNotFoundError as error:
    logger.error('The common_user_agents.pkl file was not found. Aborting operation.')
    logger.error(''.join(traceback.format_tb(error.__traceback__)))
    sys.exit(1)
except OSError as error:
    logger.error(f"An OS error occurred when trying to open the file common_user_agents.pkl")
    logger.error(''.join(traceback.format_tb(error.__traceback__)))
    sys.exit(1)


def get_random_user_agent():
    """
    This function obtains a random user agent from a
    dictionary of available agents.

    :return: random user agent
    :rtype: string
    """
    global _user_agents_list
    random_key = random.choice(list(_user_agents_list.keys()))
    random_value = random.choice(list(_user_agents_list[random_key]))
    return random_value


def get_specific_user_agent(requested_key):
    """
    This function obtains a specific user agent type from a
    dictionary of available agents. The available agents types
    are listed below:

    - android
    - chrome macOS
    - chrome windows
    - firefox macOS
    - firefox windows
    - safari ipad
    - safari iphone
    - safari macOS

    :param requested_key:
    :return: random user agent
    :rtype: string
    """

    # available user agent types
    user_agent_keys = {'chrome macOS': 'chrome_mac_os_x', 'chrome windows': 'chrome_windows_10',
                       'firefox macOS': 'firefox_mac_os_x', 'firefox windows': 'firefox_windows_10',
                       'safari macOS': 'safari_mac_os_x', 'safari iphone': 'safari_iphone',
                       'safari ipad': 'safari_ipad', 'android': 'samsung_browser_android'}

    if bool([v for k, v in user_agent_keys.items() if k == requested_key]):
        key = ''.join([v for k, v in user_agent_keys.items() if k == requested_key])
        global _user_agents_list
        random_value = random.choice(list(_user_agents_list[key]))
        return random_value
    else:
        logger.error('The requested user agent was not found in the list of available agents.')
        logger.info(f'Agent requested: {requested_key}')
