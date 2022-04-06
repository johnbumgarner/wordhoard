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
# Date Completed: October 15, 2020
# Author: John Bumgarner
#
# Date Last Revised: April 04, 2022
# Revised by: John Bumgarner
#
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import sys
import urllib3
import logging
import requests
import warnings
import traceback
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from wordhoard.utilities.user_agents import get_random_user_agent

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

logger = logging.getLogger(__name__)

##################################################################
# Select a random user agent from the array of user agent choices
##################################################################
rand_user_agent = get_random_user_agent()

############################################
# Create http request for harvest operation
############################################
http_headers = {'user-agent': rand_user_agent}


class Query(object):

    def __init__(self, url_to_scrape='', user_agent=None, proxies=None):

        self._url_to_scrape = url_to_scrape
        self._proxies = proxies
        self._user_agent = user_agent

    # reference: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    @staticmethod
    def _requests_retry_session(retries=5,
                                backoff_factor=0.5,
                                status_force_list=(500, 502, 503, 504),
                                session=None,
                                ):

        session = session or requests.Session()

        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_force_list,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    ###################################################################
    # Open a HTTP connection and harvest HTML from initial source URL
    ###################################################################
    def get_single_page_html(self):
        response = ''
        try:
            if self._proxies is None:
                if self._user_agent is None:
                    response = self._requests_retry_session().get(self._url_to_scrape,
                                                                  headers=http_headers,
                                                                  allow_redirects=True,
                                                                  verify=True,
                                                                  timeout=(30, 45))

                elif self._user_agent is not None:
                    response = self._requests_retry_session().get(self._url_to_scrape,
                                                                  headers={'user-agent': self._user_agent},
                                                                  allow_redirects=True,
                                                                  verify=True,
                                                                  timeout=(30, 45))
            elif self._proxies is not None:
                if self._user_agent is None:
                    response = self._requests_retry_session().get(self._url_to_scrape,
                                                                  headers=http_headers,
                                                                  allow_redirects=True,
                                                                  verify=True,
                                                                  timeout=(30, 45),
                                                                  proxies=self._proxies)
                elif self._user_agent is not None:
                    response = self._requests_retry_session().get(self._url_to_scrape,
                                                                  headers={'user-agent': self._user_agent},
                                                                  allow_redirects=True,
                                                                  verify=True,
                                                                  timeout=(30, 45),
                                                                  proxies=self._proxies)

            cloudflare_protected = bool([value for (key, value) in response.headers.items()
                                         if key == 'Server'
                                         and value == 'cloudflare'])

            if response.status_code == 403:
                if cloudflare_protected is True:
                    logger.info('-' * 80)
                    logger.info("The requested URL is protected by Cloudflare's DDoS mitigation service.")
                    logger.info(f'Requested URL: {self._url_to_scrape}')
                    logger.info('-' * 80)
                elif cloudflare_protected is False:
                    logger.info('-' * 80)
                    logger.error(f'Response Status Code: {response.status_code}')
                    logger.info('HTTP 403 is an HTTP status code meaning access to the requested '
                                'resource is forbidden.')
                    logger.info(f'Requested URL: {self._url_to_scrape}')
                    logger.info('-' * 80)
            elif response.status_code == 404:
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info(
                    'The HTTP 404 Not Found status code means that the file or page that the was requested '
                    'was not found on the server')
                logger.info(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            elif response.status_code == 500:
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info(
                    "The HTTP 500 Internal Server Error status code indicates that the server encountered "
                    "an unexpected condition that prevented it from fulfilling the request.")
                logger.info(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            elif response.status_code == 503:
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info(
                    "The 503 Service Unavailable status code indicates that the server is temporarily unable "
                    "to handle the request")
                logger.error(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            elif response.status_code == 504:
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info(
                    "The HTTP 504 Gateway Timeout Error status code indicating that a server, which is "
                    "currently acting as a gateway or proxy, did not receive a timely response "
                    "from another server")
                logger.error(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            elif response.status_code == 521:
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info("This status code is not specified in any RFCs, but is used by CloudFlare's"
                            "reverse proxies to indicate that the origin webserver refused the connection")
                logger.info(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            else:
                if response.status_code != 200:
                    logger.error(f'Response Status Code: {response.status_code}')
                    logger.info(f'Requested URL: {self._url_to_scrape}')
                    logger.info('-' * 80)

        except requests.HTTPError as e:
            logger.error(f'A HTTPError has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        except requests.URLRequired as e:
            logger.error(f'A URLRequired has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        except requests.exceptions.ProxyError as e:
            logger.error(f'A ProxyError has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
        except urllib3.exceptions.MaxRetryError as e:
            logger.error(f'A MaxRetryError has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
        except requests.ConnectionError as e:
            if requests.codes: 'Failed to establish a new connection'
            logger.error(f'A ConnectionError has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
        except requests.Timeout as e:
            logger.error(f'A Timeout has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        except requests.RequestException as e:
            logger.error(f'A RequestException has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
            sys.exit(1)
        return response

    @staticmethod
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
