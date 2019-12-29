STEPutils
=========

THIS PROJECT IS IN PLANNING STATE!
----------------------------------

Abstract
--------

STEPutils is a Python package to manage STEP model data.

The intention of this package is to build a simple document object model (DOM) for STEP model data like 
`xml.etree.ElementTree` for XML data. STEPutils could be used as import/export layer for CAD like application. 
The DOM has methods to traverse, create and delete object nodes but no further CAD-like functionality like translating, 
scaling or rotating objects, if you need that - you are looking for a CAD application like 
[FreeCAD](https://www.freecadweb.org/).   

For more information about the STEP (ISO 10303) standard read this 
[Wikipedia](https://en.wikipedia.org/w/index.php?title=ISO_10303) article.

Quick-Info
----------

- Python package to manage a simple document object model (DOM) for STEP model data
- the intended audience are developers
- requires at least Python 3.6
- OS independent
- tested with CPython & PyPy on Windows 10 & Manjaro Linux
- MIT-License

Installation
------------

Install with pip for Python 3.6 and later:

    pip install steputils

Install latest development version with pip from GitHub:

    pip install git+https://github.com/mozman/steputils.git@master

or from source:

    python setup.py install

Documentation
-------------

https://steputils.readthedocs.io/

Contribution
------------

The source code of STEPutils can be found at __GitHub__, target your pull requests to the `master` branch:

http://github.com/mozman/steputils.git
