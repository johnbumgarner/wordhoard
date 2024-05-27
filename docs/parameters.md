<h1 style="color:IndianRed;"> <strong>Parameters</strong> </h1>

---

<h3 style="color:IndianRed;"> Default Parameters </h3>

<p align="justify"> 
Most of the modules within <strong>WordHoard</strong> have several parameters that are configurable.  
</p>

<p align="justify"> 
The default parameters in the <i>Antonyms</i>, <i>Definitions</i>, <i>Hypernyms</i>, <i>Hyponyms</i> and <i>Synonyms</i> modules are.
</p>

```python
from wordhoard import Synonyms

synonym = Synonyms(search_string='',
                   output_format='list',
                   max_number_of_requests=30,
                   rate_limit_timeout_period=60,
                   user_agent=None,
                   proxies=None)
```

<ul>

<li><strong>search_string:</strong>
	<ul>
		<li>type: string</li> 
		<li>String containing the variable to search for</li>  
</ul>
</li>


<li><strong>output_format:</strong>
	<ul>
		<li>type: string</li> 
		<li>String containing the requested output format</li>  
		<li>Acceptable values: dictionary, list and json</li> 
</ul>
</li>

<li><strong>max_number_of_requests:</strong>
	<ul>
		<li>type: int</li> 
		<li>Maximum number of requests for a specific timeout_period, which is defined in the variable rate_limit_timeout_period</li>
		<li>default value: 30</li> 
</ul>
</li>

<li><strong>rate_limit_timeout_period:</strong>
	<ul>
		<li>type: int</li> 
		<li>The time period in seconds before a session is placed in a temporary hibernation mode</li> 
		<li>default value: 60</li> 
</ul>
</li>

<ul>
    <li><strong>user_agent:</strong>
	    <ul>
		    <li>type: string</li> 
		    <li>default value: None</li> 
        </ul>
    </li>
</ul>

<li><strong>proxies:</strong>
	<ul>
		<li>type: dictionary</li> 
		<li>Dictionary of proxies to use with Python Requests</li> 
		<li>default value: None</li> 
    </ul>
</li>

</ul>

<h3 style="color:IndianRed;"> Source Parameters </h3>

<p align="justify"> 
The modules <i>Antonyms</i>, <i>Definitions</i> and <i>Synonyms</i> also have a <i>sources</i> parameters. This parameter
can be modified to restrict the sources being queried.
</p>

<ul>
<li>Antonyms</li>
    <ul>
        <li> sources = ['google', 'thesaurus.com', 'wordhippo'] </li>
    </ul>

<li>Definitions</li>
    <ul>
        <li> sources = ['collins', 'merriam-webster', 'synonym.com', 'thesaurus.com'] </li>
    </ul>

<li>Synonyms</li>
    <ul>
        <li> sources = ['collins', 'merriam-webster', 'synonym.com', 'thesaurus.com', 'wordnet'] </li>
    </ul>
</ul>

<p align="justify"> 
This <i>sources</i> parameter can be modified to restrict the sources being queried. For instance the example below
removes Collins Dictionary as a search source when querying for Synonyms for the word mother.
</p>

```python
from wordhoard import Synonyms

synonym = Synonyms(search_string='mother',
                   output_format='list',
                   sources = ['merriam-webster', 'synonym.com', 'thesaurus.com', 'wordnet'],
                   max_number_of_requests=30,
                   rate_limit_timeout_period=60,
                   user_agent=None,
                   proxies=None)
```