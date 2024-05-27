#!/usr/bin/env python3

"""
This Python module is used to bypass the Cloudflare's DDoS mitigation protection
for the website provided.
"""
__author__ = 'John Bumgarner'
__date__ = 'February 25, 2023'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2023 John Bumgarner'

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
# Date Completed: February 25, 2023
# Author: John Bumgarner
#
# Date Revised: May 04, 2024
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
# Standard library imports
import logging
from time import sleep
from typing import Union
from random import randint

# Third-party imports
import cloudscraper
from bs4 import BeautifulSoup
from cloudscraper.exceptions import CloudflareChallengeError

logger = logging.getLogger(__name__)

SCRAPE_COUNT = 0

class Cloudflare:
    """
    This Class is used to bypass the Cloudflare's DDoS mitigation protection for a specific website.
    """
    def __init__(self, url):
        self._url: str = url

    def bypass(self) -> Union[BeautifulSoup, None]:
        """
        This function attempts to bypass the Cloudflare's DDoS mitigation protection for a specific website.

        :return: BeautifulSoup object
        """
        global SCRAPE_COUNT
        SCRAPE_COUNT += 1
        scraper = cloudscraper.create_scraper(delay=20, browser={'browser': 'chrome',
                                                                 'platform': 'ios',
                                                                 'mobile': True})
        response = scraper.get(self._url)
        if response.status_code == 403:
            if SCRAPE_COUNT != 10:
                logger.info("The requested URL is protected by Cloudflare's DDoS mitigation service.")
                logger.info(f'Requested URL: {self._url}')
                logger.info(f'Status Code: {response.status_code}')
                sleep(randint(1, 10))
                Cloudflare(self._url).bypass()
            else:
                return None
        elif response.status_code in (502, 520, 521):
            logger.info('-' * 80)
            logger.info('Cloudflare DDoS mitigation service protection bypass started.')
            logger.info(f'Requested URL: {self._url}')
            logger.info(f'Status Code: {response.status_code}')
            logger.info('-' * 80)
            scraper.close()
            sleep(randint(1, 10))
            Cloudflare(self._url).bypass()
        elif response.status_code == 200:
            try:
                logger.info('-' * 80)
                logger.info('Cloudflare DDoS mitigation service protection bypass successful.')
                logger.info(f'Requested URL: {self._url}')
                logger.info('-' * 80)
                soup = BeautifulSoup(response.content, 'lxml')
                if isinstance(soup, BeautifulSoup):
                    scraper.close()
                    return soup
                elif not isinstance(soup, BeautifulSoup):
                    return None
            except CloudflareChallengeError:
                pass
