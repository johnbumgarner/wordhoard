#!/usr/bin/env python3

"""
This Python script provide basic requests.get function and BeautifulSoup parent tag extraction.
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
import sys
import random
import logging
import requests
import traceback
from bs4 import BeautifulSoup
from wordhoard.utilities import wordhoard_logger

logger = logging.getLogger(__name__)
wordhoard_logger.enable_logging(logger)

##################################################################
# Array of common user agents to use for the HTTP connection
# source:  http://http://www.useragentstring.com
# source:  https://deviceatlas.com/blog/list-of-user-agent-strings
##################################################################
user_agent_strings = \
[   ##############################
    # Android Mobile User Agents #
    ##############################
    # Samsung Galaxy S9
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
    # Samsung Galaxy S8
    'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'
    # Samsung Galaxy S8
    'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
    # Samsung Galaxy S7
    'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36',
    # Samsung Galaxy S7 Edge
    'Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36',
    # Samsung Galaxy S6
    'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
    # Samsung Galaxy S6 Edge Plus
    'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
    # Nexus 6P
    'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
    # Sony Xperia XZ
    'Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
    # Sony Xperia Z5
    'Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
    # HTC One X10
    'Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36',
    # HTC One M9
    'Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3',
    ##############################
    # iPhone User Agents         #
    ##############################
    # Apple iPhone XR (Safari)
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
    # Apple iPhone XS (Chrome)
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1',
    # Apple iPhone XS Max (Firefox)
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15',
    # Apple iPhone X
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    # Apple iPhone 8
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
    # Apple iPhone 8 Plus
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1',
    # Apple iPhone 7
    'Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
    # Apple iPhone 7 Plus
    'Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
    # Apple iPhone 6
    'Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3',
    ################################
    # MS Windows Phone User Agents #
    ################################
    # Microsoft Lumia 650
    'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254',
    # Microsoft Lumia 550
    'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536',
    # Microsoft Lumia 950
    'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058',
    ######################
    # Tablet User Agents #
    ######################
    # Google Pixel C
    'Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36',
    # Sony Xperia Z4 Tablet
    'Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36',
    # Nvidia Shield Tablet K1
    'Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36',
    # Samsung Galaxy Tab S3
    'Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36',
    # Samsung Galaxy Tab A
    'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36',
    # Amazon Kindle Fire HDX 7
    'Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36',
    # LG G Pad 7.0
    'Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36',
    #######################
    # Desktop User Agents #
    #######################
    # Windows 10-based PC using Edge browser
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    # Chrome OS-based laptop using Chrome browser (Chromebook)
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    # Mac OS X-based computer using a Safari browser
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    # Windows 7-based PC using a Chrome browser
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    # Linux-based PC using a Firefox browser
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    # Chrome 70.0.3538.77
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    # Chrome 75.0.3770.90
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    # Firefox 64.0
    'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
    # Firefox 63.0
    'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
    # Firefox 62.0
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0',
    # Internet Explorer 11.0
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
]

##################################################################
# Select a random user agent from the array of user agent choices
##################################################################
rand_user_agent = random.choice(user_agent_strings)

############################################
# Create http request for harvest operation
############################################
http_headers = {'user-agent': rand_user_agent}


###################################################################
# Open a HTTP connection and harvest HTML from initial source URL
###################################################################
def get_single_page_html(url_to_scrape):
    with requests.Session() as session:
        try:
            raw_html = session.get(url_to_scrape, headers=http_headers, allow_redirects=True, verify=True, timeout=30)
        except requests.HTTPError as e:
            logger.error(f'A HTTPError has occurred when requesting {url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        except requests.URLRequired as e:
            logger.error(f'A URLRequired has occurred when requesting {url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        except requests.ConnectionError as e:
            if requests.codes: 'Failed to establish a new connection'
            logger.error(f'A ConnectionError has occurred when requesting {url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        except requests.Timeout as e:
            logger.error(f'A Timeout has occurred when requesting {url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        except requests.RequestException as e:
            logger.error(f'A RequestException has occurred when requesting {url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        return raw_html.text


def query_html(raw_html, tag_type, tag_attribute, attribute_text):
    """
    :param raw_html: The HTML code for the paged that was scraped in the previous function
    :param tag_type:
    :param tag_attribute:
    :param attribute_text:
    :return: The section of the HTML containing the information that requires further parsing
    """
    soup = BeautifulSoup(raw_html, 'lxml')
    try:
        results = soup.find(tag_type, {tag_attribute: attribute_text})
    except AttributeError as e:
        logger.error('An AttributeError has occurred when parsing with BeautifulSoup.')
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
        sys.exit(1)
    return results
