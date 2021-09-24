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

# General Package Utilization

## Antonyms Module Usage

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


## Synonyms Module Usage

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

## Hypernyms Module Usage

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

## Hyponyms Module Usage

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

## Homophones Module Usage

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

## Definitions Module Usage

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

## Language Translation

<p align="justify">
The majority of the sources that <i>wordhoard</i> queries are primarily in the English language. To find antonyms, synonyms, hypernyms, hyponyms and homophones for other languages <i>wordhoard</i> has 3 translation service modules. These modules support <a href="https://translate.google.com">Google Translate</a>, <a href="https://www.deepl.com/translator">DeepL Translate</a> and <a href="https://mymemory.translated.net">MyMemory Translate.</a> 

<p align="justify">
The example below uses the <i>Google Translate</i> module within <i>wordhoard</i> to translate Spanish language words to English language and then back into Spanish.
</p>

```python
from wordhoard import Antonyms
from wordhoard.utilities.google_translator import Translator

words = ['buena', 'contenta', 'suave']
for word in words:
    translated_word = Translator(source_language='es', str_to_translate=word).translate_word()
    antonyms = Antonyms(translated_word).find_antonyms()
    reverse_translations = []
    for antonym in antonyms:
        reverse_translated_word = Translator(source_language='es', str_to_translate=antonym).reverse_translate()
        reverse_translations.append(reverse_translated_word)
    output_dict = {word: sorted(reverse_translations)}
    print(output_dict)
   {'buena': ['Dios espantoso', 'OK', 'abominable', 'aborrecible', 'acogedor', 'agravante', 'amenazante', 
   'angustioso', 'antiestético', 'asqueroso', 'basura', 'carente', 'contaminado', 'de segunda', 'decepcionante', 
   'defectuoso', 'deficiente', 'deplorable', 'deprimente', 'desagradable', 'desaliñado', 'descorazonador', 
   'desfavorecido', 'desgarbado', 'desgarrador', 'detestable', 'doloroso', 'duro', 'débil', 'enfermo', 
   'enfureciendo', 'enloquecedor', 'espantoso', 'esperado', 'exasperante', 'falsificado', 'falso', 'falta', 
   'falto', 'feo', 'frustrante', 'grotesco', 'horrible', 'hostil', 'impactante', 'imperfecto', 'inaceptable', 
   'inadecuado', 'inadmisible', 'inaguantable', 'incensar', 'incompetente', 'incongruente', 'inconsecuente', 
   'incorrecto', 'indeseable', 'indignante', 'indigno', 'indigno de', 'infeliz', 'inferior', 'infernal', 'inflamando', 
   'inmoral', 'insalubre', 'insatisfactorio', 'insignificante', 'insoportable', 'insuficiente', 'insufrible', 
   'intimidante', 'inútil', 'irreal', 'irritante', 'lamentable', 'lúgubre', 'maldad', 'malo', 'malvado', 'malísimo', 
   'mediocre', 'menor', 'miserable', 'molesto', 'nauseabundo', 'no a la par', 'no atractivo', 'no capacitado', 
   'no es bueno', 'no es suficiente', 'no fidedigno', 'no satisfactorio', 'nocivo', 'objetable', 'odioso', 'ofensiva', 
   'ordinario', 'pacotilla', 'patético', 'pecaminoso', 'perturbador', 'pobre', 'poco agraciado', 'poco apetecible', 
   'poco hermoso', 'poco imponente', 'poco satisfactorio', 'poco virtuoso', 'podrido', 'portarse mal', 'preocupante', 
   'repelente', 'repugnante', 'repulsivo', 'sencillo', 'significar', 'sin forma', 'sin importancia', 'sin placer', 
   'sin valor', 'sombrío', 'subóptimo', 'sucio', 'terrible', 'triste', 'trágico', 'vicioso', 'vil']}
   
    truncated....
```

<p align="justify">
The example below uses the <i>Deep Translate</i> module within <i>wordhoard</i> to translate Spanish language words to English language and then back into Spanish.
</p>

