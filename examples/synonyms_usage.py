#!/usr/bin/env python3

######################################################
# This script has several usage examples for querying
# both a single source and multiple sources for
# synonyms related to a specific word.
######################################################

# Import the synonyms functions
from wordhoard import synonyms

# Example 1: single source query
# Query synonym.com for synonyms related to
# the word "mother"
results = synonyms.query_synonym_com('mother')
print(results)
# The output of this query is a list of synonyms
# for the word "mother." The list has been sorted
# in alphabetical order.
# ['female parent', 'ma', 'mama', 'mamma', 'mammy', 'mater', 'mom', 'momma', 'mommy', 'mother-in-law', 'mum',
#  'mummy', 'para I', 'parent', 'primipara', 'puerpera', 'quadripara', 'quintipara', 'supermom', 'surrogate mother']


# Example 2: multiple sources query
# This example queries each source for
# synonyms related to the word "mother"
synonym_01 = synonyms.query_collins_dictionary_synonym('mother')
synonym_02 = synonyms.query_synonym_com('mother')
synonym_03 = synonyms.query_thesaurus_com('mother')
synonym_04 = synonyms.query_thesaurus_plus('mother')
synonym_results = sorted(set([y for x in [synonym_01, synonym_02, synonym_03, synonym_04] for y in x]))
print(synonym_results)
# The output of this query is a list of synonyms
# for the word "mother." The list has been sorted
# in alphabetical order.
# ['ancestor', 'antecedent', 'architect', 'author', 'begetter', 'beginning', 'child-bearer', 'creator',
#  'dam', 'female parent', 'forebearer', 'forefather', 'foster mother', 'founder', 'fount', 'fountain',
#  'fountainhead', 'genesis', 'inspiration', 'inventor', 'lady', 'ma', 'maker', 'mam', 'mama', 'mamma',
#  'mammy', 'mater', 'materfamilias', 'matriarch', 'mom', 'momma', 'mommy', 'mother-in-law', 'mum',
#  'mummy', 'nurse', 'old lady', 'old woman', 'origin', 'originator', 'para I', 'parent', 'predecessor',
#  'primipara', 'procreator', 'producer', 'progenitor', 'provenience', 'puerpera', 'quadripara', 'quintipara',
#  'sire', 'source', 'spring', 'start', 'stimulus', 'supermom', 'surrogate mother', 'wellspring']
