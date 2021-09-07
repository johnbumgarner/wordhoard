__author__ = 'John Bumgarner'
__date__ = 'July 5, 2021'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2021 John Bumgarner"

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