```python
from wordhoard import Antonyms
from wordhoard.utilities.deep_translator import Translator

words = ['buena', 'contenta', 'suave']
for word in words:
    translated_word = Translator(source_language='es', str_to_translate=word,
                                 api_key='your_api_key').translate_word()
    antonyms = Antonyms(translated_word).find_antonyms()
    reverse_translations = []
    for antonym in antonyms:
        reverse_translated_word = Translator(source_language='es', str_to_translate=antonym,
                                             api_key='your_api_key').reverse_translate()
        reverse_translations.append(reverse_translated_word)
    output_dict = {word: sorted(set(reverse_translations))}
    print(output_dict)
    {'buena': ['abominable', 'agravante', 'angustia', 'antiestético', 'antipático', 'asqueroso', 'basura', 'casero', 
    'contaminado', 'crummy', 'de mala calidad', 'de segunda categoría', 'decepcionante', 'defectuoso', 'deficiente', 
    'deplorable', 'deprimente', 'desagradable', 'descorazonador', 'desgarrador', 'detestable', 'dios-horrible', 
    'doloroso', 'duro', 'débil', 'en llamas', 'enfermo', 'enfureciendo a', 'enloquecedor', 'equivocada', 'espantoso', 
    'esperado', 'exasperante', 'falso', 'falta', 'feo', 'forjado', 'frumpish', 'frumpy', 'frustrante', 'grotesco', 
    'horrible', 'hostil', 'impactante', 'imperfecto', 'impermisible', 'inaceptable', 'inadecuado', 'inadmisible', 
    'incandescente', 'incompetente', 'incongruente', 'indeseable', 'indignante', 'indigno', 'infeliz', 'inferior', 
    'infernal', 'inflamando', 'inmoral', 'inquietante', 'insalubre', 'insatisfactorio', 'insignificante', 'insoportable', 
    'insostenible', 'insuficiente', 'insufrible', 'intimidante', 'intrascendente', 'irreal', 'irritante', 'lamentable', 
    'llano', 'lúgubre', 'mal', 'mal favorecido', 'malvado', 'media', 'mediocre', 'menor', 'miserable', 'molestos', 
    'nauseabundo', 'no apto', 'no cualificado', 'no es agradable', 'no es bienvenido', 'no es bueno', 
    'no es lo suficientemente bueno', 'no es sano', 'no está a la altura', 'no hay que olvidar que', 'no se puede confiar en', 
    'nocivo', 'objetable', 'odioso', 'ofensiva', 'ok', 'ordinario', 'patético', 'pecaminoso', 'perturbando', 'pobre', 
    'poco apetecible', 'poco atractivo', 'poco encantador', 'poco imponente', 'poco útil', 'podrido', 'problemático', 
    'prohibiendo', 'pésimo', 'que molesta', 'queriendo', 'rankling', 'repelente', 'repugnante', 'repulsivo', 'rilando', 
    'se comportan mal', 'sin alegría', 'sin duda', 'sin forma', 'sin importancia', 'sin placer', 'sin pretensiones', 
    'sin sentido', 'sin valor', 'sombrío', 'subestándar', 'subóptima', 'terrible', 'triste', 'trágico', 'uncute', 'unvirtuoso', 
    'vicioso', 'vil', 'yukky']}
    
     truncated.... 
```
<p align="justify">
The example below uses the <i>MyMemory Translate</i> module within <i>wordhoard</i> to translate Spanish language words to English language and then back into Spanish.
</p>

