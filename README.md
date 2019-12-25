Ifc4data
========

THIS PROJECT IS IN PLANNING STATE!
----------------------------------

Abstract
--------

Ifc4data is a Python package to manage IFC4 data.

The intention of this package is to build a simple document object model (DOM) for IFC4 like `xml.etree.ElementTree` 
for XML data. This DOM can be loaded from a file or text stream and written to a file or text stream and could be 
used as import/export layer for CAD like application. The DOM has methods to traverse, create and delete object 
nodes but no further CAD-like functionality like translating, scaling or rotating objects, if you need that - you are 
looking for a CAD application like [FreeCAD](https://www.freecadweb.org/).   

For more information about the IFC4 standard go to [buildingSMART International](https://technical.buildingsmart.org/).

Quick-Info
----------

- Python package to manage a simple document object model (DOM) for IFC4 data
- the intended audience are developers
- requires at least Python 3.6
- OS independent
- tested with CPython & PyPy on Windows 10 & Manjaro Linux
- MIT-License

Installation
------------

Install with pip for Python 3.6 and later:

    pip install ifc4data

Install latest development version with pip from GitHub:

    pip install git+https://github.com/mozman/ifc4data.git@master

or from source:

    python setup.py install

Contribution
------------

The source code of ifc4data can be found at __GitHub__, target your pull requests to the `master` branch:

http://github.com/mozman/ifc4data.git
