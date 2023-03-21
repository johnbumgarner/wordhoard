#!/usr/bin/env python3

"""
This Python script is used to bypass the Cloudflare's DDoS mitigation protection
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
# Date Revised:
# Revised by:
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import logging
import cloudscraper
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from cloudscraper.exceptions import CloudflareChallengeError

logger = logging.getLogger(__name__)


class Cloudflare(object):
    """
    This Class is used to bypass the Cloudflare's DDoS mitigation protection for a specific website.
    """
    def __init__(self, url):
        self._url: str = url

    def bypass(self) -> BeautifulSoup:
        """
        This function attempts to bypass the Cloudflare's DDoS mitigation protection
        for a specific website.

        :return: BeautifulSoup object
        """
        scraper = cloudscraper.create_scraper(delay=10,  browser={'custom': 'ScraperBot/1.0', })
        response = scraper.get(self._url)
        if response.status_code == 502 or response.status_code == 520 or response.status_code == 521:
            logger.info('-' * 80)
            logger.info(f'Cloudflare DDoS mitigation service protection bypass started.')
            logger.info(f'Requested URL: {self._url}')
            logger.info(f'Status Code: {response.status_code}')
            logger.info('-' * 80)
            scraper.close()
            sleep(randint(1, 5))
            Cloudflare(self._url).bypass()
        elif response.status_code == 200:
            try:
                soup = BeautifulSoup(response.content, 'lxml')
                logger.info('-' * 80)
                logger.info(f'Cloudflare DDoS mitigation service protection bypass successful.')
                logger.info(f'Requested URL: {self._url}')
                logger.info('-' * 80)
                scraper.close()
                return soup
            except CloudflareChallengeError:
                pass
