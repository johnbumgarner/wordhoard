#!/usr/bin/env python3

"""
This Python module is to create temporary dictionary caches.  These caches are
designed to limit redundant queries.
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
# Date Last Revised: May 28, 2024
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
from typing import List, Dict, Optional, Tuple, Set

##################################################################################
# in memory temporary cache for antonyms
##################################################################################
temporary_dict_antonyms: Dict[str, Dict[str, Set[str]]] = {}

def cache_antonyms(word:  str) -> Tuple[bool, Optional[str]]:
    """
    Checks if the antonyms for a given word are cached in the temporary dictionary.

    :param word: The word to check for cached antonyms.
    :type word: str
    :return: A tuple indicating success (True if antonyms are cached, False otherwise) and the cached antonyms if found.
    :rtype: Tuple[bool, Optional[str]]
    """
    success = (retrieved := temporary_dict_antonyms.get(word)) is not None
    return success, retrieved

def insert_word_cache_antonyms(word: str, pos_category: str, antonyms: Set[str]) -> None:
    """
    Inserts or updates the cache with antonyms for a word in the temporary dictionary.

    :param word: The word to insert or update the cache for.
    :type word: str
    :param pos_category: The part-of-speech category of the antonyms.
    :type pos_category: str
    :param antonyms: The set of antonyms to cache.
    :type antonyms: Set[str]
    :return: None
    """
    if word not in temporary_dict_antonyms:
        # Initialize the dictionary for the word with the given part of speech category
        temporary_dict_antonyms[word] = {pos_category: antonyms}
    elif pos_category in temporary_dict_antonyms[word]:
        # Deduplicate and update the existing antonyms list
        deduplicated_values = set(antonyms) - set(temporary_dict_antonyms[word][pos_category])
        temporary_dict_antonyms[word][pos_category] += list(deduplicated_values)
    else:
        # Initialize the list for the part of speech category
        temporary_dict_antonyms[word][pos_category] = antonyms


##################################################################################
# in memory temporary cache for synonyms
##################################################################################
temporary_dict_synonyms: Dict[str, Dict[str, Set[str]]] = {}

def cache_synonyms(word:  str) -> Tuple[bool, Optional[str]]:
    """
    Checks if the synonyms for a given word are cached in the temporary dictionary.

    :param word: The word to check for cached synonyms.
    :type word: str
    :return: A tuple indicating success (True if synonyms are cached, False otherwise) and the cached synonyms if found.
    :rtype: Tuple[bool, Optional[str]]
    """
    success = (retrieved := temporary_dict_synonyms.get(word)) is not None
    return success, retrieved

def insert_word_cache_synonyms(word: str, pos_category: str, synonyms: Set[str]) -> None:
    """
    Inserts or updates the cache with synonyms for a word in the temporary dictionary.

    :param word: The word to insert or update the cache for.
    :type word: str
    :param pos_category: The part-of-speech category of the synonyms.
    :type pos_category: str
    :param synonyms: The set of synonyms to cache.
    :type synonyms: Set[str]
    :return: None
    """
    if word not in temporary_dict_synonyms:
        # Initialize the dictionary for the word with the given part of speech category
        temporary_dict_synonyms[word] = {pos_category: synonyms}
    elif word in temporary_dict_synonyms and pos_category in temporary_dict_synonyms[word]:
        # Deduplicate and update the existing synonyms list
        deduplicated_values = set(synonyms) - set(temporary_dict_synonyms[word][pos_category])
        temporary_dict_synonyms[word][pos_category] += list(deduplicated_values)
    else:
        # Initialize the list for the part of speech category
        temporary_dict_synonyms[word][pos_category] = synonyms

##################################################################################
# in memory temporary cache for definitions
##################################################################################
temporary_dict_definition: Dict[str, Dict[str, Set[str]]] = {}

def cache_definition(word:  str) -> Tuple[bool, Optional[str]]:
    """
    Checks if the definitions for a given word are cached in the temporary dictionary.

    :param word: The word to check for cached definitions.
    :type word: str
    :return: A tuple indicating success (True if definitions are cached, False otherwise) and the cached definitions if found.
    :rtype: Tuple[bool, Optional[str]]
    """
    success = (retrieved := temporary_dict_definition.get(word)) is not None
    return success, retrieved

def insert_word_cache_definition(word: str, pos_category: str, definitions: Set[str]) -> None:
    """
    Inserts or updates the cache with definitions for a word in the temporary dictionary.

    :param word: The word to insert or update the cache for.
    :type word: str
    :param pos_category: The part-of-speech category of the definitions.
    :type pos_category: str
    :param definitions: The set of definitions to cache.
    :type definitions: Set[str]
    :return: None
    """
    if word not in temporary_dict_definition:
        # Initialize the dictionary for the word with the given part of speech category
        temporary_dict_definition[word] = {pos_category: definitions}
    elif word in temporary_dict_definition and pos_category in temporary_dict_definition[word]:
        # Deduplicate and update the existing definitions list
        deduplicated_values = set(definitions) - set(temporary_dict_definition[word][pos_category])
        temporary_dict_definition[word][pos_category] += list(deduplicated_values)
    else:
        # Initialize the list for the part of speech category
        temporary_dict_definition[word][pos_category] = definitions

##################################################################################
# in memory temporary cache for hypernyms
##################################################################################
temporary_dict_hypernyms: Dict[str, list[str]] = {}

def cache_hypernyms(word: str) -> Tuple[bool, Optional[List[str]]]:
    """
    Checks if the hypernyms for a given word are cached in the temporary dictionary.

    :param word: The word to check for cached hypernyms.
    :type word: str
    :return: A tuple indicating success (True if hypernyms are cached, False otherwise) and the cached hypernyms if found.
    :rtype: Tuple[bool, Optional[List[str]]]
    """
    try:
        values = temporary_dict_hypernyms[word]
    except KeyError:
        return False, None
    else:
        return True, sorted(set(values))

def insert_word_cache_hypernyms(word: str, values: List[str]) -> None:
    """
    Inserts or updates the cache with hypernyms for a word in the temporary dictionary.

    :param word: The word to insert or update the cache for.
    :type word: str
    :param values: The list of hypernyms to cache.
    :type values: List[str]
    :return: None
    """
    if word in temporary_dict_hypernyms:
        deduplicated_values = set(values) - set(temporary_dict_hypernyms.get(word))
        temporary_dict_hypernyms[word].extend(deduplicated_values)
    else:
        temporary_dict_hypernyms[word] = values


##################################################################################
# in memory temporary cache for hyponyms
##################################################################################
temporary_dict_hyponyms: Dict[str, List[str]] = {}

def cache_hyponyms(word: str) -> Tuple[bool, Optional[List[str]]]:
    """
    Checks if the hyponyms for a given word are cached in the temporary dictionary.

    :param word: The word to check for cached hyponyms.
    :type word: str
    :return: A tuple indicating success (True if hyponyms are cached, False otherwise) and the cached hyponyms if found.
    :rtype: Tuple[bool, Optional[List[str]]]
    """
    try:
        values = temporary_dict_hyponyms[word]
    except KeyError:
        return False, None
    else:
        return True, sorted(set(values))

def insert_word_cache_hyponyms(word: str, values: List[str]) -> None:
    """
    Inserts or updates the cache with hyponyms for a word in the temporary dictionary.

    :param word: The word to insert or update the cache for.
    :type word: str
    :param values: The list of hyponyms to cache.
    :type values: List[str]
    :return: None
    """
    if word in temporary_dict_hyponyms:
        deduplicated_values = set(values) - set(temporary_dict_hyponyms.get(word))
        temporary_dict_hyponyms[word].extend(deduplicated_values)
    else:
        temporary_dict_hyponyms[word] = values
