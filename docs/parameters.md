<h1> <strong>Parameters</strong> </h1>
---

<p align="justify"> 
Most of the modules within <strong>WordHoard</strong> have several parameters that are configurable.  
</p>

<p align="justify"> 
The default parameters in the <i>Antonyms</i>, <i>Synonyms</i> and <i>Definitions</i> modules are.
</p>

```python
from wordhoard import Synonyms
synonym = Synonyms(search_string='',
	               output_format='list',
                   max_number_of_requests=30,
                   rate_limit_timeout_period=60,
                   proxies=None
```


<p align="justify"> 
The default parameters in the <i>Hypernyms</i> and <i>Hyponyms</i> modules are.
</p>


```python
from wordhoard import Hypernyms
hypernyms = Hypernyms(search_string='',
                      max_number_of_requests=30,
                      rate_limit_timeout_period=60,
                      proxies=None
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
		<li>Acceptable values: list and dictionary</li> 
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


<li><strong>proxies:</strong>
	<ul>
		<li>type: dictionary</li> 
		<li>Dictionary of proxies to use with Python Requests</li> 
</ul>
</li>

</ul>
