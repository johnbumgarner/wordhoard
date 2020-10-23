#!/usr/bin/env python3

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
# Date Revised:
# Revised by:
#
# This Python script is to create temporary dictionary caches.  These caches are
# designed to limit redundant queries.
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
