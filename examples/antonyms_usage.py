#!/usr/bin/env python3

######################################################
# This script has several usage examples for querying
# both a single source and multiple sources for
# antonyms related to a specific word.
######################################################

# Import the antonyms functions
from wordhoard import antonyms

# Example 1: single source query
# Query synonym.com for antonyms related to
# the word "mother"
results = antonyms.query_synonym_com('mother')
print(results)
# The output of this query is a list of antonyms
# for the word "mother." The list has been sorted
# in alphabetical order.
# ['child', 'descendant', 'father', 'follower', 'male parent']


# Example 2: multiple sources query
# This example queries each source for
# antonyms related to the word "mother"
antonyms_01 = antonyms.query_synonym_com('mother')
antonyms_02 = antonyms.query_thesaurus_com('mother')
antonyms_03 = antonyms.query_thesaurus_plus('mother')
antonyms_results = sorted(set([y for x in [antonyms_01, antonyms_02, antonyms_03] for y in x]))
print(antonyms_results)
# The output of this query is a list of antonyms
# for the word "mother." The list has been sorted
# in alphabetical order.
# ['abort', 'begetter', 'brush', 'brush aside', 'brush off', 'child', 'dad', 'daughter', 'descendant',
#  'effect', 'end', 'father', 'follower', 'forget', 'ignore', 'lose', 'male parent', 'miscarry', 'neglect',
#  'offspring', 'overlook', 'result', 'slight']


