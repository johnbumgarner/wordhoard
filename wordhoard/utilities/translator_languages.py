#!/usr/bin/env python3

"""
This Python script provides the supported languages for the translation modules
embedded into WordHoard.
"""
__author__ = 'John Bumgarner'
__date__ = 'February 12, 2023'
__status__ = 'Production'
__license__ = 'MIT'
__copyright__ = "Copyright (C) 2023 John Bumgarner"

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
# Date Completed: February 12, 2023
# Author: John Bumgarner
#
# Date Last Revised: May 24, 2024
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
from typing import Dict

class Languages:
    """
        This class provides static methods to retrieve supported languages for different translation services.

        Methods:
            - deep_supported_languages: Retrieves the supported languages for the Deep Translation service.
            - google_supported_languages: Retrieves the supported languages for the Google Translation service.
            - mymemory_supported_languages: Retrieves the supported languages for the MyMemory Translation service.
    """

    @staticmethod
    def deep_supported_languages() -> Dict[str, str]:
        """
        This function returns the supported languages for the Deep Translation service.

        :return: languages
        :rtype: dict
        """
        # Deep Translator supported languages listed in as of 02-04-2023
        supported_languages = {'bg': 'bulgarian',
                               'zh': 'chinese',
                               'cs': 'czech',
                               'da': 'danish',
                               'nl': 'dutch',
                               'en': 'english',
                               'et': 'estonian',
                               'fi': 'finnish',
                               'fr': 'french',
                               'de': 'german',
                               'el': 'greek',
                               'hu': 'hungarian',
                               'id': 'indonesian',
                               'it': 'italian',
                               'ja': 'japanese',
                               'ko': 'korean',
                               'lv': 'latvian',
                               'lt': 'lithuanian',
                               'nb': 'norwegian',
                               'pl': 'polish',
                               'pt': 'portuguese',
                               'ro': 'romanian',
                               'ru': 'russian',
                               'sk': 'slovakian',
                               'sl': 'slovenian',
                               'es': 'spanish',
                               'sv': 'swedish',
                               'tr': 'turkish',
                               'uk': 'ukrainian'}

        return supported_languages

    @staticmethod
    def google_supported_languages() -> Dict[str, str]:
        """
        This function returns the supported languages for the Google Translation service.

        :return: languages
        :rtype: dict
        """
        # Google Translator supported languages listed as of 02-10-2023
        supported_languages = {'af': 'afrikaans',
                               'sq': 'albanian',
                               'am': 'amharic',
                               'ar': 'arabic',
                               'hy': 'armenian',
                               'as': 'assamese',
                               'ay': 'aymara',
                               'az': 'azerbaijani',
                               'bm': 'bambara',
                               'eu': 'basque',
                               'be': 'belarusian',
                               'bn': 'bengali',
                               'bho': 'bhojpuri',
                               'bs': 'bosnian',
                               'bg': 'bulgarian',
                               'ca': 'catalan',
                               'ceb': 'cebuano',
                               'ny': 'chichewa',
                               'zh-CN': 'chinese (simplified)',
                               'zh-TW': 'chinese (traditional)',
                               'co': 'corsican',
                               'hr': 'croatian',
                               'cs': 'czech',
                               'da': 'danish',
                               'dv': 'dhiveh',
                               'doi': 'dogri',
                               'nl': 'dutch',
                               'en': 'english',
                               'eo': 'esperanto',
                               'et': 'estonian',
                               'ee': 'ewe',
                               'fil': 'filipino',
                               'fi': 'finnish',
                               'fr': 'french',
                               'fy': 'frisian',
                               'gl': 'galician',
                               'ka': 'georgian',
                               'de': 'german',
                               'el': 'greek',
                               'gn': 'guarani',
                               'gu': 'gujarati',
                               'ht': 'haitian creole',
                               'ha': 'hausa',
                               'haw': 'hawaiian',
                               'iw': 'hebrew',
                               'hi': 'hindi',
                               'hmn': 'hmong',
                               'hu': 'hungarian',
                               'is': 'icelandic',
                               'ig': 'igbo',
                               'ilo': 'ilocano',
                               'id': 'indonesian',
                               'ga': 'irish',
                               'it': 'italian',
                               'ja': 'japanese',
                               'jw': 'javanese',
                               'kn': 'kannada',
                               'kk': 'kazakh',
                               'km': 'khmer',
                               'rw': 'kinyarwanda',
                               'gom': 'konkani',
                               'ko': 'korean',
                               'kri': 'krio',
                               'ku': 'kurdish',
                               'ckb': 'kurdish (sorani)',
                               'ky': 'kyrgyz',
                               'lo': 'lao',
                               'la': 'latin',
                               'lv': 'latvian',
                               'ln': 'lingala',
                               'lt': 'lithuanian',
                               'lg': 'luganda',
                               'lb': 'luxembourgish',
                               'mk': 'macedonian',
                               'mai': 'maithili',
                               'mg': 'malagasy',
                               'ms': 'malay',
                               'ml': 'malayalam',
                               'mt': 'maltese',
                               'mi': 'maori',
                               'mr': 'marathi',
                               'mni': 'meiteilon',
                               'lus': 'mizo',
                               'mn': 'mongolian',
                               'my': 'myanmar',
                               'ne': 'nepali',
                               'no': 'norwegian',
                               'or': 'odia',
                               'om': 'oromo',
                               'ps': 'pashto',
                               'fa': 'persian',
                               'pl': 'polish',
                               'pt': 'portuguese',
                               'pa': 'punjabi',
                               'qu': 'quechua',
                               'ro': 'romanian',
                               'ru': 'russian',
                               'sm': 'samoan',
                               'sa': 'sanskrit',
                               'gd': 'scots gaelic',
                               'nso': 'sepedi',
                               'sr': 'serbian',
                               'st': 'sesotho',
                               'sn': 'shona',
                               'sd': 'sindhi',
                               'si': 'sinhala',
                               'sk': 'slovak',
                               'sl': 'slovenian',
                               'so': 'somali',
                               'es': 'spanish',
                               'su': 'sundanese',
                               'sw': 'swahili',
                               'sv': 'swedish',
                               'tl': 'tagalog',
                               'tg': 'tajik',
                               'ta': 'tamil',
                               'tt': 'tatar',
                               'te': 'telugu',
                               'th': 'thai',
                               'ti': 'tigrinya',
                               'ts': 'tsonga',
                               'tr': 'turkish',
                               'tk': 'turkmen',
                               'ak': 'twi',
                               'uk': 'ukrainian',
                               'ur': 'urdu',
                               'ug': 'uyghur',
                               'uz': 'uzbek',
                               'vi': 'vietnamese',
                               'cy': 'welsh',
                               'xh': 'xhosa',
                               'yi': 'yiddish',
                               'yo': 'yoruba',
                               'zu': 'zulu'}

        return supported_languages

    @staticmethod
    def mymemory_supported_languages() -> Dict[str, str]:
        """
        This function returns the supported languages for the MyMemory Translation service.

        :return: languages
        :rtype: dict
        """
        # MyMemory Translator supported languages as of 02-09-2023
        supported_languages = {'af': 'afrikaans',
                               'sq': 'albanian',
                               'am': 'amharic',
                               'ar': 'arabic',
                               'hy': 'armenian',
                               'az': 'azerbaijani',
                               'bjs': 'bajan',
                               'rm': 'balkan gipsy',
                               'eu': 'basque',
                               'be': 'bielarus',
                               'bem': 'bemba',
                               'bn': 'bengali',
                               'bi': 'bislama',
                               'bs': 'bosnian',
                               'br': 'breton',
                               'bg': 'bulgarian',
                               'ca': 'catalan',
                               'cb': 'cebuano',
                               'ny': 'chichewa',
                               'ch': 'chamorro',
                               'zh-CN': 'chinese (simplified)',
                               'zh-TW': 'chinese (traditional)',
                               'zdj': 'comorian',
                               'cop': 'coptic',
                               'aig': 'creole english (antigua and barbuda)',
                               'bah': 'creole english (bahamas)',
                               'gcl': 'creole english (grenadian)',
                               'gyn': 'creole english (guyanese)',
                               'jam': 'creole english (jamaican)',
                               'svc': 'creole english (vincentian)',
                               'vic': 'creole english (virgin islands)',
                               'ht': 'creole french (haitian)',
                               'acf': 'creole french (saint lucian)',
                               'crs': 'creole french (seselwa)',
                               'pov': 'creole portuguese (upper guinea)',
                               'co': 'corsican',
                               'hr': 'croatian',
                               'cs': 'czech',
                               'da': 'danish',
                               'nl': 'dutch',
                               'dz': 'dzongkha',
                               'en': 'english',
                               'eo': 'esperanto',
                               'et-EE': 'estonian',
                               'fn': 'fanagalo',
                               'fo': 'faroese',
                               'fi': 'finnish',
                               'fr': 'french',
                               'fy': 'frisian',
                               'gl': 'galician',
                               'ka': 'georgian',
                               'de': 'german',
                               'el': 'greek',
                               'gu': 'gujarati',
                               'ha': 'hausa',
                               'haw': 'hawaiian',
                               'he': 'hebrew',
                               'hi': 'hindi',
                               'hmn': 'hmong',
                               'hu': 'hungarian',
                               'is': 'icelandic',
                               'ig': 'igbo',
                               'id': 'indonesian',
                               'kl': 'inuktitut',
                               'ga': 'irish',
                               'it': 'italian',
                               'ja': 'japanese',
                               'jv': 'javanese',
                               'kea': 'kabuverdianu',
                               'kab': 'kabylian',
                               'kn': 'kannada',
                               'kk': 'kazakh',
                               'km': 'khmer',
                               'rw': 'kinyarwanda',
                               'rn': 'kirundi',
                               'ko': 'korean',
                               'ku': 'kurdish',
                               'ckb': 'kurdish sorani',
                               'ky': 'kyrgyz',
                               'lo': 'lao',
                               'la': 'latin',
                               'lv': 'latvian',
                               'lt': 'lithuanian',
                               'lb': 'luxembourgish',
                               'mk': 'macedonian',
                               'mg': 'malagasy',
                               'ms': 'malay',
                               'ml': 'malayalam',
                               'dv': 'maldivian',
                               'mt': 'maltese',
                               'gv': 'manx gaelic',
                               'mi': 'maori',
                               'mr': 'marathi',
                               'mh': 'marshallese',
                               'men': 'mende',
                               'mn': 'mongolian',
                               'my': 'myanmar',
                               'ne': 'nepali',
                               'niu': 'niuean',
                               'no': 'norwegian',
                               'or': 'odia',
                               'pau': 'palauan',
                               'pa': 'panjabi',
                               'pap': 'papiamentu',
                               'ps': 'pashto',
                               'pis': 'pijin',
                               'fa': 'persian',
                               'pl': 'polish',
                               'pt': 'portuguese',
                               'qu': 'quechua',
                               'ro': 'romanian',
                               'ru': 'russian',
                               'sm': 'samoan',
                               'gd': 'scots gaelic',
                               'sr': 'serbian',
                               'st': 'sesotho',
                               'sn': 'shona',
                               'sd': 'sindhi',
                               'si': 'sinhala',
                               'sk': 'slovak',
                               'sl': 'slovenian',
                               'so': 'somali',
                               'es': 'spanish',
                               'su': 'sundanese',
                               'sw': 'swahili',
                               'sv': 'swedish',
                               'de-ch': 'swiss german',
                               'tl': 'tagalog',
                               'tg': 'tajik',
                               'tmh': 'tamashek',
                               'ta': 'tamil',
                               'tt': 'tatar',
                               'te': 'telugu',
                               'tet': 'tetum',
                               'th': 'thai',
                               'bo': 'tibetan',
                               'ti': 'tigrinya',
                               'tpi': 'tok pisin',
                               'tkl': 'tokelauan',
                               'to': 'tongan',
                               'tn': 'tswana',
                               'tr': 'turkish',
                               'tk': 'turkmen',
                               'tvl': 'tuvaluan',
                               'uk': 'ukrainian',
                               'ppk': 'uma',
                               'ur': 'urdu',
                               'ug': 'uyghur',
                               'uz': 'uzbek',
                               'vi': 'vietnamese',
                               'wls': 'wallisian',
                               'cy': 'welsh',
                               'wo': 'wolof',
                               'xh': 'xhosa',
                               'yi': 'yiddish',
                               'yo': 'yoruba',
                               'zu': 'zulu'}

        return supported_languages
