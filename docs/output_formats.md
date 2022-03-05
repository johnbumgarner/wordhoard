<h1><strong>Output Formats</strong></h1>
---


### List Output

The default output of <strong>WordHoard</strong> is a <i>Python list</i>.  This output is set using the variable <i>output_format</i>, which by default is preset to <i>output_format='list'</i>.


```python
from wordhoard import Synonyms

word = 'mother'
results = Synonyms(search_string=word, output_format='list').find_synonyms()
print(results)
['ancestor', 'child-bearer', 'creator', 'female parent', 'forebearer', 'ma', 
'mama', 'mamma', 'mammy', 'mater', 'mom', 'momma', 'mommy', 'mother-in-law', 
'mum', 'mummy', 'old lady', 'origin', 'para i', 'parent', 'predecessor', 
'primipara', 'procreator', 'progenitor', 'puerpera', 'quadripara', 'quintipara', 
'source', 'supermom', 'surrogate mother']

```


### Dictionary Output

The data elements can also be outputted in a <i>Python dictionary</i>. This is accomplished by changing the 
<i>output_format</i> variable, to <i>output_format='dictionary'</i>.


```python
from wordhoard import Synonyms

word = 'mother'
results = Synonyms(search_string=word, output_format='dictionary').find_synonyms()
print(results)
{'mother': ['ancestor', 'child-bearer', 'creator', 'female parent', 'forebearer', 
'ma', 'mama', 'mamma', 'mammy', 'mater', 'mom', 'momma', 'mommy', 'mother-in-law', 
'mum', 'mummy', 'old lady', 'origin', 'para i', 'parent', 'predecessor', 
'primipara', 'procreator', 'progenitor', 'puerpera', 'quadripara', 'quintipara', 
'source', 'supermom', 'surrogate mother']}

```

### JSON Output

The data elements can also be outputted in JSON. This is accomplished by changing the <i>output_format</i>
variable, to <i>output_format='json'</i>.


```python
from wordhoard import Synonyms

word = 'mother'
results = Synonyms(search_string=word, output_format='json').find_synonyms()
print(results)
{
    "synonyms": {
        "mother": [
            "ancestor",
            "child-bearer",
            "creator",
            "female parent",
            "forebearer",
            "ma",
            "mama",
            "mamma",
            "mammy",
            "mater",
            "mom",
            "momma",
            "mommy",
            "mother-in-law",
            "mum",
            "mummy",
            "old lady",
            "origin",
            "para i",
            "parent",
            "predecessor",
            "primipara",
            "procreator",
            "progenitor",
            "puerpera",
            "quadripara",
            "quintipara",
            "source",
            "supermom",
            "surrogate mother"
        ]
    }
}
```
