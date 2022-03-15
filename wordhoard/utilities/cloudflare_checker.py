#!/usr/bin/env python3

"""
This Python script is used to verify the HREF being queried is
protected by Cloudflare's DDoS mitigation services.
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
# Date Revised:
# Revised by:
##################################################################################


class CloudflareVerification(object):
    """
    This Class is used to query a webpage to determine if it is protected by
    Cloudflare's DDoS mitigation services.
    """

    def __init__(self, url, soup):
        self._url = url
        self._raw_soup = soup

    def _check_p_tag(self):
        """
        This function is designed to query for the existence
        of specific tag known to be commonly related to a
        Cloudflare protected webpage.

        :return: True or False
        :rtype: boolean
        """
        if self._raw_soup.find(name='p', attrs={'data-translate': 'why_captcha_detail'}):
            p_tag = self._raw_soup.find(name='p', attrs={'data-translate': 'why_captcha_detail'})
            if p_tag.text == 'Completing the CAPTCHA proves you are a human and gives you temporary access to the web property.':
                return True
            else:
                return False

    def _check_title_tag(self):
        """
        This function is designed to query for the existence
        of specific Cloudflare related text contained in a title tag.

        :return: True or False
        :rtype: boolean
        """
        title_tag = self._raw_soup.find(name='title')
        try:
            if 'Please Wait... | Cloudflare' in title_tag.text:
                return True
            else:
                return False
        except AttributeError:
            pass

    def _check_meta_tag(self):
        """
        This function is designed to query for the existence
        of specific Cloudflare related meta tag.

        :return: True or False
        :rtype: boolean
        """
        if self._raw_soup.find(name='meta', attrs={'id': 'captcha-bypass'}):
            return True
        else:
            return False

    def cloudflare_protected_url(self):
        """
        This function is designed to query specific elements, which
        will determine if a webpage is protected by Cloudflare's
        DDoS mitigation services.

        :return: True or False
        :rtype: boolean
        """
        p_tag_bool = self._check_p_tag()
        title_tag_bool = self._check_title_tag()
        meta_tag_bool = self._check_meta_tag()

        if p_tag_bool is True:
            return True
        elif title_tag_bool is True:
            return True
        elif meta_tag_bool is True:
            return True
        else:
            return False
