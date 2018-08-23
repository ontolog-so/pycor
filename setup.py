from setuptools import setup, find_packages

setup(
    name             = 'pycor',
    version          = '0.0.3',
    description      = 'Python based Korean Language Processing Lib, POS Tagger',
    author           = 'Ikchan Kwon',
    author_email     = 'ontolog.so@gmail.com',
    url              = 'https://github.com/ontolog-so/pycor',
    download_url     = 'https://github.com/ontolog-so/pykor/archive/0.0.3.tar.gz',
    install_requires = [ ],
    packages         = find_packages(exclude = ['bisect', 'notebooks', 'samples']),
    keywords         = ['Korean NLP', 'POS Tagger'],
    python_requires  = '>=3.6',
    # package_data     =  {},
    # zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3.6'
    ]
)