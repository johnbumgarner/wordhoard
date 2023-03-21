<h1><strong> Release Notes </strong></h1>
---

<p align="justify"> 
This page provides information on all the <strong>WordHoard</strong> releases since inception.
</p>

## Version 1.5.3

<strong>Date of Release: 03.21.2023</strong><br>
<strong>Purpose: Code enhancements to improve performance when querying online repositories and to obtain part of speech category for word being queried.</strong>

---

<p align="justify"> 
	A <i>ThreadPoolExecutor function</i> and more targeted word extraction was added to the following modules. The 
	<i>ThreadPoolExecutor</i> decreases collection time by almost 50% in some cases.  The targeted extraction is designed to find more relevant antonyms, synonyms and definitions. 
</p>

<ul>
	<li>antonyms</li>
	<li>dictionary</li>
	<li>synonyms</li>
</ul>


<p align="justify"> 
	Type hinting was added to all functions within all query modules and all utilities modules.  
</p>


<p align="justify"> 
	Additional Cloudflare verification was added to the query modules. This verification allowed the source 
	<a href="https://www.collinsdictionary.com">Collins Dictionary</a> to be readded to the list of repositories being queried. 
</p>


## Version 1.5.2

<strong>Date of Release: 02.12.2023</strong><br>
<strong>Purpose: Code enhancements of the Translator classes and bug fix in the dictionary module</strong>

---

<p align="justify"> 
Fixed the bug identified in the Issue 14: &nbsp <a href="https://github.com/johnbumgarner/wordhoard/issues/14">find_definitions can returns antonyms</a>
</p>


## Version 1.5.2

<strong>Date of Release: 02.12.2023</strong><br>
<strong>Purpose: Code enhancements of the Translator classes and bug fix in the dictionary module</strong>

---

<p align="justify"> 
Fixed the bug identified in the Issue 14: &nbsp <a href="https://github.com/johnbumgarner/wordhoard/issues/14">find_definitions can returns antonyms</a>
</p>

<p align="justify"> 
Redesigned the <i>Exceptions</i> in these modules:
</p>

<ul>
	<li>deep_translator.py</li>
	<li>google_translator.py</li>
	<li>mymemory_translator.py</li>
</ul>

<p align="justify"> 
Updated the available languages for translations in these modules:
</p>

<ul>
	<li>deep_translator.py</li>
	<li>google_translator.py</li>
	<li>mymemory_translator.py</li>
</ul>

<p align="justify"> 
Added a module for email address verification and one for colorized text for specific 
error messages sent to the console/terminal. 
</p>

<p align="justify"> 
Updated and tested the <a href="https://wordhoard.readthedocs.io/en/latest/dependencies/">dependencies</a> for 
WordHoard.
</p>


## Version 1.5.1

<strong>Date of Release: 04.06.2022</strong><br>
<strong>Purpose: Code enhancements (proxy and user agents)</strong>

---

<p align="justify"> 
Proxy enhancements were added to these modules:
</p>

<ul>
	<li>antonyms</li>
	<li>dictionary</li>
	<li>hypernyms</li>
	<li>hyponyms</li>
	<li>synonyms</li>
</ul>

<p align="justify"> 
Selectable user agents capabilities were added to these modules:
</p>

<ul>
	<li>antonyms</li>
	<li>dictionary</li>
	<li>hypernyms</li>
	<li>hyponyms</li>
	<li>synonyms</li>
</ul>

<p align="justify"> 
	The source <a href="https://www.collinsdictionary.com">Collins Dictionary</a> was disabled in <strong>WordHoard</strong>, because Cloudflare DDoS mitigation service protection was recently added. 
</p>


## Version 1.5.0

<strong>Date of Release: 09.24.2021</strong><br>
<strong>Purpose: Code enhancements (proxy and translation support)</strong>

---

<p align="justify"> 
Proxy support was added to these modules:
</p>

<ul>
	<li>antonyms</li>
	<li>dictionary</li>
	<li>hypernyms</li>
	<li>hyponyms</li>
	<li>synonyms</li>
</ul>

<p align="justify"> 
These modules and the homophones module now have configurable output formatting capabilities. The default formatting is a Python List. The secondary format is a Python dictionary.
</p>

<p align="justify"> 
Updated User-Agents were also added to wordhoard.
</p>

<p align="justify"> 
Multiple translation modules were also added to wordhoard. These modules are:
</p>
<ul>
	<li><a href="https://translate.google.com">Google Translate</a></li>
	<li><a href="https://www.deepl.com/translator">DeepL Translate</a></li>
	<li><a href="https://mymemory.translated.net">MyMemory Translate</a></li>
</ul>


## Version 1.4.9

<strong>Date of Release: 09.07.2021</strong><br>
<strong>Purpose: Added query rate limiting and additional exception handling</strong>

---

<p align="justify"> 
Rate limiting was added to all modules that query online repositories. Additional exception handling was added to the <i>basic_soup.py</i> module and all modules that query online repositories. This extra exception handling can be used to diagnose issues related to queuing the online repositories.
</p>


## Version 1.4.8

<strong>Date of Release: 08.24.2021</strong><br>
<strong>Purpose: Removed source and leftover debugging code</strong>

---

<p align="justify"> 
One of the original sources being queried was providing questionable synonyms and antonyms. That source was 
<a href="https://thesaurus.plus">thesaurus.plus</a>, which was removed from the query pool.
</p>


## Version 1.4.7

<strong>Date of Release: 08.15.2021</strong><br>
<strong>Purpose: Bugfix linked to changes in a page's navigational structure</strong>

---

<p align="justify"> 
This bugfix was related to the source <a href="https://www.synonym.com">synonym.com</a> modifying its page navigational structure. This structural change caused the extraction code for the source to fail. It was determined that this change impacted the <strong>Wordhoard</strong> extraction modules antonyms, synonyms and definitions.
</p>

<p align="justify"> 
Version 1.4.7 was redesigned to handle this new navigational structure.
</p>



## Version 1.4.6

<strong>Date of Release: 06.06.2021</strong><br>
<strong>Purpose: Code redesign and enhancements</strong>

---

<p align="justify"> 
The python modules antonyms, dictionary, homophones, hyponyms, hypernyms and synonyms were all redesign into Python Classes. The Classes reduce the complexity of having to call individual sources.
</p>

<p align="justify"> 
The internal cacheing was improved.
</p>

<p align="justify"> 
Console logging was disabled and all log entries are now written only to the file <i>wordhoard_error.yaml</i>.
</p>


## Version 1.4.5

<strong>Date of Release: 05.12.2021</strong><br>
<strong>Purpose: Code enhancements</strong>

---

<p align="justify"> 
Version 1.4.5 includes new modules to find hypernyms, hyponyms and homophones for words in the English language.
</p>


## Version 1.2

<strong>Date of Release: 10.23.2020</strong><br>
<strong>Purpose: Initial Release</strong>

---

<p align="justify"> 
Version 1.2 includes both console-level and file-level logging. It also has in-memory caching capabilities for queries.
</p>
