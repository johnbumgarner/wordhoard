<h1 style="color:IndianRed;"><strong>Limitations</strong></h1>

---

<p align="justify"> 
The querying capabilities of this Python package is highly dependent on the navigational structure of each source in the query pool.  If a source modifies its navigational structure then extraction from that specific source will likely have some challenges. The maintainers of <strong>WordHoard</strong> will correct these navigational extraction issues when they are discovered in periodic testing or reported as an issue.    
</p>

<p align="justify">
Another package limitation is the accuracy of certain antonyms or synonyms provided by a source. For instance 
<a href="https://www.wordhippo.com/">WordHippo</a> (a source still under evaluation) provides an overabundance of synonyms for a given word.  In most cases the words provided have almost no relationship to the word inputted. 
</p>  

<p align="justify">
For example:  
</p>

```python
from wordhoard import Synonyms

synonym = Synonyms('banana')
results = synonym.query_wordhippo() # debugging source
print(results)
['actor', 'buffoon', 'card', 'clown', 'comedian', 'comic', 'cutup', 'droll', 'farceur', 'fool', 'funster', 
'gagster', 'humorist', 'jester', 'jokesmith', 'jokester', 'jook-sing', 'josher', 'kidder', 'life of the party', 
'prankster', 'punster', 'quipster', 'second banana', 'stand-up comic', 'stooge', 'straight person', 'top banana', 
'trickster', 'twinkie', 'wag', 'wisecracker', 'wit']
```

<p align="justify">
It is hard for an application like <strong>WordHoard</strong> to intuitively extract the words, which are actually synonyms from the <i>WordHippo</i> results.  To counter this <i>WordHippo</i> was removed for the <i>Synonyms</i> module. 
</p>

<p align="justify">
Additionally, some sources provide <u>near antonyms</u> or <u>near synonyms</u> for a specific word.  The maintainers of <strong>WordHoard</strong> have made a best effort to remove these types of erroneous responses from the output of any given query.
</p>
