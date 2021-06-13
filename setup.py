import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordhoard",
    version="1.4.5",
    author="John Bumgarner",
    author_email="wordhoardproject@gmail.com",
    description="lexical processing for textual analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnbumgarner/wordhoard",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'files': ['files/common_english_homophones.pkl',
                            'files/no_homophones_english.pkl']},
    license='LICENSE.txt',
    classifiers=["License :: OSI Approved :: MIT License", "Operating System :: OS Independent"],
    keywords='antonyms, synonyms, hypernyms, hyponyms, homophones, definitions, lexicon, wordsearch',
    python_requires='>=3.6',
    install_requires=['bs4', 'lxml', 'requests', 'urllib3']
)

