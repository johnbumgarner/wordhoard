<h1 style="color:IndianRed;"><strong> Release Notes </strong></h1>

---

<p align="justify"> 
This page provides information on all the <strong>WordHoard</strong> releases since inception.
</p>

<h2 style="color:IndianRed;"> Version 1.5.5 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>05.23.2024</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Code refactoring to improved modularization for readability and to reduce duplicated code related to error handling and querying.</i>

---

<p align="justify"> 
	Mutiple modules were refactored to improve readability and reduce duplicated code.  The following modules had new Classes added to 
obtain parts of speech and data extract using <i> BeautifulSoup </i> .
</p>

<ul>
	<li>antonyms</li>
	<li>dictionary</li>
	<li>synonyms</li>
</ul>


<p align="justify"> 
	The optional variable <i>sources</i> had been added to following modules. This variable allows you to refine the search sources to fit your requirements. 
</p>

<ul>
	<li>antonyms</li>
	<li>dictionary</li>
	<li>synonyms</li>
</ul>

<p align="justify"> 
	Type hinting was validated in all functions within all query modules and all utilities modules. Additionally, all parameter names in every function or call have been added.  This improves code readability and reduces ambiguity when reviewing the code.  
</p>

<p align="justify"> 
	Cloudflare verification was modified with a timeout feature. Using <a href="https://www.collinsdictionary.com">Collins Dictionary</a> as a source can increase the runtime of <strong>WordHoard</strong> in the following modules.
</p>

<ul>
	<li>antonyms</li>
	<li>dictionary</li>
	<li>synonyms</li>
</ul>

<h2 style="color:IndianRed;"> Version 1.5.4 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>06.01.2023</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Code enhancements to improve cache processing related to list output for these modules.</i>

<ul>
    <li>antonyms</li>
    <li>dictionary</li>
    <li>hypernyms</li>
    <li>hyponyms</li>
    <li>synonyms</li>	
</ul>

<p align="justify"> 
    Updated the colorized text module. And updated console warnings and informational messages with various shades of colorized text.
</p>

<h2 style="color:IndianRed;"> Version 1.5.3 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>03.21.2023</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Code enhancements to improve performance when querying online repositories and to obtain part of speech category for word being queried.</i>

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

<h2 style="color:IndianRed;"> Version 1.5.2 </h2>


<strong>Date of Release:&nbsp;&nbsp;</strong>  <i>02.13.2023</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong>  <i>Code enhancements of the Translator classes and bug fix in the dictionary module</i>

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


<h2 style="color:IndianRed;"> Version 1.5.1 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>04.06.2022</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Code enhancements (proxy and user agents)</i>

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

<h2 style="color:IndianRed;"> Version 1.5.0 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>09.24.2021</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Code enhancements (proxy and translation support)</i>

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

<h2 style="color:IndianRed;"> Version 1.4.9 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>09.07.2021</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Added query rate limiting and additional exception handling</i>

---

<p align="justify"> 
Rate limiting was added to all modules that query online repositories. Additional exception handling was added to the <i>basic_soup.py</i> module and all modules that query online repositories. This extra exception handling can be used to diagnose issues related to queuing the online repositories.
</p>


<h2 style="color:IndianRed;"> Version 1.4.8 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>08.24.2021</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Removed source and leftover debugging code</i>

---

<p align="justify"> 
One of the original sources being queried was providing questionable synonyms and antonyms. That source was 
<a href="https://thesaurus.plus">thesaurus.plus</a>, which was removed from the query pool.
</p>


<h2 style="color:IndianRed;"> Version 1.4.7 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong>  <i>08.15.2021</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Bugfix linked to changes in a page's navigational structure</i>

---

<p align="justify"> 
This bugfix was related to the source <a href="https://www.synonym.com">synonym.com</a> modifying its page navigational structure. This structural change caused the extraction code for the source to fail. It was determined that this change impacted the <strong>Wordhoard</strong> extraction modules antonyms, synonyms and definitions.
</p>

<p align="justify"> 
Version 1.4.7 was redesigned to handle this new navigational structure.
</p>

<h2 style="color:IndianRed;"> Version 1.4.6 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>06.06.2021</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Code redesign and enhancements</i>

---

<p align="justify"> 
The python modules antonyms, dictionary, homophones, hyponyms, hypernyms and synonyms were all redesign into Python Classes. The Classes reduce the complexity of having to call individual sources.
</p>

<p align="justify"> 
The internal caching was improved.
</p>

<p align="justify"> 
Console logging was disabled and all log entries are now written only to the file <i>wordhoard_error.yaml</i>.
</p>

<h2 style="color:IndianRed;"> Version 1.4.5 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong>  <i>05.12.2021</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong> <i>Code enhancements</i>

---

<p align="justify"> 
Version 1.4.5 includes new modules to find hypernyms, hyponyms and homophones for words in the English language.
</p>

<p align="justify">
    The discrepancy in version numbering been 1.2 and 1.4.5 is related to Python Package Index (PyPI) issues related to builds.
</p>

<h2 style="color:IndianRed;"> Version 1.2 </h2>

<strong>Date of Release:&nbsp;&nbsp;</strong> <i>10.23.2020</i>
<br>
<strong>Purpose:&nbsp;&nbsp;</strong>  <i>Initial Release</i>

---

<p align="justify"> 
Version 1.2 includes both console-level and file-level logging. It also has in-memory caching capabilities for queries.
</p>
