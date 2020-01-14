#!/usr/bin/env python3
# Created: 25.12.2019
# Copyright (c) 2019-2020 Manfred Moitzi
# License: MIT License
import os
from setuptools import setup, find_packages


# setuptools docs: https://setuptools.readthedocs.io/en/latest/setuptools.html

def get_version():
    # do not import package, because required packages may not be installed yet
    v = {}
    exec(open('./src/steputils/version.py').read(), v)
    return v['__version__']


def read(fname, until=""):
    def read_until(lines):
        last_index = -1
        for index, line in enumerate(lines):
            if line.startswith(until):
                last_index = index
                break
        return "".join(lines[:last_index])

    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return read_until(f.readlines()) if until else f.read()
    except IOError:
        return "File '%s' not found.\n" % fname


setup(
    name='steputils',
    version=get_version(),
    description='A Python package to read/write STEP data files.',
    author='Manfred Moitzi',
    author_email='me@mozman.at',
    url='http://github.com/mozman/steputils',
    download_url='https://pypi.org/project/steputils/',
    project_urls={
        'Documentation': 'https://steputils.readthedocs.io',
        'Wiki': 'https://github.com/mozman/steputils/wiki',
        'Source': 'http://github.com/mozman/steputils',
        'Bug Tracker': 'https://github.com/mozman/steputils/issues',
    },
    python_requires='>=3.6',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    provides=['steputils'],
    install_requires=['pyparsing', 'antlr4-python3-runtime'],
    setup_requires=['wheel'],
    tests_require=['pytest'],
    keywords=['IFC4', 'CAD', 'STEP'],
    long_description=read('README.md') + read('NEWS.md'),
    long_description_content_type="text/markdown",
    platforms="OS Independent",
    license="MIT License",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)

# Development Status :: 1 - Planning
# Development Status :: 2 - Pre-Alpha
# Development Status :: 3 - Alpha
# Development Status :: 4 - Beta
# Development Status :: 5 - Production/Stable
# Development Status :: 6 - Mature
# Development Status :: 7 - Inactive
