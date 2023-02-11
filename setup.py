import setuptools

with open("PYPI_description.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordhoard",
    version="1.5.2",
    author="John Bumgarner",
    author_email="wordhoardproject@gmail.com",
    description="A comprehensive lexical discovery application that is useful for finding semantic relationships "
                "such as, the antonyms, synonyms, hypernyms, hyponyms, homophones and definitions for a specific word.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnbumgarner/wordhoard",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'files': ['files/common_user_agents.pkl',
                            'files/common_english_homophones.pkl',
                            'files/no_homophones_english.pkl']},
    license='LICENSE.txt',
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Topic :: Software Development :: Libraries",
                 "Topic :: Text Processing :: Linguistic",
                 "Topic :: Utilities"],
    keywords=['antonyms', 'bag of words', 'definitions', 'hypernyms', 'hyponyms', 'homophones',
              'information retrieval', 'lexicon', 'semantic relationships', 'synonyms',
              'natural language processing'],
    python_requires='>=3.6',
    install_requires=['backoff>=2.2.1',
                      'beautifulsoup4>=4.11.2',
                      'certifi>=2022.12.7',
                      'charset-normalizer>=3.0.1',
                      'deckar01-ratelimit>=3.0.2',
                      'deepl>=1.13.0',
                      'lxml>=4.9.2',
                      'requests>=2.28.2',
                      'soupsieve>=1.2',
                      'urllib3>=1.26.14']
)
