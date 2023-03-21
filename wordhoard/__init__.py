__author__ = 'John Bumgarner'
__date__ = 'July 5, 2021'
__module_name__ = 'wordhoard'
__version__ = '1.5.3'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"
__url__ = 'https://pypi.org/project/wordhoard/'
__url_bug_tracker__ = 'https://github.com/johnbumgarner/wordhoard/issues'
__url_documentation__ = 'https://wordhoard.readthedocs.io/en/latest/'
__url_source_code__ = 'https://github.com/johnbumgarner/wordhoard'

from .antonyms import Antonyms
from .synonyms import Synonyms
from .hyponyms import Hyponyms
from .hypernyms import Hypernyms
from .homophones import Homophones
from .dictionary import Definitions

import logging
from .utilities import wordhoard_logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
wordhoard_logger.enable_logging(logger)

