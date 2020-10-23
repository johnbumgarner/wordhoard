#!/usr/bin/env python3

######################################################
# This script has several usage examples for querying
# both a single source and multiple sources for
# definitions related to a specific word.
######################################################

# Import the dictionary functions
from wordhoard import dictionary

# Example 1: single source query
# Query synonym.com for the definition for
# the word "mother"
results = dictionary.query_synonym_com('mother')
print(results)
# a woman who has given birth to a child (also used as a term of address to your mother)

# Example 2: multiple sources query
# This example queries each source for
# definitions related to the word "mother"
definition_01 = dictionary.query_collins_dictionary_synonym('mother')
definition_02 = dictionary.query_synonym_com('mother')
definition_03 = dictionary.query_thesaurus_com('mother')
definition_results = [y for y in [definition_01, definition_02, definition_03]]
print(definition_results)
# ["a person's own mother", 'a woman who has given birth to a child (also used as a term of address to your mother)',
# 'female person who has borne children']


