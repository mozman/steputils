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

1. [STEP] - Standard for the Exchange of Product model data - `p21.readfile()` already works and is fast enough. 
2. [XML] - Extensible Markup Language, fast to read from Python with `xml.etree.ElementTree`
3. [JSON] - JavaScript Object Notation, no examples available yet

### EXPRESS Schema Parser

A Python data model generator has to be written for EXPRESS definition files, the solution I found online called 
[STEPcode], is a starting point, but the generated Python code is ugly and does not correspond to PEP8, generated 
code is included in folder `doc/stepcode`.

- EXPRESS data specification language, EXPRESS is a standard data modeling language for product data. 
  EXPRESS is formalized in the ISO Standard for the Exchange of Product model STEP (ISO 10303), and standardized 
  as [ISO 10303-11].
- `iso-10303-11--2004.bnf`: Backus-Naur-Form for EXPRESS
- EXPRESS parser implemented by antlr4 works but is very slow. Generating a Python data model from EXPRESS schema
  is a done once and therefore hasn't to be very fast, but it is a pain in the development and testing phase 
  (Caching AST!).
- The pyparsing implementation does not work but is promising for speed, so I will not abandon this implementation 
  complete - but for now I go the antlr4 route. 

#### Abstract Syntax Tree for EXPRESS

It is required to create an AST from the parse tree, (EXP|XSD) -> AST -> Python Data Model.

Caching the AST could speed up developing and testing phase for the slow antlr4 parser!  

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
   - (+) manually modifications are possible
   - (-) modifications are lost at recreation process
   - (-) big code base     

2. Dynamic: use Python meta programming to create classes on the fly
   - (-) no modifications are possible by default, maybe extensible by mixins
   - (+) small code base

### Instances

Instantiation by factory! `args` is a list of positional arguments and `kwargs` are keyword arguments as a dict.

    ifc4 = steputils.model('IFC4')
    root = ifc4.get_root()
    entity = ifc4.entity('IfcRoot', IfcGloballyUniqueId=guid())

### DOM Interface

Create new model:

    ifc4 = steputils.model('IFC4')

Get root node:

    root = ifc4.get_root()

Create new node:

    entity = ifc4.entity('IfcRoot', IfcGloballyUniqueId=guid())

Adding new node to parent:

    # add one child node
    root.append(entity)
    
    # add multiple child nodes
    root.extend([entity, entity2, ...])
    
    # insert at a specified position
    root.insert(index, entity)
    
Iterate child nodes:

    for entity in root:
        pass

Delete child nodes:

    root.remove(entity)
    
### Query Language - First Draft

Query entities in a XPath like way:

`tag` Selects all child elements with the given tag. For example, `spam` selects all child elements named spam, 
and `spam/egg` selects all grandchildren named egg in all children named spam.

`.` Selects the current node. This is mostly useful at the beginning of the path, to indicate that it’s a relative path.

`*` Selects all child elements. For example, `*/egg` selects all grandchildren named egg

`//` Selects all subelements, on all levels beneath the current element. For example, `.//egg` selects all egg
elements in the entire tree.

`..` Selects the parent element.

`[@attrib]` Selects all elements that have the given attribute.

`[@attrib='value']` Selects all elements for which the given attribute has the given value. The value cannot contain quotes.

`[tag]` Selects all elements that have a child named tag. Only immediate children are supported.

`[tag='text']` Selects all elements that have a child named tag whose complete text content, including descendants,
equals the given text.

`[position]` Selects all elements that are located at the given position. The position is an integer: 1 is the first 
position, -1 for the last position like Python list indices.

    root.findall('spam')  # finds all matching child elements named spam
    root.find('spam')  # find first matching child element named spam


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
