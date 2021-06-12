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
#
# Date Completed: October 15, 2020
# Author: John Bumgarner
#
# Date Revised: June 1, 2021
# Revised by: John Bumgarner
#
##################################################################################

##################################################################################
# in memory temporary cache for antonyms
##################################################################################
temporary_dict_antonyms = {}


def cache_antonyms(word, source):
    item_to_check = f'{word}_{source}'
    if item_to_check in temporary_dict_antonyms.keys():
        new_dict = {key: val for (key, val) in temporary_dict_antonyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_antonyms(word, source, values):
    key = f'{word}_{source}'
    temporary_dict_antonyms[key] = values


##################################################################################
# in memory temporary cache for synonyms
##################################################################################
temporary_dict_synonyms = {}


def cache_synonyms(word, source):
    item_to_check = f'{word}_{source}'
    if item_to_check in temporary_dict_synonyms.keys():
        new_dict = {key: val for (key, val) in temporary_dict_synonyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_synonyms(word, source, values):
    key = f'{word}_{source}'
    temporary_dict_synonyms[key] = values


##################################################################################
# in memory temporary cache for definitions
##################################################################################
temporary_dict_definition = {}


def cache_definition(word, source):
    item_to_check = f'{word}_{source}'
    if item_to_check in temporary_dict_definition.keys():
        new_dict = {key: val for (key, val) in temporary_dict_synonyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_definition(word, source, values):
    key = f'{word}_{source}'
    temporary_dict_definition[key] = values


##################################################################################
# in memory temporary cache for hypernyms
##################################################################################
temporary_dict_hypernyms = {}


def cache_hypernyms(word, source):
    item_to_check = f'{word}_{source}'
    if item_to_check in temporary_dict_hypernyms.keys():
        new_dict = {key: val for (key, val) in temporary_dict_hypernyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_hypernyms(word, source, values):
    key = f'{word}_{source}'
    temporary_dict_hypernyms[key] = values


##################################################################################
# in memory temporary cache for hyponyms
##################################################################################
temporary_dict_hyponyms = {}


def cache_hyponyms(word, source):
    item_to_check = f'{word}_{source}'
    if item_to_check in temporary_dict_hyponyms.keys():
        new_dict = {key: val for (key, val) in temporary_dict_hyponyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_hyponyms(word, source, values):
    key = f'{word}_{source}'
    temporary_dict_hyponyms[key] = values

