
<p align="center">
   <! -- Graphic source: https://thesaurus.plus --> 
  <img src="https://github.com/johnbumgarner/wordhoard/blob/master/graphic/wordhoard_graphic.jpg"/>
</p>

# Overviews

![PyPI](https://img.shields.io/pypi/v/wordhoard) &nbsp;
![License: MIT](https://img.shields.io/github/license/johnbumgarner/wordhoard)&nbsp;
![GitHub issues](https://img.shields.io/github/issues/johnbumgarner/wordhoard)&nbsp;
![GitHub pull requests](https://img.shields.io/github/issues-pr/johnbumgarner/wordhoard)&nbsp;
[![wordhoard](https://snyk.io/advisor/python/wordhoard/badge.svg)](https://snyk.io/advisor/python/wordhoard)&nbsp;
![PyPI - Downloads](https://img.shields.io/pypi/dm/wordhoard)&nbsp;

<p align="justify">
The Oxford Dictionary defines <i>wordhoard</i> as a supply of words or a lexicon. <i>Wordhoard</i> is a <b>Python 3 module </b> that can be used to obtain antonyms, synonyms, hypernyms, hyponyms, homophones and definitions for words in the English language. 
  
This <i>Python</i> package was spawned from a <a href="https://stackoverflow.com/questions/63705803/merge-related-words-in-nlp/63771196#63771196">Stack Overflow</a> bountied question.  That question forced me to look into the best practices for obtaining a comprehensive lists of synonyms for a given word.  During my research, I developed the repository <a href="https://github.com/johnbumgarner/synonyms_discovery_aggregation">synonym discovery and aggregation</a> and decided to create <i>wordhoard</i>.
<p>
   
# Primary Use Case
<p align="justify"> 
Textual analysis is a broad term for various research methodologies used to qualitatively describe, interpret and understand text data. These methodologies are mainly used in academic research to analyze content related to media and communication studies, popular culture, sociology, and philosophy. Textual analysis allows these researchers to quickly obtain relevant insights from unstructured data. All types of information can be gleaned from textual data, especially from social media posts or news articles. Some of this information includes the overall concept of the subtext, symbolism within the text, assumptions being made and potential relative value to a subject (e.g. data science). In some cases it is possible to deduce the relative historical and cultural context of a body of text using analysis techniques coupled with knowledge from different disciplines, like linguistics and semiotics.
   
Word frequency is the technique used in textual analysis to measure the frequency of a specific word or word grouping within unstructured data. Measuring the number of word occurrences in a corpus allows a researcher to garner interesting insights about the text. A subset of word frequency is the correlation between a given word and that word's relationship to either antonyms and synonyms within the specific corpus being analyzed. Knowing these relationships is critical to improving word frequencies and topic modeling.

<i>Wordhoard</i> was designed to assist researchers performing textual analysis to build more comprehensive lists of antonyms, synonyms, hypernyms, hyponyms and homophones.
</p>

# Installation

<p align="justify"> 
   Install the distribution via pip:
</p>

```python
pip3 install wordhoard
```

# Antonyms Module Usage

<p align="justify"> 
  An <i>antonym</i> is word that has the exact opposite meaning of another word or its antonym.

Antonym examples:

- bad and good
- fast and slow
- stop and go
</p>

```python
from wordhoard import Antonyms

antonym = Antonyms('mother')
antonym_results = antonym.find_antonyms()
print(antonym_results)
['dad', 'daddy', 'father', 'old man', 'pa', 'papa', 'pop', 'poppa']
```

## Antonyms written to Python dictionary
```python
from wordhoard import Antonyms

antonyms_results = {}
list_of_words = ['mother', 'daughter', 'father', 'son']

for word in list_of_words:
    antonym = Antonyms(word)
    results = antonym.find_antonyms()
    antonyms_results[word] = results

for key, value in antonyms_results.items():
    print(key, value)
    
    mother['dad', 'daddy', 'father', 'old man', 'pa', 'papa', 'pop', 'poppa']

    daughter['son']

    father['biological mother', 'birth mother', 'ma', 'mama', 'mom', 'momma', 'mommy', 'mother', 'mum', 'mummy', 
    'progenitress', 'progenitrix']

    son['daughter']
```


# Synonyms Module Usage

<p align="justify">
 A <i>synonym</i> is a word or phrase that means exactly or nearly the same as another word or phrase in the same language.

Synonym examples:
- happy, joyful, elated, cheerful
- bad, evil, rotten, corrupt  
- cold, chilly, freezing, frosty
</p>

```python
from wordhoard import Synonyms

synonym = Synonyms('mother')
synonym_results = synonym.find_synonyms()
print(synonym_results)
['ancestor', 'biological mother', 'birth mother', 'child-bearer', 'creator', 'dam', 'female parent', 
'forebearer', 'foster mother', 'ma', 'mama', 'mamma', 'mammy', 'mater', 'mom', 'momma', 'mommy', 
'mother-in-law', 'mum', 'mummy', 'old lady', 'old woman', 'origin', 'para i', 'parent', 'predecessor', 
'primipara', 'procreator', 'progenitor', 'puerpera', 'quadripara', 'quintipara', 'source', 'supermom', 
'surrogate mother']
```

## Synonyms written to Python dictionary

```python
from wordhoard import Synonyms

synonyms_results = {}
list_of_words = ['mother', 'daughter', 'father', 'son']

for word in list_of_words:
    synonym = Synonyms(word)
    results = synonym.find_synonyms()
    synonyms_results[word] = results

for key, value in synonyms_results.items():
    print(key, value)
    
    mother['ancestor', 'biological mother', 'birth mother', 'child-bearer', 'creator', 'dam', 'female parent', 
    'forebearer', 'foster mother', 'ma', 'mama', 'mamma', 'mammy', 'mater', 'mom', 'momma', 'mommy', 
    'mother-in-law', 'mum', 'mummy', 'old lady', 'old woman', 'origin', 'para i', 'parent', 'predecessor', 
    'primipara', 'procreator', 'progenitor', 'puerpera', 'quadripara', 'quintipara', 'source', 'supermom', 
    'surrogate mother']

    daughter['female child', 'female offspring', 'girl', 'lass', "mother's daughter", 'offspring', 'woman']
    
    father['ancestor', 'begetter', 'beginner', 'biological father', 'birth father', 'church father', 'dad', 
    'dada', 'daddy', 'don', 'father of the church', 'father-god', 'father-in-law', 'fatherhood', 'forebearer', 
    'forefather', 'foster father', 'founder', 'founding father', 'governor', 'male parent', 'old boy', 'old man', 
    'origin', 'pa', 'padre', 'papa', 'pappa', 'parent', 'pater', 'paterfamilias', 'patriarch', 'pop', 'poppa', 
    'predecessor', 'procreator', 'progenitor', 'sire', 'source']

    son['boy', 'dependent', 'descendant', 'heir', 'jnr', 'jr', 'junior', 'lad', 'logos', 'male child', 
    'male offspring', "mama's boy", "mamma's boy", "mother's boy", 'offspring', 'scion', 'son and heir']
```

# Hypernyms Module Usage

<p align="justify">

Hypernym: (semantics) A word or phrase whose referents form a set including as a subset the referents of a subordinate term.
Musical instrument is a hypernym of "guitar" because a guitar is a musical instrument.

 A <i>hypernym</i> is a word with a broad meaning that more specific words fall under.
Other names for hypernym include umbrella term and blanket term.

Hypernym examples:
- diamond is a hypernym of gem
- eagle is a hypernym of bird 
- red is a hypernym of color
</p>

```python
from wordhoard import Hypernyms

hypernym = Hypernyms('red')
hypernym_results = hypernym.find_hypernyms()
print(hypernym_results)
['amount', 'amount of money', 'card games', 'chromatic color', 'chromatic colour', 'color', 
 'colour', 'cooking', 'geographical name', 'hair', 'hair color', 'lake', 'person', 'radical', 
 'rainbow', 'river', 'spectral color', 'spectral colour', 'sum', 'sum of money']
```

# Hyponyms Module Usage

<p align="justify">
A <i>hyponym</i> is a word of more specific meaning than a general or superordinate term applicable to it.

Hyponym examples:
- horse is a hyponym of animal
- table is a hyponym of furniture
- maple is a hyponym of tree

</p>

```python
from wordhoard import Hyponyms

hyponym = Hyponyms('horse')
hyponym_results = hyponym.find_hyponyms()
print(hyponym_results)
['american saddlebred', 'andalusian horse', 'arabian horse', 'azteca horse', 'barb horse', 'belgian horse',
 'belgian warmblood', 'clydesdale horse', 'coldblood trotter', 'curly horse', 'dutch warmblood', 'ethiopian horses',
 'falabella', 'fjord horse', 'friesian horse', 'gypsy horse', 'lusitano', "przewalski's horse", 'shire horse',
 'wild horse']
```

# Homophones Module Usage

<p align="justify">
A <i>homophone</i> is a word that is pronounced the same as another word but differs in meaning.

Homophone examples:
- one is a homophone of won
- ate is a homophone of eight
- meet is a homophone of meat
   
</p>

```python
from wordhoard import Homophones

homophone = Homophones('horse')
homophone_results = homophone.find_homophones()
print(homophone_results)
['horse is a homophone of hoarse']
```

# Definitions Module Usage

<p align="justify">
A <i>definition</i> is a statement of the exact meaning of a word, especially in a dictionary.
</p>

```python
from wordhoard import Definitions

definition = Definitions('mother')
definition_results = definition.find_definitions()
print(definition_results)
["a person's own mother", 'a woman who has given birth to a child (also used as a term of address to your mother)',
 'female person who has borne children']
```

# Advanced Usage 

<p align="justify">
One of the <a href="https://github.com/johnbumgarner/wordhoard/blob/master/examples/nlp_synonym_use_case.py">example scripts</a> uses the <a href="https://pypi.org/project/nltk/">Natural Language Toolkit (NLTK)</a> to parse a block of text.
Part of the parsing process includes removing punctuation and numeral characters for the text.  It also includes removed English language stop words.  After the text has been cleaned the script looks for synonyms for each word. 
</p>

# Language Translation
<p align="justify">
The majority of the sources that <i>wordhoard</i> queries are primarily in the English language. To find antonyms, synonyms, hypernyms, hyponyms and homophones for other languages <i>wordhoard</i> uses the Python package <a href="https://github.com/nidhaloff/deep-translator">deep-translator.</a>

One of the many translators embedded in `deep-translator` is `GoogleTranslator.` Some of these other translators, such as `MicrosoftTranslator` require an API key.
You can obtain a list of supported languages by querying `get_supported_languages().`  As of July 5, 2021, there were 107 languages supported by `GoogleTranslator`
</p>

```python
from deep_translator import GoogleTranslator

langs_dict = GoogleTranslator.get_supported_languages(as_dict=True)
for lang_name, lang_abbreviation in langs_dict.items():
    print(f'{lang_name}: {lang_abbreviation}')
```

The example below uses `GoogleTranslator` to translate Spanish language words to English language ones.  The translated words are processed using `Synonyms.find_synonyms()` and the English results are retranslated back to Spanish.

```python
from wordhoard import Synonyms
from deep_translator import GoogleTranslator

list_of_words = ['madre', 'hija', 'padre', 'hiño']
synonyms_results = {}

for word in list_of_words:
    translated_word = GoogleTranslator(source='spanish', target='english').translate(word)
    synonym = Synonyms(translated_word.lower())
    results = synonym.find_synonyms()
    synonyms_results[word] = results

for key, values in synonyms_results.items():
    translated_synonyms = {}
    unique_values = set()
    # The languages keywords can be either the:
    # Full word: spanish
    # or the abbreviation: es
    translated_synonyms.setdefault(key, [])
    for value in sorted(set(values)):
        translated_value = GoogleTranslator(source='english', target='spanish').translate(value)
        unique_values.add(translated_value.lower())
    translated_synonyms[key].append(sorted(unique_values))
    print(translated_synonyms)
    
   {'madre': [['anciana', 'antepasado', 'creador', 'fuente', 'madre', 'madre adoptiva', 'madre biológica', 
   'madre sustituta', 'mami', 'mamita', 'mamá', 'mater', 'momia', 'origen', 'padre', 'para yo', 
   'portador de hijos', 'predecesor', 'primípara', 'procreador', 'progenitor', 'puerpera', 
   'quadripara', 'quintipara', 'represa', 'señora mayor', 'suegra', 'súper mamá']]}
   
   {'hija': [['descendencia', 'descendencia femenina', 'hija de la madre', 'muchacha', 'mujer', 'niña']]}

   {'padre': [['anciano', 'chico mayor', 'dada', 'engendrador', 'música pop', 'padrastro', 'padre', 
   'padre adoptivo', 'padre biológico', 'papito', 'pappa', 'papá', 'paterfamilias', 'patriarca', 
   'pensilvania']]}

   {'hiño': [['chico', 'dependiente', 'descendencia', 'descendencia masculina', 'descendiente', 
   'el hijo de mamá', 'el niño de mama', 'heredero', 'hijo de la madre', 'hijo y heredero', 'jnr', 
   'jr', 'júnior', 'logotipos', 'muchacho', 'niño', 'palabra', 'vástago']]}

```

<p align="justify">
It is worth noting that Google Translate is not perfect, thus it can make “lost in translation” translation mistakes. These mistakes are usually related to Google Translate not having an in-depth understanding of the language or not being able to under the context of these words being translated.  In some cases Google Translate will make nonsensical literal translations.  So any translation should be reviewed for these mistakes. 
</p>

# Additional Features
   
<p align="justify">
<i>wordhoard</i> uses an in-memory cache, which helps prevent redundant queries to an individual resource for the same word.  These caches are currently being erased after each session. 
   
This application also uses <i>Python logging</i> to both the terminal and to the logfile <i>wordhoard_error.yaml</i>.
</p>

# Sources

<p align="justify">
This package is designed to query these online sources for antonyms, synonyms, hypernyms, hyponyms and definitions:

1. classicthesaurus.com
2. collinsdictionary.com
3. merriam-webster.com
4. synonym.com
5. thesaurus.com
6. wordhippo.com
7. wordnet.princeton.edu
</p>
  
# Dependencies

<p align="justify">
This package has these dependencies:
  
1. <b>BeautifulSoup</b>
2. <b>deep-translator</b>
3. <b>lxml</b>
4. <b>requests</b>
5. <b>urllib3</b>
</p>

# Development

<p align="justify">
If you would like to contribute to the <i>wordhoard</i> project please read the <a href="https://github.com/johnbumgarner/wordhoard/blob/master/CONTRIBUTING.md">contributing guidelines</a>.
   
Items currently under development:
   - Rate limiting related to `Python Requests`
   - English language word verification using the Python package `pyenchant` 
   - Embedded translations using the Python package `deep-translator`
   - Selectable query output - list or dictionary format
   - Expanding the list of hypernyms, hyponyms and homophones
   - Adding part-of-speech filters in queries 
</p>

# Issues

<p align="justify">
This repository is actively maintained.  Feel free to open any issues related to bugs, coding errors, broken links or enhancements. 

You can also contact me at [John Bumgarner](mailto:wordhoardproject@gmail.com?subject=[GitHub]%20wordhoard%20project%20request) with any issues or enhancement requests.
</p>

# Limitations
   
<p align="justify">
   
The querying capabilities of this Python package is highly dependent on the navigational structure of each source in the query pool.  If a source modifies its navigational structure then extraction from that specific source will likely have some challenges. The maintainers of `Wordhoard` will correct these navigational extraction issues when they are discovered in periodic testing or reported as an issue.    

Another package limitation is the accuracy of certain antonyms or synonyms provided by a source. For instance 
<a href="https://www.wordhippo.com/">WordHippo</a> (a source still under evaluation) provides an overabundance of synonyms for a given word.  In most cases the words provided have almost no relationship to the word inputted. 
   
For example:  
</p>

```python
from wordhoard import Synonyms

synonym = Synonyms('banana')
results = synonym.query_wordhippo() # debugging source
print(results)
['actor', 'buffoon', 'card', 'clown', 'comedian', 'comic', 'cutup', 'droll', 'farceur', 'fool', 'funster', 'gagster', 
'humorist', 'jester', 'jokesmith', 'jokester', 'jook-sing', 'josher', 'kidder', 'life of the party', 'prankster', 
'punster', 'quipster', 'second banana', 'stand-up comic', 'stooge', 'straight person', 'top banana', 'trickster', 
'twinkie', 'wag', 'wisecracker', 'wit']

```

<p align="justify">
   
It is hard for an application like `Wordhoard` to intuitively extract the words, which are actually synonyms from the `WordHippo` results.  To counter this `WordHippo` was removed for the `Synonyms` module. 
 
Additionally, some sources provide _near antonyms_ or _near synonyms_ for a specific word.  The maintainers of `Wordhoard` have made a best effort to remove these types of erroneous responses from the output of any given query.
   
Some sources have ratelimits, which can impact querying and extraction for that source. In some cases exceeding these ratelimits will trigger a `Cloudflare` challenge session.  Errors related to these blocked sessions are written the `wordhoard_error.yaml` file.  Such entries can have a `status code` of 521, which is a Cloudflare-specific error message. The maintainers of `Wordhoard` are exploring adding ratelimits to those sources that impose querying limits for a specific period.
</p>

# Sponsorship
   
Under consideration at the moment. 

# License

<p align="justify">
The MIT License (MIT).  Please see <a href="https://github.com/johnbumgarner/wordhoard/blob/main/LICENSE">License File</a> for more information.
</p>

