Project Goals
=============

The main goal is to build a simple document object model (DOM) for [STEP] model data. 
The DOM can be used as an import/export layer for CAD like application or applications which need access to 
STEP model data. STEP defines various applications, one example application is [IFC4] data 
(Industry Foundation Classes [1]), this also will be the first application with explict support, because it is related 
to my profession and because there is a free documentation for [IFC4] provided by 
[buildingSMART International](https://www.buildingsmart.org/). Other applications of the ISO 10303 standard may not have
such free resources, and I will not purchase ISO standards for a hobby project and because of the complexity it is 
not possible for me to support all application in an extensive way beyond a generic support.

The DOM should provide methods to travers the model and create or delete object nodes like `xml.etree.ElementTree` for 
XML data.

Loading and Storing Data
------------------------

Many file formats of the [STEP] standard should be supported, as plain text file and also as 
compressed zip file:

1. [STEP] -  Standard for the Exchange of Product model data
2. [XML] - Extensible Markup Language
3. [JSON] - JavaScript Object Notation

### STEP Requirements & Resources

A parser generator has to be written for EXPRESS definition files, the solution I found online called [STEPcode], 
is starting point, but the generated Python code is ugly and does not correspond to PEP8, generated code is included in 
folder `doc/stepcode`.

Resources to build STEP parser:

- EXPRESS data specification language, EXPRESS is a standard data modeling language for product data. 
  EXPRESS is formalized in the ISO Standard for the Exchange of Product model STEP (ISO 10303), and standardized 
  as [ISO 10303-11].
- `iso-10303-11--2004.bnf`: Backus-Naur-Form for EXPRESS
- `iso-10303-21--2002.bnf`: Backus-Naur-Form for STEP-File: [ISO 10303-21] defines the encoding mechanism for 
  representing data conforming to a particular schema in the EXPRESS data modeling language specified in [ISO 10303-11]. 
  A STEP-File is also called p21-File and STEP Physical File. The file extensions .stp and .step indicate that the file 
  contains data conforming to STEP Application Protocols while the extension .p21 should be used for all other purposes.

### XML Requirements & Resources

Import/Export by standard Python module `xml.etree.ElementTree` and the ability to use an faster alternative 
implementation like [lxml]. 

### JSON Requirements & Resources

Import/Export by the standard Python module `json` and the ability to use an faster alternative implementation 
like [orjson]. 

Internal Data Model
-------------------

### Classes

1. Static: create class declarations from EXPRESS file as a Python .py file
   - (-) requires data from EXPRESS file, need a parser
   - (+) manually modifications are possible
   - (-) modifications are lost at recreation process
   - (-) big code base     

2. Dynamic: use Python meta programming to create classes on the fly
   - (-) requires data from EXPRESS file, need a parser  
   - (-) no modifications are possible by default, maybe extensible by mixins
   - (+) small code base

### Instances

Instantiation by factory! `args` is a list of positional arguments and `kwargs` are keyword arguments as a dict.

```
    def instance(cls_name: str, *args, **kwargs):
        pass

    e = ifc2data.instance('IfcRoot', IfcGloballyUniqueId=guid())
```

Parsing
-------

Use [pyparsing] to write parsers, i have already some experience with this tool and it is Pythonic,
big disadvantage: it is slow!

But speed shouldn't be a problem, an EXPRESS parser does not have to be fast because parsing EXPRESS files is not a 
runtime process, and STEP-files are organized as one object per line, sometimes very long lines, but mostly short 
lines, so no deep nested parsing is necessary, for XML and JSON exist Python tools and advanced 3rd party libs.   

[IFC4]: https://technical.buildingsmart.org/
[STEP]: https://en.wikipedia.org/wiki/ISO_10303-21
[XML]: https://en.wikipedia.org/wiki/XML
[JSON]: https://en.wikipedia.org/wiki/JSON
[STEPcode]: https://stepcode.github.io/
[orjson]: https://pypi.org/project/orjson/
[lxml]: https://pypi.org/project/lxml/
[BNF]: https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form
[ISO 10303-21]: https://en.wikipedia.org/wiki/ISO_10303-21
[ISO 10303-11]: https://en.wikipedia.org/wiki/EXPRESS_(data_modeling_language)
[pyparsing]: https://pypi.org/project/pyparsing/

[1]: https://en.wikipedia.org/wiki/Industry_Foundation_Classes
