
<p align="center">
   <! -- Graphic source: https://thesaurus.plus --> 
  <img src="https://github.com/johnbumgarner/wordhoard/blob/master/graphic/wordhoard_graphic.jpg"/>
</p>

# Overview

![PyPI version](https://img.shields.io/pypi/v/wordhoard?style=flat-square)&nbsp;
![License: MIT](https://img.shields.io/github/license/johnbumgarner/wordhoard?style=flat-square) &nbsp;


<p align="justify">
The Oxford Dictionary defines <i>wordhoard</i> as a supply of words or a lexicon. <i>Wordhoard</i> is a <i>Python</i> 3 module that can be used to obtain antonyms, synonyms and definitions for words. 
  
This <i>Python</i> module was spawned from a <a href="https://stackoverflow.com/questions/63705803/merge-related-words-in-nlp/63771196#63771196">Stack Overflow</a> bountied question.  That question forced me to looked into the best practices for obtaining a comprehensive lists of synonyms for a given word.  During my research, I developed the repository <a href="https://github.com/johnbumgarner/synonyms_discovery_aggregation">synonym discovery and aggregation</a> and decided to create <i>wordhoard</i>.
<p>
   
# Primary Use Case
<p align="justify"> 
Textual analysis is a broad term for various research methodologies used to qualitatively describe, interpret and understand text data. These methodologies are mainly used in academic research to analyze content related to media and communication studies, popular culture, sociology, and philosophy. Textual analysis allows these researchers to quickly obtain relevant insights from unstructured data. All types of information can be gleaned from textual data, especially from social media posts or news articles. Some of this information includes the overall concept of the subtext, symbolism within the text, assumptions being made and potential relative value to a subject (e.g. data science). In some cases it is possible to deduce the relative historical and cultural context of a body of text using analysis techniques coupled with knowledge from different disciplines, like linguistics and semiotics.
   
Word frequency is the technique used in textual analysis to measure the frequency of a specific word or word grouping within unstructured data. Measuring the number of word occurrences in a corpus allows a researcher to garner interesting insights about the text. A subset of word frequency is the correlation between a given word and that word's relationship to either antonyms and synonyms within the specific corpus being analyzed. Knowing these relationships is critical to improving word frequencies and topic modeling.

<i>Wordhoard</i> was designed to assist researchers performing textual analysis to build more comprehensive antonyms and synonyms lists.
</p>

# Installation

<p align="justify"> 
   Install the distribution via pip:
</p>

```python
pip3 install wordhoard
```

# Basic Usage Antonyms

## Antonyms

## Antonyms - single source

```python
from wordhoard import antonyms

results = antonyms.query_synonym_com('mother')
print(results)
['father', 'male parnt', 'child', 'descendant', 'follower']
```

## Antonyms - multiple sources

```python
from wordhoard import antonyms

antonyms_01 = antonyms.query_synonym_com('mother')
antonyms_02 = antonyms.query_thesaurus_com('mother')
antonyms_03 = antonyms.query_thesaurus_plus('mother')
antonyms_results = sorted(set([y for x in [antonyms_01, antonyms_02, antonyms_03] for y in x]))
print(antonyms_results)
['abort', 'begetter', 'brush', 'brush aside', 'brush off', 'child', 'dad', 'daughter', 'descendant', 'effect', 'end', 'father', 'follower', 
forget', 'ignore', 'lose', 'male parent', 'miscarry', 'neglect', 'offspring', 'overlook', 'result', 'slight']
```

# Basic Usage Synonyms

## Synonyms - single source
  
```python
from wordhoard import synonyms

results = synonyms.query_synonym_com('mother')
print(results)
['female parent', 'ma', 'mama', 'mamma', 'mammy', 'mater', 'mom', 'momma', 'mommy', 'mother-in-law', 'mum', 'mummy', 'para I', 'parent', 
'primipara', 'puerpera', 'quadripara', 'quintipara', 'supermom', 'surrogate mother']
```

## Synonyms - multiple sources

```python
from wordhoard import synonyms

synonym_01 = synonyms.query_collins_dictionary_synonym('mother')
synonym_02 = synonyms.query_synonym_com('mother')
synonym_03 = synonyms.query_thesaurus_com('mother')
synonym_04 = synonyms.query_thesaurus_plus('mother')
synonym_results = sorted(set([y for x in [synonym_01, synonym_02, synonym_03, synonym_04] for y in x]))
print(synonym_results)
['ancestor', 'antecedent', 'architect', 'author', 'begetter', 'beginning', 'child-bearer', 'creator', 'dam', 'female parent', 'forebearer', 'forefather', 'foster mother', 'founder', 'fount', 'fountain', 'fountainhead', 'genesis', 'inspiration', 'inventor', 'lady', 'ma', 'maker', 'mam', 'mama', 'mamma', 'mammy', 'mater', 'materfamilias', 'matriarch', 'mom', 'momma', 'mommy', 'mother-in-law', 'mum', 'mummy', 'nurse', 'old lady', 'old woman', 'origin', 'originator', 'para I', 'parent', 'predecessor', 'primipara', 'procreator', 'producer', 'progenitor', 'provenience', 'puerpera', 'quadripara', 'quintipara', 'sire', 'source', 'spring', 'start', 'stimulus', 'supermom', 'surrogate mother', 'wellspring']
```

## Synonyms - single source written to Python dictionary
```python
from wordhoard import synonyms

list_of_words = ['mother', 'daughter', 'father', 'son']

synonyms_results = {}

for word in list_of_words:
    results = synonyms.query_synonym_com(word)
    synonyms_results[word] = results

for key, value in synonyms_results.items():
    print(key, value)
    mother ['female parent', 'ma', 'mama', 'mamma', 'mammy', 'mater', 'mom', 'momma', 'mommy', 'mother-in-law', 'mum', 'mummy', 'para I', 'parent', 'primipara', 'puerpera', 'quadripara', 'quintipara', 'supermom', 'surrogate mother']
    daughter ['female offspring', 'girl', "mother's daughter"]
    father ['begetter', 'dad', 'dada', 'daddy', 'father-in-law', 'male parent', 'old man', 'pa', 'papa', 'pappa', 'parent', 'pater', 'pop']
    son ['Jnr', 'Jr', 'Junior', 'boy', 'male offspring', "mama's boy", "mamma's boy", 'man-child', "mother's boy"]
```

# Basic Usage Definitions

## Definition -  single source

```python
from wordhoard import dictionary

results = dictionary.query_synonym_com('mother')
print(results)
['a woman who has given birth to a child (also used as a term of address to your mother)']
```

## Definition - multiple sources

```python
from wordhoard import dictionary

definition_01 = dictionary.query_collins_dictionary_synonym('mother')
definition_02 =  dictionary.query_synonym_com('mother')
definition_03 = dictionary.query_thesaurus_com('mother')
definition_results = [y for y in [definition_01, definition_02, definition_03]]
print(definition_results)
["a person's own mother", 'a woman who has given birth to a child (also used as a term of address to your mother)', 'female person who has borne children']
```

# Advanced Usage Synonyms
<p align="justify">
A more advanced example is provided in the example script 
<a href="https://github.com/johnbumgarner/wordhoard/blob/master/examples/nlp_synonym_use_case.py">nlp synonym use case</a>.
</p>

# Additional Features
<p align="justify">
<i>wordhoard</i> uses an in-memory dictionary cache, which helps prevent redundant queries to an individual resource for the same word.  This application also uses <i>Python logging</i> to both the terminal and to the logfile <i>wordhoard_error.yaml</i>.
<p>

# Sources

<p align="justify">
This package is designed to query these online sources for antonyms, synonyms and definitions:

1. collinsdictionary.com
2. wordnet.princeton.edu
3. synonym.com
4. thesaurus.com
5. thesaurus.plus
<p>
  
# Dependencies

<p align="justify">
This package has these dependencies:
  
1. <b>BeautifulSoup</b>
2. <b>lxml</b>
3. <b>requests</b>
4. <b>urllib3</b>
<p>

# License
<p align="justify">
The MIT License (MIT). Please see <a href="https://github.com/johnbumgarner/wordhoard/blob/main/LICENSE">License File</a> for more information.
<p>

