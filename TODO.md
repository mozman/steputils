Project Goals
=============

The main goal is to build a simple document object model (DOM) for [IFC4] (Industry Foundation Classes [1]) data. 
The DOM can be used as an import/export layer for CAD like application or applications which need access to 
IFC data.

The DOM should provide methods to travers the model and create or delete object nodes like `xml.etree.ElementTree` for 
XML data.

Loading and Storing Data
------------------------

All official mentioned file formats of the [IFC4] standard should be supported, as plain text file and also as 
compressed zip file:

1. [STEP] -  Standard for the Exchange of Product model data
2. [XML] - Extensible Markup Language
3. [JSON] - JavaScript Object Notation

### STEP Requirements & Resources

A parser has to be written for the STEP format, based on the EXPRESS definition file, provided by the [IFC4] maintainer, 
if possible in an automated way, but the solution I found online called [STEPcode], is not a good starting 
point, because the generated Python code is just ugly and does not correspond to PEP8, generated code is included in 
folder `doc/stepcode`.

Resources to build STEP parser:

- `IFC4x2.exp`: EXPRESS data specification language, EXPRESS is a standard data modeling language for product data. 
  EXPRESS is formalized in the ISO Standard for the Exchange of Product model STEP (ISO 10303), and standardized 
  as [ISO 10303-11].
- `IFC4x2.xsd`: XML Schema definition language (XSD), defined in XML Schema W3C Recommendation
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

[1]: https://en.wikipedia.org/wiki/Industry_Foundation_Classes
