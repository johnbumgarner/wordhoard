<h1 style="color:IndianRed;"><strong>Dependencies</strong></h1>

---

<p align="justify">
	The <strong>WordHoard</strong> package has these core external dependencies:
</p>

<h3 style="color:IndianRed;">backoff</h3>

<p align="justify">
The Python package <a href="https://github.com/litl/backoff" target="_blank">backoff</a> is used in conjunction with <a href="https://github.com/deckar01/ratelimit" target="_blank">deckar01-ratelimit</a>. The primary function of this module is to provide function decorators which can be used to wrap a function such that it will be retried until some condition is met.
</p>


<h3 style="color:IndianRed;">Beautiful Soup</h3>
<p align="justify">
The Python package <a href="https://beautiful-soup-4.readthedocs.io/en/latest" target="_blank">Beautiful Soup</a> is used to find and parse predefined content from a website related to a news article or from an HTML (HyperText Markup Language) file.
</p>


<h3 style="color:IndianRed;">certifi</h3>
<p align="justify">
The Python package <a href="https://certifiio.readthedocs.io/en/latest" target="_blank">certifi</a> is a carefully curated collection of Root Certificates for validating the trustworthiness of SSL certificates while verifying the identity of TLS hosts. This module is a required dependency of the Python library 
<a href="https://docs.python-requests.org/en/latest" target="_blank">requests</a>. 
</p>


<h3 style="color:IndianRed;">charset-normalizer</h3>
<p align="justify">
The Python package <a href="https://github.com/ousret/charset_normalizer" target="_blank">charset-normalizer</a> is used for language detection from an unknown charset encoding. This module is a required dependency of the Python library <a href="https://docs.python-requests.org/en/latest" target="_blank">requests</a>. 
</p>


<h3 style="color:IndianRed;">click</h3>
<p align="justify">
The Python package <a href="https://palletsprojects.com/p/click/" target="_blank">click</a> is used to create command line interfaces.  This module is a required dependency of the Python library <a href="https://github.com/DeepLcom/deepl-python" target="_blank">deepl</a>. 
</p>


<h3 style="color:IndianRed;">cloudscraper</h3>
<p align="justify">
The Python package <a href="https://github.com/venomous/cloudscraper" target="_blank">cloudscraper</a> is used to bypass websites being protected by Cloudflare's nti-bot protection system. This package has these core dependencies: <a href="https://certifiio.readthedocs.io/en/latest" target="_blank">certifi</a>, <a href="https://github.com/ousret/charset_normalizer" target="_blank">charset-normalizer</a>, <a href="https://github.com/kjd/idna" target="_blank">idna</a>, <a href="https://github.com/pyparsing/pyparsing/" target="_blank">pyparsing</a>, <a href="https://docs.python-requests.org/en/latest" target="_blank">requests</a>, <a href="https://toolbelt.readthedocs.io/en/latest/" target="_blank">requests-toolbelt</a>, and <a href="https://github.com/urllib3/urllib3" target="_blank">urllib3</a>.
</p>


<h3 style="color:IndianRed;">deckar01-ratelimit</h3>
<p align="justify">
The Python package <a href="https://github.com/deckar01/ratelimit" target="_blank">ratelimit</a> is used to limit the number of queries to a specific website for a predefined time period.  This rate limiting helps to reduce the possibility of a website blocking your IP address for aggressive behavior when requesting multiple articles in succession.  This rate limiting is configurable in <i>WordHoard</i>, but the timeout period for violating a rate limit is not configurable.  
</p>


<h3 style="color:IndianRed;">deepl</h3>
<p align="justify">
The Python package <a href="https://github.com/DeepLcom/deepl-python" target="_blank">deepl</a> is used for language translation.  The package is a wrapper for the DeepL API, which requires an account, which can be either a paid subscription or free one with specific limitation, such as monthly character limits. This package has these core dependencies: <a href="https://certifiio.readthedocs.io/en/latest" target="_blank">certifi</a>, <a href="https://github.com/ousret/charset_normalizer" target="_blank">charset-normalizer</a>, <a href="https://github.com/kjd/idna" target="_blank">idna</a>, <a href="https://docs.python-requests.org/en/latest" target="_blank">requests</a>, and <a href="https://github.com/urllib3/urllib3" target="_blank">urllib3</a>.
</p>


<h3 style="color:IndianRed;">idna</h3>
<p align="justify">
The Python package <a href="https://github.com/kjd/idna" target="_blank">idna</a> exposes the Internationalised Domain Names in Applications (IDNA) protocol as specified in <a href="https://datatracker.ietf.org/doc/html/rfc5891" target="_blank">RFC 5891</a>, which is used for encoding and decoding. This module is a required dependency of the Python library <a href="https://docs.python-requests.org/en/latest" target="_blank">requests</a>. 
</p>


<h3 style="color:IndianRed;">lxml</h3>
<p align="justify">
The Python package <a href="https://lxml.de" target="_blank">lxml</a> is used for processing XML data. For example the function <i>lxml.html.clean.Cleaner</i> is used to remove unwanted tags and content types from an HTML document. This module is a required dependency of the Python library <a href="https://beautiful-soup-4.readthedocs.io/en/latest" target="_blank">Beautiful Soup</a>. 
</p>

<h3 style="color:IndianRed;">pyparsing</h3>
<p align="justify">
The Python package <a href="https://github.com/pyparsing/pyparsing/" target="_blank">pyparsing</a> provides a library of classes that client code uses to construct the grammar directly in Python code.  This module is a required dependency of the Python library <a href="https://github.com/venomous/cloudscraper" target="_blank">cloudscraper</a>.
</p>


<h3 style="color:IndianRed;">requests</h3>
<p align="justify">
The Python package <a href="https://docs.python-requests.org/en/latest" target="_blank">requests</a> is the de facto standard for making HTTP requests in Python. 
</p>


<h3 style="color:IndianRed;">requests-toolbelt</h3>
<p align="justify">
The Python package <a href="https://toolbelt.readthedocs.io/en/latest/" target="_blank">requests-toolbelt</a> is a collection of tools that can be used by the Python package <a href="https://docs.python-requests.org/en/latest" target="_blank">requests</a>. This module is a required dependency of the Python library <a href="https://github.com/venomous/cloudscraper" target="_blank">cloudscraper</a>.
</p>


<h3 style="color:IndianRed;">Soup Sieve</h3>
<p align="justify">
The Python package <a href="https://github.com/facelessuser/soupsieve" target="_blank">Soup Sieve</a> is CSS selector library. This module is a required dependency of the Python library <a href="https://beautiful-soup-4.readthedocs.io/en/latest" target="_blank">Beautiful Soup</a>. 
</p>


<h3 style="color:IndianRed;">urllib3</h3>
<p align="justify">
The Python package <a href="https://github.com/urllib3/urllib3" target="_blank">urllib3</a> is a powerful, user-friendly HTTP client for Python. This module is a required dependency of the Python libraries <a href="https://docs.python-requests.org/en/latest" target="_blank">requests</a> and <a href="https://github.com/venomous/cloudscraper" target="_blank">cloudscraper</a>.
</p>




