#!/usr/bin/env python3

"""
This Python script is used to verify the webpage being queried is either
protected or not protected by a captcha that requires human interaction to bypass.
"""
__author__ = 'John Bumgarner'
__date__ = 'December 07, 2021'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2021 John Bumgarner'

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
# Date Completed: December 07, 2021
# Author: John Bumgarner
#
# Date Revised: February 25, 2023
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import bs4
import logging

logger = logging.getLogger(__name__)


class CaptchaVerification(object):
    """
    This Class is used to query a webpage to determine if it is protected by a captcha.
    """

    def __init__(self, url, soup):
        self._url: str = url
        self._raw_soup: bs4.BeautifulSoup = soup

    def _check_div_tag(self) -> bool:
        """
        This function is designed to query for the existence
        of specific tag known to be commonly related to a
        captcha protected webpage.

        :return: True or False
        :rtype: boolean
        """
        captcha_protected_div_tag = bool(self._raw_soup.find(name='div', attrs={'id': 'px-captcha'}))
        if captcha_protected_div_tag is True:
            logger.error(f'The {self._url} has captcha protection.')
            return True
        elif captcha_protected_div_tag is False:
            return False

    def _check_title_tag(self)  -> bool:
        """
        This function is designed to query for the existence
        of specific captcha related text contained in a title tag.

        :return: True or False
        :rtype: boolean
        """
        title_tag = self._raw_soup.find(name='title')
        if 'Are you a robot?' in title_tag.text:
            logger.error(f'The {self._url} has captcha protection.')
            return True
        else:
            return False

    def _check_h2_tag(self) -> bool:
        """
        This function is designed to query for the existence
        of specific captcha related text contained in an H2 tag.

        :return: True or False
        :rtype: boolean
        """
        captcha_protected_h2_tag = bool(self._raw_soup.find(name='h2', attrs={'class': 'main__heading'}))
        if captcha_protected_h2_tag is True:
            captcha_protected_tag = self._raw_soup.find(name='h2', attrs={'class': 'main__heading'})
            if "We've detected unusual activity from your computer network" in captcha_protected_tag.text:
                return True
            else:
                return False

    def captcha_protected_url(self)  -> bool:
        """
        This function is designed to query specific elements, which
        will determine if a webpage is protected by a captcha.

        :return: True or False
        :rtype: boolean
        """
        div_tag_bool = self._check_div_tag()
        if div_tag_bool is True:
            return True
        elif div_tag_bool is False:
            title_tag_bool = self._check_title_tag()
            if title_tag_bool is True:
                return True
            else:
                h2_tag_bool = self._check_h2_tag()
                if h2_tag_bool is True:
                    return True
                else:
                    return False