```python
from wordhoard import Antonyms
from wordhoard.utilities.mymemory_translator import Translator

words = ['buena', 'contenta', 'suave']
for word in words:
    translated_word = Translator(source_language='es', str_to_translate=word,
                                 email_address='your_email_address').translate_word()
    antonyms = Antonyms(translated_word).find_antonyms()
    reverse_translations = []
    for antonym in antonyms:
        reverse_translated_word = Translator(source_language='es', str_to_translate=antonym,
                                             email_address='your_email_address').reverse_translate()
        reverse_translations.append(reverse_translated_word)
    output_dict = {word: sorted(set(reverse_translations))}
    print(output_dict)
    {'buena': ['abominable', 'aborrecible', 'aceptar', 'afligido', 'agravante', 'amenazante', 'ansia nauseosa', 
    'antiestético', 'asco', 'asqueroso', 'atroz', 'basura', 'caballo que padece tiro', 'carente', 'chocante', 
    'consternador', 'de baja calidad', 'decepcionando', 'defectuoso', 'deficiente', 'deprimentes', 'desagradable', 
    'desaliñado', 'descorazonador', 'desfavorecido', 'desgarbado', 'desgarrador', 'desgraciado', 'detestable', 
    'dios espantoso', 'doloroso', 'duelo psicológico', 'débil', 'enfermas', 'enfermo', 'enfureciendo', 'enloquecedor', 
    'es lo suficientemente buena', 'espantoso', 'esperado', 'está por el suelo', 'exasperante', 'fake', 'familiar', 
    'feo', 'forjado', 'fúnebre', 'grutesco', 'horrible', 'hostil', 'impropio', 'inaceptable', 'inadecuado', 'inadmisible', 
    'inaguantable', 'incensar', 'incomible', 'incompetente', 'incongruente', 'indeseable', 'indignante', 'indigno', 
    'inexperto', 'infeliz', 'inferior', 'infernal', 'inflamando', 'inmoral', 'inquietante', 'insatisfactorio', 'insignificante', 
    'insoportable', 'insuficientes', 'insufrible', 'insípido', 'intimidante', 'intrascendente', 'irreal', 'irritante', 
    'lamentable', 'lúgubre', 'mal', 'mal acogido', 'malo', 'media', 'mezquino', 'molesto', 'nauseabundo', 'no es bueno', 
    'no satisfactorio', 'no útil', 'nocivo', 'o antipatico', 'odioso', 'ofensivo', 'parcialmente podrido', 'patético', 
    'pecador', 'penoso', 'pequeños', 'perturbador', 'piojoso', 'poco agraciado', 'poco apetecible', 'poco atractivo', 
    'poco fiable', 'poco hermoso', 'poco imponente', 'poco satisfactorio', 'poco virtuoso', 'podrido', 'portarse mal', 
    'preocupante', 'pretérito imperfecto', 'puede ser frustrante', 'querer', 'repelente', 'repugnante', 'repulsivo', 
    'residuos de lana', 'riling', 'ser agrupado con', 'simple', 'sin forma', 'sin importancia', 'sin placer', 'sin valor', 
    'sombría', 'subóptimo', 'sucio', 'tarifa segunda', 'temperatura', 'terrible', 'triste', 'trágico', 'tu bienvenida mi hermano', 
    'un error', 'vano', 'vicioso', 'vil', '¡horrible', 'áspero']}
    
      truncated.... 
```

<p align="justify">
It is worth noting that none of the translation services are perfect, thus it can make “lost in translation” translation mistakes. These mistakes are usually related to the translation service not having an in-depth understanding of the language or not being able to under the context of these words being translated.  In some cases there will be nonsensical literal translations.  So any translations should be reviewed for these common mistakes. 
</p>

## Natural Language Processing

<p align="justify">
One of the <a href="https://github.com/johnbumgarner/wordhoard/blob/master/examples/nlp_synonym_use_case.py">example scripts</a> uses the <a href="https://pypi.org/project/nltk/">Natural Language Toolkit (NLTK)</a> to parse a block of text.
Part of the parsing process includes removing punctuation and numeral characters for the text.  It also includes removing common English language stop words.  After the text has been cleaned the script looks for synonyms for each word (aka token).
</p>

# Additional Features

## In-memory cache
   
<p align="justify">
<i>wordhoard</i> uses an in-memory cache, which helps prevent redundant queries to an individual resource for the same word.  These caches are currently being erased after each session. 
</p>
   
## Rate limiting

<p align="justify">
Some sources have ratelimits, which can impact querying and extraction for that source. In some cases exceeding these ratelimits will trigger a `Cloudflare` challenge session.  Errors related to these blocked sessions are written the `wordhoard_error.yaml` file.  Such entries can have a `status code` of 521, which is a Cloudflare-specific error message. The maintainers of `Wordhoard` have added ratelimits to mutiple modules.  These ratelimits can be modified, but reducing these predefined limits can lead to querying sessions being dropped or blocked by a source.  

