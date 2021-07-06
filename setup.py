import setuptools

with open("PYPI_description.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordhoard",
    version="1.4.6",
    author="John Bumgarner",
    author_email="wordhoardproject@gmail.com",
    description="A comprehensive lexical discovery application that is useful for finding semantic relationships between "
                "words including a word's synonyms, synonyms, hypernyms, hyponyms and homophones.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnbumgarner/wordhoard",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'files': ['files/common_english_homophones.pkl',
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
    keywords=['antonyms', 'synonyms', 'hypernyms', 'hyponyms', 'homophones', 'definitions', 'lexicon',
              'semantic relationships', 'natural language processing'],
    python_requires='>=3.6',
    install_requires=['bs4',
                      'deep-translator',
                      'lxml',
                      'requests',
                      'urllib3']
)

