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
# Date Last Revised: July 4, 2021
# Revised by: John Bumgarner
#
##################################################################################

##################################################################################
# in memory temporary cache for antonyms
##################################################################################
temporary_dict_antonyms = {}


def cache_antonyms(word):
    item_to_check = f'{word}'
    if item_to_check in temporary_dict_antonyms.keys():
        new_dict = {key: val for (key, val) in temporary_dict_antonyms.items() if key == item_to_check}
        return new_dict
    else:
        return False


def insert_word_cache_antonyms(word, values):
    if word in temporary_dict_antonyms:
        temporary_dict_antonyms[word].append(values)
    else:
        temporary_dict_antonyms[word] = values


##################################################################################
# in memory temporary cache for synonyms
##################################################################################
temporary_dict_synonyms = {}


def cache_synonyms(word):
    item_to_check = f'{word}'
    if item_to_check in temporary_dict_synonyms.keys():
        new_dict = {key: val for (key, val) in temporary_dict_synonyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_synonyms(word, values):
    if word in temporary_dict_synonyms:
        temporary_dict_synonyms[word].append(values)
    else:
        temporary_dict_synonyms[word] = values


##################################################################################
# in memory temporary cache for definitions
##################################################################################
temporary_dict_definition = {}


def cache_definition(word):
    item_to_check = f'{word}'
    if item_to_check in temporary_dict_definition.keys():
        new_dict = {key: val for (key, val) in temporary_dict_synonyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_definition(word, values):
    if word in temporary_dict_definition:
        temporary_dict_definition.update({word: values})
    else:
        temporary_dict_definition[word] = values


##################################################################################
# in memory temporary cache for hypernyms
##################################################################################
temporary_dict_hypernyms = {}


def cache_hypernyms(word):
    item_to_check = f'{word}'
    if item_to_check in temporary_dict_hypernyms.keys():
        new_dict = {key: val for (key, val) in temporary_dict_hypernyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_hypernyms(word, values):
    if word in temporary_dict_hypernyms:
        temporary_dict_hypernyms[word].append(values)
    else:
        temporary_dict_hypernyms[word] = values


##################################################################################
# in memory temporary cache for hyponyms
##################################################################################
temporary_dict_hyponyms = {}


def cache_hyponyms(word):
    item_to_check = f'{word}'
    if item_to_check in temporary_dict_hyponyms.keys():
        new_dict = {key: val for (key, val) in temporary_dict_hyponyms.items() if key == word}
        return new_dict
    else:
        return False


def insert_word_cache_hyponyms(word, values):
    if word in temporary_dict_hyponyms:
        temporary_dict_hyponyms[word].append(values)
    else:
        temporary_dict_hyponyms[word] = values
