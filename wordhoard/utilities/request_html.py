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
# Date Last Revised: March 18, 2023
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
import sys
import logging
import requests
import warnings
import traceback
from requests.adapters import Retry
from typing import Dict, Optional, Tuple
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError
from wordhoard.utilities.colorized_text import colorized_text
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

    def __init__(self,
                 url_to_scrape: str = '',
                 user_agent: Optional[str] = None,
                 proxies: Optional[Dict[str, str]] = None):

        # Reformat complex words, such as 'artificial intelligence' contained in a URL
        # with a string.replace. The new format is 'artificial%20intelligence', which
        # can be passed Python Requests as a quoted string
        self._url_to_scrape = url_to_scrape.replace(" ", "%20")

        self._proxies = proxies
        self._user_agent = user_agent

    # reference: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    @staticmethod
    def _requests_retry_session(retries: int = 5,
                                backoff_factor: float = 0.5,
                                status_forcelist: Tuple[int] = (500, 502, 503, 504),
                                session: requests.sessions.Session = None,
                                ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    ###################################################################
    # Open a HTTP connection and harvest HTML from initial source URL
    ###################################################################
    def get_website_html(self) -> requests.models.Response:
        response = ''
        try:
            if self._proxies is None and self._user_agent is None:
                response = self._requests_retry_session().get(self._url_to_scrape,
                                                              headers=http_headers,
                                                              allow_redirects=True,
                                                              verify=True,
                                                              timeout=(30, 45))

            elif self._proxies is None and self._user_agent is not None:
                response = self._requests_retry_session().get(self._url_to_scrape,
                                                              headers={'user-agent': self._user_agent},
                                                              allow_redirects=True,
                                                              verify=True,
                                                              timeout=(30, 45))

            elif self._proxies is not None and self._user_agent is None:
                response = self._requests_retry_session().get(self._url_to_scrape,
                                                              headers=http_headers,
                                                              allow_redirects=True,
                                                              verify=True,
                                                              timeout=(30, 45),
                                                              proxies=self._proxies)

            elif self._proxies is not None and self._user_agent is not None:
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
                print(colorized_text(255, 0, 0,
                                     'An HTTP 500 Internal Server Error has occurred.'
                                     '\nPlease review the WordHoard logs for additional information.'))
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info(
                    "The HTTP 500 Internal Server Error status code indicates that the server encountered "
                    "an unexpected condition that prevented it from fulfilling the request.")
                logger.info(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            elif response.status_code == 503:
                print(colorized_text(255, 0, 0,
                                     'A 503 Service Unavailable status code has been detected.'
                                     '\nPlease review the WordHoard logs for additional information.'))
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info(
                    "The 503 Service Unavailable status code indicates that the server is temporarily unable "
                    "to handle the request")
                logger.error(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            elif response.status_code == 504:
                print(colorized_text(255, 0, 0,
                                     'An HTTP 504 Gateway Timeout Error status code has been detected.'
                                     '\nPlease review the WordHoard logs for additional information.'))
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info(
                    "The HTTP 504 Gateway Timeout Error status code indicating that a server, which is "
                    "currently acting as a gateway or proxy, did not receive a timely response "
                    "from another server")
                logger.error(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            elif response.status_code == 521:
                print(colorized_text(255, 0, 0,
                                     'A 521 status code has been detected. This code is often used by CloudFlare.'
                                     '\nPlease review the WordHoard logs for additional information.'))
                logger.info('-' * 80)
                logger.error(f'Response Status Code: {response.status_code}')
                logger.info("This status code is not specified in any RFCs, but is used by CloudFlare's"
                            "reverse proxies to indicate that the origin webserver refused the connection")
                logger.info(f'Requested URL: {self._url_to_scrape}')
                logger.info('-' * 80)
            else:
                if response.status_code != 200:
                    print(colorized_text(255, 0, 0,
                                         f'The Status Code: {response.status_code} has been detected.'
                                         '\nPlease review the WordHoard logs for additional information.'))
                    logger.error(f'Response Status Code: {response.status_code}')
                    logger.info(f'Requested URL: {self._url_to_scrape}')
                    logger.info('-' * 80)

        except requests.HTTPError as error:
            print(colorized_text(255, 0, 0,
                                 'A HTTPError has occurred.'
                                 '\nPlease review the WordHoard logs for additional information.'))
            logger.error(f'A HTTPError has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            sys.exit(1)
        except requests.URLRequired as error:
            logger.error(f'A URLRequired has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            sys.exit(1)
        except requests.exceptions.ProxyError as error:
            print(colorized_text(255, 0, 0,
                                 'A unknown type of Proxy Error has occurred.'
                                 '\nPlease verify that your proxies are working.'))
            logger.error(f'A ProxyError has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            sys.exit(1)
        except MaxRetryError as error:
            print(colorized_text(255, 0, 0,
                                 'The max number of connection retries was exceeded.'
                                 '\nPlease review the WordHoard logs for additional information.'))
            logger.error(f'A MaxRetryError has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            sys.exit(1)
        except requests.ConnectionError as error:
            print(colorized_text(255, 0, 0,
                                 'A ConnectionError has occurred.'
                                 '\nPlease review the WordHoard logs for additional information.'))
            logger.error(f'A ConnectionError has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            sys.exit(1)
        except requests.Timeout as error:
            print(colorized_text(255, 0, 0,
                                 'A connection timeout has occurred.'
                                 '\nPlease review the WordHoard logs for additional information.'))
            logger.error(f'A Timeout has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            sys.exit(1)
        except requests.RequestException as error:
            print(colorized_text(255, 0, 0,
                                 'A RequestException has occurred.'
                                 '\nPlease review the WordHoard logs for additional information.'))
            logger.error(f'A RequestException has occurred when requesting {self._url_to_scrape}')
            logger.error(''.join(traceback.format_tb(error.__traceback__)))
            sys.exit(1)
        return response