Currently there are 2 parameters that can be set:
   
- max_number_of_requests
- rate_limit_timeout_period
   
These parameters are currently set to 30 requests every 60 seconds.   Requests is a misnomer, because within the Synonyms module 150 queries will be made.  The reason here is that there are 5 sources, which will be called 30 times each in the 60 seconds timeout period.  
   
When a ratelimit is trigger a warning message is written to both the console and the `wordhoard_error.yaml` file.  The ratelimit will automatically reset after a set time period, which currently cannot be modified using a parameter passed in a `Class object`.  

</p>

```python 
from wordhoard import Synonyms
synonym = Synonyms(search_string='mother', max_number_of_requests=30, rate_limit_timeout_period=60)
results = synonym.find_synonyms()   
```

## Proxy usage 

<p align="justify">
<i>Wordhoard</i> provides out of the box usage of proxies. Just define your proxies config as a dictionary and pass it to the corresponding module as shown below.
</p>

```python 
from wordhoard import Synonyms
proxies_example = {
    "http": "your http proxy if available" # example: http://149.28.94.152:8080
    "https": "your https proxy"  # example: https://128.230.60.178:3128
}

synonym = Synonyms(search_string='mother', proxies=proxies_example)
results = synonym.find_synonyms()  
```
<p align="justify">
There is a known bug in <i>urllib3</i> between versions 1.26.0 and 1.26.7, which will raise different errors. <i>Wordhoard</i> will be using <i>urllib3</i> version 1.25.11 until the bug is fixed in a future release.  
</p>

## Output Formatting

<p align="justify">
The default output of <i>wordhoard</i> is a <i>Python</i> List.  The output format can be changed to use a <i>Python</i> dictionary.  The code example below shows how to change the formatting.  
</p>

```python
from wordhoard import Antonyms

words = ['good', 'bad', 'happy']
for word in words:
    antonym_dict = Antonyms(search_string=word, output_format='dictionary').find_antonyms()
    print(antonym_dict)
    {'good': ['detestable', 'evil', 'fake', 'forged', 'immoral', 'inadequate', 'incompetent', 'inconsequential',
              'inconsiderable', 'mean', 'misbehaving', 'noxious', 'rotten', 'sinful', 'tainted', 'unpleasant', 'unreal',
              'unreliable', 'unskilled', 'unsuitable', 'unvirtuous', 'vicious', 'vile', 'wicked']}
    {'bad': ['advantageous', 'beneficial', 'benevolent', 'honest', 'just', 'profitable', 'reputable', 'right', 'true',
             'undecayed', 'upright', 'virtuous', 'worthy']}
    {'happy': ['discouraged', 'dissatisfied', 'forsaken', 'hopeless', 'morose', 'pained', 'unfortunate', 'unlucky']}

```


## Logging 
<p align="justify">
This application also uses <i>Python logging</i> to both the terminal and to the logfile <i>wordhoard_error.yaml</i>.  The maintainers of <i>Wordhoard</i> have attempted to catch any potential exception and write these error messages to the logfile. The logfile is useful to troubleshooting any issue with this package or with the sources being queried by `Wordhoard`.
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
This package has these core dependencies:
  
1. <b>backoff</b>
2. <b>BeautifulSoup</b>
3. <b>deckar01-ratelimit</b>
4. <b>deepl</b>
5. <b>lxml</b>
6. <b>requests</b>
7. <b>urllib3</b>
</p>


# Development

<p align="justify">
If you would like to contribute to the <i>Wordhoard</i> project please read the <a href="https://github.com/johnbumgarner/wordhoard/blob/master/CONTRIBUTING.md">contributing guidelines</a>.
   
Items currently under development:
   - English language word verification using the Python package `pyenchant` 
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
   
</p>

# Sponsorship
   
If you would like to contribute financially to the development and maintenance of the <i>Wordhoard</i> project please read the <a href="https://github.com/johnbumgarner/wordhoard/blob/master/SPONSOR.md">sponsorship information.</a>.

# License

<p align="justify">
The MIT License (MIT).  Please see <a href="https://github.com/johnbumgarner/wordhoard/blob/main/LICENSE">License File</a> for more information.
</p>

