<h1><strong>Additional Features</strong></h1>
---

### In-memory cache
   
<p align="justify">
<strong>WordHoard</strong> uses an in-memory cache, which helps prevent redundant queries to an individual resource for the same word.  These caches are currently being erased after each session. 
</p>


### Logging 

<p align="justify">
This application also uses <i>Python</i> logging, which is written to the logfile <i>wordhoard_error.yaml</i>. The maintainers of <strong>WordHoard</strong> have attempted to catch any potential exception and write these error messages to that logfile. The logfile is useful in troubleshooting any issue with this package or with the sources being queried by <strong>WordHoard</strong>.
</p>


### Rate limiting

<p align="justify">
Some sources have rate limits, which can impact querying and parsing for that source. In some cases exceeding these rate limits will trigger a <i>Cloudflare</i> challenge session.  Errors related to these blocked sessions are written the <i>wordhoard_error.yaml</i> file.  Such entries can have either a <i>status code</i> of 521, which is a 
<i>Cloudflare-specific</i> message or a <i>status code</i> of 403. 
</p>

<p align="justify">
The maintainers of <strong>WordHoard</strong> have added rate limits to multiple modules.  These rate limits can be modified, but increasing these predefined limits can lead to querying sessions being dropped or blocked by a source.  
</p>

<p align="justify">
Currently there are 2 parameters that can be set:
</p>

<ul>
	<li>max_number_of_requests</li>
	<li>rate_limit_timeout_period</li>
</ul>

<p align="justify">
These parameters are currently set to 30 requests every 60 seconds. 
</p>

```python 
from wordhoard import Synonyms

synonym = Synonyms(search_string='mother', 
	               max_number_of_requests=30, 
	               rate_limit_timeout_period=60)

results = synonym.find_synonyms()   
```

<p align="justify">
When a rate limit is triggered a warning message is written to both the console and the <i>wordhoard_error.yaml</i> file.  The rate limit will <strong><i>automatically reset</i></strong> after a set time period.  This <strong style="color:red;">reset time period cannot be modified</strong> using a parameter passed in a <i>Class object</i>.  
</p>


### Proxy usage 

<p align="justify">
<strong>WordHoard</strong> provides out of the box usage of proxies. Just define your proxies config as a dictionary and pass it to the corresponding module as shown below.
</p>

```python 
from wordhoard import Synonyms

proxies_example = {
    "http": "your http proxy if available", # example: http://149.28.94.152:8080
    "https": "your https proxy",  # example: https://128.230.60.178:3128
}

synonym = Synonyms(search_string='mother', proxies=proxies_example)
results = synonym.find_synonyms()  
```

<p align="justify">
	It is highly recommended that a reliable commercial proxy service is used over free ones, such as <a href="http://free-proxy.cz">free-proxy.cz</a> or <a href="https://free-proxy-list.net/">Free Proxy List.</a>. 	
</p>


### User Agents

<p align="justify">
<strong>WordHoard</strong> has an embedded file that contains an array of common user agents for these platforms. 
</p>

```python
user_agent_keys = {'chrome macOS': 'chrome_mac_os_x', 
                   'chrome windows': 'chrome_windows_10',
                   'firefox macOS': 'firefox_mac_os_x', 
                   'firefox windows': 'firefox_windows_10',
                   'safari macOS': 'safari_mac_os_x', 
                   'safari iphone': 'safari_iphone',
                   'safari ipad': 'safari_ipad', 
                   'android': 'samsung_browser_android'}

```
<p align="justify">
Without any intervention <strong>WordHoard</strong> is designed to randomly selected one of these user agents when a module (e.g. Synonyms) is being called.  An end user can override this global randomness by passing a string to the variable <i>user_agent</i>. 
</p>

<p align="justify">
For example an end user wanting to use only Safari iPhone user agents would do the following.  The example below would randomly select a Safari iPhone user agent with each Class call. 
</p>


```python 
from wordhoard import Synonyms
from wordhoard.utilities.user_agents import get_specific_user_agent

user_agent = get_specific_user_agent('safari iphone')

synonym = Synonyms(search_string='mother', user_agent=user_agent)
results = synonym.find_synonyms() 

```

<p align="justify">
If an end user wants to pass a specific user agent they would do the following.
</p>

```python 
from wordhoard import Synonyms

synonym = Synonyms(search_string='mother', user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1')
results = synonym.find_synonyms() 

```


