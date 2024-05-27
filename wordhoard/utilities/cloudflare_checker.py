#!/usr/bin/env python3

"""
This Python script is used to verify that the webpage being queried is
either protected or not protected by Cloudflare's DDoS mitigation services.
"""
__author__ = 'John Bumgarner'
__date__ = 'January 07, 2022'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2022 John Bumgarner'

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
# Date Completed: January 08, 2022
# Author: John Bumgarner
#
# Date Revised: May 25, 2024
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
from bs4 import BeautifulSoup

class CloudflareVerification:
    """
    This Class is used to query a webpage to determine if it is protected by
    Cloudflare's DDoS mitigation services.
    """

    def __init__(self, url, soup):
        self._url: str = url
        self._raw_soup: BeautifulSoup = soup

    def _check_p_tag(self) -> bool:
        """
        This function is designed to query for the existence
        of specific tag known to be commonly related to a
        Cloudflare protected webpage.

        :return: True or False
        :rtype: boolean
        """
        p_tag = self._raw_soup.find(name='p', attrs={'data-translate': 'why_captcha_detail'})
        return bool(p_tag and p_tag.text == 'Completing the CAPTCHA proves you are a human and gives you temporary access to the web property.')

    def _check_div_tag(self) -> bool:
        """
        This function is designed to query for the existence
        of a specific div tag with the id 'challenge-body-text'.

        :return: True or False
        :rtype: boolean
        """
        return bool(self._raw_soup.find(name='div', attrs={'id': 'challenge-body-text'}))

    def _check_title_tag(self) -> bool:
        """
        This function is designed to query for the existence
        of specific Cloudflare related text contained in a title tag.

        :return: True or False
        :rtype: boolean
        """
        title_tag = self._raw_soup.find(name='title')
        return bool(
                title_tag and (
                    'Please Wait... | Cloudflare' in title_tag.text or
                    'Just a moment...' in title_tag.text or
                    'Attention Required! | Cloudflare' in title_tag.text)
                    )

    def _check_meta_tag(self) -> bool:
        """
        This function is designed to query for the existence
        of specific Cloudflare related meta tag.

        :return: True or False
        :rtype: boolean
        """
        return bool(self._raw_soup.find(name='meta', attrs={'id': 'captcha-bypass'}))

    def cloudflare_protected_url(self) -> bool:
        """
        This function is designed to query specific elements, which
        will determine if a webpage is protected by Cloudflare's
        DDoS mitigation services.

        :return: True or False
        :rtype: boolean
        """
        p_tag_bool = self._check_p_tag()
        div_tag_bool = self._check_div_tag()
        title_tag_bool = self._check_title_tag()
        meta_tag_bool = self._check_meta_tag()

        if p_tag_bool is True:
            return True
        elif div_tag_bool is True:
            return True
        elif title_tag_bool is True:
            return True
        elif meta_tag_bool is True:
            return True
        else:
            return False
