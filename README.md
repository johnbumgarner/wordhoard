<p align="center">
   <! -- Graphic source: https://thesaurus.plus --> 
  <img src="https://github.com/johnbumgarner/wordhoard/blob/master/graphic/wordhoard_graphic.jpg"/>
</p>

# Overviews

![PyPI](https://img.shields.io/pypi/v/wordhoard) &nbsp;
![License: MIT](https://img.shields.io/github/license/johnbumgarner/wordhoard)&nbsp;
![GitHub issues](https://img.shields.io/github/issues/johnbumgarner/wordhoard)&nbsp;
![GitHub pull requests](https://img.shields.io/github/issues-pr/johnbumgarner/wordhoard)&nbsp;
[![wordhoard](https://snyk.io/advisor/python/wordhoard/badge.svg)](https://snyk.io/advisor/python/wordhoard)&nbsp;

<!--- [![Downloads](https://static.pepy.tech/personalized-badge/wordhoard?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/wordhoard) --->


 

# Primary Use Case
<p align="justify"> 
Textual analysis is a broad term for various research methodologies used to qualitatively describe, interpret and understand text data. These methodologies are mainly used in academic research to analyze content related to media and communication studies, popular culture, sociology, and philosophy. Textual analysis allows these researchers to quickly obtain relevant insights from unstructured data. All types of information can be gleaned from textual data, especially from social media posts or news articles. Some of this information includes the overall concept of the subtext, symbolism within the text, assumptions being made and potential relative value to a subject (e.g. data science). In some cases it is possible to deduce the relative historical and cultural context of a body of text using analysis techniques coupled with knowledge from different disciplines, like linguistics and semiotics.
   
Word frequency is the technique used in textual analysis to measure the frequency of a specific word or word grouping within unstructured data. Measuring the number of word occurrences in a corpus allows a researcher to garner interesting insights about the text. A subset of word frequency is the correlation between a given word and that word's relationship to either antonyms and synonyms within the specific corpus being analyzed. Knowing these relationships is critical to improving word frequencies and topic modeling.

<strong>Wordhoard</strong> was designed to assist researchers performing textual analysis to build more comprehensive lists of antonyms, synonyms, hypernyms, hyponyms and homophones.
</p>

# Installation

<p align="justify"> 
   Install the distribution via pip:
</p>

```python
pip3 install wordhoard
```

# General Package Utilization

<p align="justify">
Please reference the <a href="https://wordhoard.readthedocs.io/en/latest" target="_blank">WordHoard Documentation</a> for package usage guidance and parameters.
</p>

# Sources

<p align="justify">
This package is designed to query these online sources for antonyms, synonyms, hypernyms, hyponyms and definitions:

1. classicthesaurus.com
2. collinsdictionary.com
3. merriam-webster.com
4. synonym.com
5. thesaurus.com
6. wordhippo.com
7. wordnet.princeton.edu
</p>
  
# Dependencies

<p align="justify">
This package has these core dependencies:
  
1. <b>backoff</b>
2. <b>BeautifulSoup</b>
3. <b>deckar01-ratelimit</b>
4. <b>deepl</b>
5. <b>lxml</b>
6. <b>requests</b>
7. <b>urllib3</b>
</p>

<p align="justify">
Additional details on this package's dependencies can be found <a href="https://wordhoard.readthedocs.io/en/latest/dependencies" target="_blank">here</a>.
</p>

# Development

<p align="justify">
If you would like to contribute to the <i>Wordhoard</i> project please read the <a href="https://wordhoard.readthedocs.io/en/latest/contributing" target="_blank">contributing guidelines</a>.
   
Items currently under development:
   - English language word verification using the Python package `pyenchant` 
   - Expanding the list of hypernyms, hyponyms and homophones
   - Adding part-of-speech filters in queries 
</p>

# Issues

<p align="justify">
This repository is actively maintained.  Feel free to open any issues related to bugs, coding errors, broken links or enhancements. 

You can also contact me at [John Bumgarner](mailto:wordhoardproject@gmail.com?subject=[GitHub]%20wordhoard%20project%20request) with any issues or enhancement requests.
</p>


# Sponsorship
   
If you would like to contribute financially to the development and maintenance of the <i>Wordhoard</i> project please read the <a href="https://github.com/johnbumgarner/wordhoard/blob/master/SPONSOR.md">sponsorship information</a>.

# License

<p align="justify">
The MIT License (MIT).  Please see <a href="https://wordhoard.readthedocs.io/en/latest/license" target="_blank">License File</a> for more information.
</p>

