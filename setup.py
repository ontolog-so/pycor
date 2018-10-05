from setuptools import setup, find_packages
from pycor import VERSION 

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name             = 'pycor',
    version          = VERSION.VERSION,
    description      = 'Python based Korean Language Processing Lib, Contextual Parser',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author           = 'Ikchan Kwon',
    author_email     = 'ontolog.so@gmail.com',
    url              = 'https://github.com/ontolog-so/pycor',
    download_url     = 'https://github.com/ontolog-so/pykor/archive/0.0.7.tar.gz',
    license          = 'MIT',
    install_requires = [ 'pandas' ],
    packages         = find_packages(exclude = ['bisect', 'notebooks', 'samples']),
    keywords         = ['Korean NLP', 'POS Tagger', 'Natural Language Contextual Parser'],
    python_requires  = '>=3.6',
    # package_data     =  {},
    # zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3.6'
    ]
)