#!/usr/bin/env python3

"""
This Python script is to create temporary dictionary caches.  These caches are
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
# Date Last Revised: March 18, 2023
# Revised by: John Bumgarner
##################################################################################

##################################################################################
# Python imports required for basic operations
##################################################################################
from typing import List, Dict, Optional, Tuple, Union, Set

##################################################################################
# in memory temporary cache for antonyms
##################################################################################
temporary_dict_antonyms: Dict[str, Dict[str, Set[str]]] = {}

def cache_antonyms(word:  str) -> Tuple[bool, Optional[str]]:
    success = (retrieved := temporary_dict_antonyms.get(word)) is not None
    return success, retrieved

def insert_word_cache_antonyms(word: str, pos_category: str, antonyms: Set[str]) -> None:
    if word in temporary_dict_antonyms:
        deduplicated_values = set(antonyms) - set(temporary_dict_antonyms.get(word))
        temporary_dict_antonyms[word][pos_category] += deduplicated_values
    else:
        temporary_dict_antonyms[word] = {pos_category: antonyms}


##################################################################################
# in memory temporary cache for synonyms
##################################################################################
temporary_dict_synonyms: Dict[str, Dict[str, Set[str]]] = {}

def cache_synonyms(word:  str) -> Tuple[bool, Optional[str]]:
    success = (retrieved := temporary_dict_synonyms.get(word)) is not None
    return success, retrieved

def insert_word_cache_synonyms(word: str, pos_category: str, synonyms: Set[str]) -> None:
    if word in temporary_dict_synonyms:
        deduplicated_values = set(synonyms) - set(temporary_dict_synonyms.get(word))
        temporary_dict_synonyms[word][pos_category] += deduplicated_values
    else:
        temporary_dict_synonyms[word] = {pos_category: synonyms}



##################################################################################
# in memory temporary cache for definitions
##################################################################################
temporary_dict_definition: Dict[str, Dict[str, Set[str]]] = {}


def cache_definition(word:  str) -> Tuple[bool, Optional[str]]:
    success = (retrieved := temporary_dict_definition.get(word)) is not None
    return success, retrieved


def insert_word_cache_definition(word: str, pos_category: str, definitions: Set[str]) -> None:
    if word in temporary_dict_definition:
        deduplicated_values = set(definitions) - set(temporary_dict_definition.get(word))
        temporary_dict_definition[word][pos_category] += deduplicated_values
    else:
        temporary_dict_definition[word] = {pos_category: definitions}



##################################################################################
# in memory temporary cache for hypernyms
##################################################################################
temporary_dict_hypernyms: Dict[str, list[str]] = {}


def cache_hypernyms(word: str) -> Tuple[bool, Optional[List[str]]]:
    try:
        values = temporary_dict_hypernyms[word]
    except KeyError:
        return False, None
    else:
        return True, sorted(set(values))


def insert_word_cache_hypernyms(word: str, values: List[str]) -> None:
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
    try:
        values = temporary_dict_hyponyms[word]
    except KeyError:
        return False, None
    else:
        return True, sorted(set(values))


def insert_word_cache_hyponyms(word: str, values: List[str]) -> None:
    if word in temporary_dict_hyponyms:
        deduplicated_values = set(values) - set(temporary_dict_hyponyms.get(word))
        temporary_dict_hyponyms[word].extend(deduplicated_values)
    else:
        temporary_dict_hyponyms[word] = values
