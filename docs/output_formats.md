<h1><strong>Output Formats</strong></h1>
---


### List Output

<p align="justify"> 
The default output of <strong>WordHoard</strong> is a <i>Python list</i>.  This output is set using the variable <i>output_format</i>, which by default is preset to <i>output_format='list'</i>. All output is sorted by length.  
</p>

```python
from wordhoard import Synonyms

word = 'mother'
results = Synonyms(search_string=word, output_format='list').find_synonyms()
print(results)
['ma', 'mum', 'mom', 'dam', 'mama', 'mamma', 'mummy', 'momma', 'mommy', 
'mater', 'para i', 'parent', 'old lady', 'supermom', 'puerpera', 'primipara', 
'old woman', 'quadripara', 'quintipara', 'birth mother', 'foster mother', 
'female parent', 'mother-in-law', 'surrogate mother', 'biological mother']
```


### Dictionary Output

<p align="justify"> 
The data elements can also be outputted in a <i>Python dictionary</i>. This is accomplished by changing the 
<i>output_format</i> variable, to <i>output_format='dictionary'</i>.
</p>

```python
from wordhoard import Synonyms

word = 'mother'
results = Synonyms(search_string=word, output_format='dictionary').find_synonyms()
print(results)
{'mother': {'part_of_speech': 'noun', 'synonyms': ['ma', 'dam', 'mum', 'mom', 
'mama', 'mater', 'mummy', 'mamma', 'mommy', 'momma', 'parent', 'para i', 
'puerpera', 'old lady', 'supermom', 'old woman', 'primipara', 'quadripara', 
'quintipara', 'birth mother', 'foster mother', 'mother-in-law', 'female parent', 
'surrogate mother', 'biological mother']}}


```

### JSON Output

<p align="justify"> 
The data elements can also be outputted in JSON. This is accomplished by changing the <i>output_format</i>
variable, to <i>output_format='json'</i>.
</p>

```python
from wordhoard import Synonyms

word = 'mother'
results = Synonyms(search_string=word, output_format='json').find_synonyms()
print(results)
{
    "mother": {
        "part_of_speech": "noun",
        "synonyms": [
            "ma",
            "mom",
            "mum",
            "dam",
            "mama",
            "mommy",
            "mater",
            "mummy",
            "mamma",
            "momma",
            "parent",
            "para i",
            "puerpera",
            "supermom",
            "old lady",
            "primipara",
            "old woman",
            "quintipara",
            "quadripara",
            "birth mother",
            "female parent",
            "mother-in-law",
            "foster mother",
            "surrogate mother",
            "biological mother"
        ]
    }
}
```
