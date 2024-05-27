"""
Initialization module for the WordHoard library.

This module sets up the logging configuration and imports key components of the WordHoard library, including:
- Antonyms
- Synonyms
- Hyponyms
- Hypernyms
- Homophones
- Dictionary definitions

Logging is configured to output INFO level messages to a file named 'wordhoard_error.yaml' in the same directory.
"""
__author__ = 'John Bumgarner'
__date__ = 'May 31, 2023'
__module_name__ = 'wordhoard'
__version__ = '1.5.4'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"
__url__ = 'https://pypi.org/project/wordhoard/'
__url_bug_tracker__ = 'https://github.com/johnbumgarner/wordhoard/issues'
__url_documentation__ = 'https://wordhoard.readthedocs.io/en/latest/'
__url_source_code__ = 'https://github.com/johnbumgarner/wordhoard'

# Standard library imports
import logging

# Local or project-specific imports
from .antonyms import Antonyms
from .synonyms import Synonyms
from .hyponyms import Hyponyms
from .hypernyms import Hypernyms
from .homophones import Homophones
from .dictionary import Definitions
from .utilities import wordhoard_logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
wordhoard_logger.enable_logging(logger)
