<h1> <strong>Basic Usage</strong></h1>
---

<p align="justify"> 
<strong>WordHoard</strong> is a <i>Python 3</i> module that was designed using the rules of simplicity, which try to limit overly complex configuration requirements and keeps backend user intervention to the bare minimum.  
</p>


### Antonyms Module Usage

<p align="justify"> 
An <i>antonym</i> is word that has the exact opposite meaning of another word or its antonym.
</p>

<p align="justify"> 
Antonym examples:
</p>

<ul>
	<li>good and bad</li>
	<li>slow and fast</li>
	<li>stop and go</li>
</ul>


```python
from wordhoard import Antonyms

antonym = Antonyms(search_string='mother')
antonym_results = antonym.find_antonyms()
print(antonym_results)
['dad', 'daddy', 'father', 'old man', 'pa', 'papa', 'pop', 'poppa']
```

### Synonyms Module Usage

<p align="justify">
A <i>synonym</i> is a word or phrase that means exactly or nearly the same as another word or phrase in the same language.
</p>

<p align="justify"> 
Synonym examples:
</p>

<ul>
	<li>happy, joyful, elated, cheerful</li>
	<li>bad, evil, rotten, corrupt</li>  
	<li>cold, chilly, freezing, frosty</li>
</ul>


```python
from wordhoard import Synonyms

synonym = Synonyms(search_string='mother')
synonym_results = synonym.find_synonyms()
print(synonym_results)
['ancestor', 'biological mother', 'birth mother', 'child-bearer', 'creator', 
'dam', 'female parent', 'forebearer', 'foster mother', 'ma', 'mama', 'mamma', 
'mammy', 'mater', 'mom', 'momma', 'mommy', 'mother-in-law', 'mum', 'mummy', 
'old lady', 'old woman', 'origin', 'para i', 'parent', 'predecessor', 
'primipara', 'procreator', 'progenitor', 'puerpera', 'quadripara', 
'quintipara', 'source', 'supermom', 'surrogate mother']
```

### Definitions Module Usage

<p align="justify">
A <i>definition</i> is a statement of the exact meaning of a word, especially in a dictionary.
</p>

```python
from wordhoard import Definitions

definition = Definitions(search_string='mother')
definition_results = definition.find_definitions()
print(definition_results)
["a person's own mother", 'a woman who has given birth to a child (also used as a term of address to your mother)',
'female person who has borne children']
```

### Homophones Module Usage

<p align="justify">
A <i>homophone</i> is a word that is pronounced the same as another word but differs in meaning.
</p>

<p align="justify">
Homophone examples:
</p>

<ul>
	<li>one is a homophone of won</li>
	<li>ate is a homophone of eight</li>
	<li>meet is a homophone of meat</li>
</ul>


```python
from wordhoard import Homophones

homophone = Homophones(search_string='horse')
homophone_results = homophone.find_homophones()
print(homophone_results)
['horse is a homophone of hoarse']
```

### Hypernyms Module Usage

<p align="justify">
Hypernym: (semantics) A word or phrase whose referents form a set including as a subset the referents of a subordinate term. Musical instrument is a hypernym of "guitar" because a guitar is a musical instrument.
</p>

<p align="justify">
A <i>hypernym</i> is a word with a broad meaning that more specific words fall under.
Other names for hypernym include umbrella term and blanket term.
</p>

<p align="justify">
Hypernym examples:
</p>

<ul>
	<li>diamond is a hypernym of gem</li>
	<li>eagle is a hypernym of bird</li>
	<li>red is a hypernym of color</li>
</ul>

```python
from wordhoard import Hypernyms

hypernym = Hypernyms(search_string='red')
hypernym_results = hypernym.find_hypernyms()
print(hypernym_results)
['amount', 'amount of money', 'card games', 'chromatic color', 'chromatic colour', 
'color', 'colour', 'cooking', 'geographical name', 'hair', 'hair color', 'lake', 
'person', 'radical', 'rainbow', 'river', 'spectral color', 'spectral colour', 
'sum', 'sum of money']
```

### Hyponyms Module Usage

<p align="justify">
A <i>hyponym</i> is a word of more specific meaning than a general or superordinate term applicable to it.
</p>

<p align="justify">
Hyponym examples:
</p>

<ul>
	<li>horse is a hyponym of animal</li>
	<li>table is a hyponym of furniture</li>
	<li>maple is a hyponym of tree</li>
</ul>

```python
from wordhoard import Hyponyms

hyponym = Hyponyms(search_string='horse')
hyponym_results = hyponym.find_hyponyms()
print(hyponym_results)
['american saddlebred', 'andalusian horse', 'arabian horse', 'azteca horse', 
'barb horse', 'belgian horse','belgian warmblood', 'clydesdale horse', 
'coldblood trotter', 'curly horse', 'dutch warmblood', 'ethiopian horses',
'falabella', 'fjord horse', 'friesian horse', 'gypsy horse', 'lusitano',
"przewalski's horse", 'shire horse', 'wild horse']
```
