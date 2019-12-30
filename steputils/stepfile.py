# Created: 26.12.2019
# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
from typing import List, TextIO, Dict, Union, Iterable, Tuple
from typing import Optional as Opt

from collections import OrderedDict, ChainMap
from datetime import datetime

from pyparsing import (
    nums, hexnums, Literal, Char, Word, Regex, Optional, Forward, ZeroOrMore, OneOrMore,
    Combine, Suppress, cStyleComment,
)
from string import ascii_lowercase, ascii_uppercase

""" 
STEP physical file representation (STEP-file) specified by the ISO 10303-21 standard.

Documentation: https://en.wikipedia.org/wiki/ISO_10303-21

"""


# Data types:
#   Source: https://en.wikipedia.org/wiki/ISO_10303-21
#
# int: 123
# real: 123.0e+2
# binary: "0FF" | "1FF" | "2FF" | "3FF"
#   Binary values (bit sequences) are encoded as hexadecimal and surrounded by double quotes, with a leading character
#   indicating the number of unused bits (0, 1, 2, or 3) (?highest or lowest  bits? - assume: highest bits!)
#   followed by uppercase hexadecimal encoding of data. It is important to note that the entire binary value is
#   encoded as a single hexadecimal number, with the highest order  bits in the first hex character and the lowest
#   order bits in the last one.
#
# string: 'string'
#   For characters with a code greater than 126 a special encoding is used. The character sets as defined in ISO 8859
#   and 10646 are supported. Note that typical 8 (e.g. west European) or 16 (Unicode) bit character sets cannot
#   directly be taken for STEP-file strings. They have to be decoded in a very special way.
#

class StepFileStructureError(Exception):
    pass


class ParameterList(tuple):
    """ Typing helper class for parameter list. """

    # list: (arg1, list2, ...)
    #
    # The elements of aggregates (SET, BAG, LIST, ARRAY) are given in parentheses, separated by ",".


class EntityInstanceName(str):
    """ Typing helper class for entity instance name."""
    # instance_name: #1234
    #
    # Every entity instance in the exchange structure is given a unique name in the form "#1234". The instance name must
    # consist of a positive number (>0) and is typically smaller than 263. The instance name is only valid locally within
    # the STEP-file (?across multiple data sections? - assume: yes!).
    # If the same content is exported again from a system the instance names may be different for the same
    # instances. The instance name is also used to reference other entity instances through attribute values or aggregate
    # members. The referenced instance may be defined before or after the current instance.
    pass


class Keyword(str):
    """ Typing helper class for keyword."""
    pass


class Enumeration(str):
    """ Typing helper class for enumeration."""
    # enum: .ENUM.
    #   Enumeration, boolean and logical values are given in capital letters with a leading and trailing dot such as
    #   ".TRUE.".
    pass


class UnsetParameter(str):
    """ Typing helper class for unset parameter."""
    # omitted argument: $ or *
    #     Source: https://en.wikipedia.org/wiki/ISO_10303-21
    #     Unset attribute values are given as "$".
    #     Explicit attributes which got re-declared as derived in a subtype are encoded as "*" in the position of the
    #     supertype attribute.
    pass


class TypedParameter:
    """ Typed parameter, `type_name` is the type of the parameter, `param` is the parameter itself. """

    def __init__(self, name: str, param):
        self.type_name = name
        self.param = param


def is_string(e) -> bool:
    """ Returns ``True`` if `e` is a ``str``. """
    return type(e) is str


def is_integer(e) -> bool:
    """ Returns ``True`` if `e` is an ``int``. """
    return type(e) is int


def is_real(e) -> bool:
    """ Returns ``True`` if `e` is a ``float``. """
    return type(e) is float


def is_reference(e) -> bool:
    """ Returns ``True`` if `e` is an :class:`EntityInstanceName`. """
    return type(e) is EntityInstanceName


def is_keyword(e) -> bool:
    """ Returns ``True`` if `e` is a :class:`Keyword`. """
    return type(e) is Keyword


def is_enum(e) -> bool:
    """ Returns ``True`` if `e` is an :class:`Enumeration`. """
    return type(e) is Enumeration


def is_unset_parameter(e) -> bool:
    """ Returns ``True`` if `e` is an unset or omitted parameter (:class:`UnsetParameter`). """
    return type(e) is UnsetParameter


def is_typed_parameter(e) -> bool:
    """ Returns ``True`` if `e` is a :class:`TypedParameter`. """
    return type(e) is TypedParameter


def is_parameter_list(e) -> bool:
    """ Returns ``True`` if `e` is a :class:`ParameterList`. """
    return type(e) is ParameterList


def _to_unicode(s, l, t) -> str:
    return ''.join(chr(int(hexstr, 16)) for hexstr in t[1:-1])


# These _write_... functions should also work with Python primitives like, list, tuple, str, ...
def _write_parameter_list(fp: TextIO, plist: Union[Tuple, List, ParameterList], sep=','):
    fp.write('(')
    first = True
    for p in plist:
        if first:
            first = False
        else:  # write `sep` between parameters, but not after the last parameter
            fp.write(sep)
        if isinstance(p, (tuple, list, ParameterList)):
            _write_parameter_list(fp, p)
        else:
            _write_parameter(fp, p)
    fp.write(')')


ASCII_ONLY_ENCODED_PARAMETERS = {Enumeration, Keyword, EntityInstanceName, UnsetParameter}


def _write_parameter(fp: TextIO, p):
    type_ = type(p)
    if type_ in ASCII_ONLY_ENCODED_PARAMETERS:
        # faster without step encoding
        fp.write(p)
    elif type_ is str:
        fp.write(step_encoded_string(p))
    elif type_ is TypedParameter:
        fp.write(p.type_name)
        fp.write('(')
        _write_parameter(fp, p.param)
        fp.write(')')
    else:
        # TODO: floats may need special treatment for exponential floats like 1e-10 -> 1E-10
        fp.write(str(p))


HEX_16BIT = "{:04X}"
HEX_32BIT = "{:08X}"
EXT_START_16 = '\\X4\\'
EXT_START_32 = '\\X8\\'
EXT_END = "\\X0\\"
EXT_ENCODING = {
    16: HEX_16BIT,
    32: HEX_32BIT,
}


def step_encoded_string(s: str) -> str:
    buffer = []
    encoding = 0  # 0 for no encoding, 16 for 16bit encoding, 32 for 32bit encoding
    for char in s:
        value = ord(char)
        if value < 127:  # just ASCII code
            if encoding:  # stop extended encoding
                buffer.append(EXT_END)
                encoding = 0
            else:
                if char == '\\':  # escaping backslash
                    char = '\\\\'
                elif char == "'":  # escaping apostrophe
                    char = "''"
            buffer.append(char)
        else:  # value > 126
            if not encoding:  # start new extended character sequence
                if value < 65536:  # 16bit character
                    encoding = 16
                    buffer.append(EXT_START_16)
                else:  # 32bit character
                    encoding = 32
                    buffer.append(EXT_START_32)
            elif value >= 65536 and encoding == 16:
                # already extended 16bit encoding, but 32bit encoding is required
                # stop 16bit encoding
                buffer.append(EXT_END)
                # and start 32bit encoding
                encoding = 32
                buffer.append(EXT_START_32)
            buffer.append(EXT_ENCODING[encoding].format(value))
    return ''.join(buffer)


BACKSLASH = '\\'
REVERESE_SOLIDUS = Char(BACKSLASH)
SIGN = Char('+-')
SPACE = Char(' ')
DOT = Char('.')
OMITTED_PARAMETER = Char('*').setParseAction(lambda s, l, t: UnsetParameter(t[0]))
UNSET_PARAMETER = Char('$').setParseAction(lambda s, l, t: UnsetParameter(t[0]))
APOSTROPHE = Char("'")
SPECIAL = Char('!"*$%&.#+,-()?/:;<=>@[]{|}^`~')
LOWER = Char(ascii_lowercase)
UPPER = Char(ascii_uppercase + '_')
DIGIT = Char(nums)
HEX_1 = Char(hexnums)
HEX_2 = Word(hexnums, exact=2)
HEX_4 = Word(hexnums, exact=4)
HEX_8 = Word(hexnums, exact=8)

ENUMERATION = Regex(r'\.[A-Z_][A-Z0-9_]*\.').addParseAction(lambda s, l, t: Enumeration(t[0]))
BINARY = Regex(r'"[0-3][0-9A-Fa-f]*"').addParseAction(lambda s, l, t: int(t[0][2:-1], 16))
INTEGER = Regex(r"[-+]?\d+").addParseAction(lambda s, l, t: int(t[0]))
REAL = Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?").addParseAction(lambda s, l, t: float(t[0]))
ENTITY_INSTANCE_NAME = Regex(r"[#]\d+").setParseAction(lambda s, l, t: EntityInstanceName(t[0]))

ALPHABET = Literal(BACKSLASH + 'P') + UPPER + REVERESE_SOLIDUS
# alphabet= \P?\ - which characters are supported, what do they mean
ARBITRARY = Literal(BACKSLASH + 'X' + BACKSLASH) + HEX_2
CHARACTER = SPACE | DIGIT | LOWER | UPPER | SPECIAL | REVERESE_SOLIDUS | APOSTROPHE
PAGE = Literal(BACKSLASH + 'S' + BACKSLASH) + CHARACTER
# page= \S\? - which characters are supported, what do they mean

NON_Q_CHAR = SPECIAL | DIGIT | SPACE | LOWER | UPPER
END_EXTENDED = Literal(BACKSLASH + 'X0' + BACKSLASH)

extended2 = (Literal(BACKSLASH + 'X2' + BACKSLASH) + OneOrMore(HEX_4) + END_EXTENDED).addParseAction(_to_unicode)
# \X2\00E4\X0\ - encoding ISO 8859 and 10646 (python encoding 'utf-16be')
extended4 = (Literal(BACKSLASH + 'X4' + BACKSLASH) + OneOrMore(HEX_8) + END_EXTENDED).addParseAction(_to_unicode)
# \X4\000000E4\X0\ - encoding ISO 8859 and ISO 10646 (python encoding 'utf-32be')
control_directive = PAGE | ALPHABET | extended2 | extended4 | ARBITRARY

string = Combine(Suppress(APOSTROPHE) + ZeroOrMore(
    NON_Q_CHAR |
    (APOSTROPHE + APOSTROPHE).addParseAction(lambda s, l, t: "'") |
    (REVERESE_SOLIDUS + REVERESE_SOLIDUS).addParseAction(lambda s, l, t: "\\") |
    control_directive) + Suppress(APOSTROPHE))

standard_keyword = Combine(UPPER + ZeroOrMore(UPPER | DIGIT))
user_defined_keyword = Combine('!' + UPPER + ZeroOrMore(UPPER | DIGIT))
keyword = Combine(user_defined_keyword | standard_keyword).setParseAction(lambda s, l, t: Keyword(t[0]))

parameter = Forward()
# parse a list of arguments and convert to a tuple
LIST = (Suppress('(') + Optional(parameter + ZeroOrMore(',' + parameter)) + Suppress(')')).addParseAction(
    lambda s, l, t: ParameterList(t[0::2]))
typed_parameter = (keyword + '(' + parameter + ')').addParseAction(
    lambda s, l, t: TypedParameter(name=t[0], param=t[2]))

untyped_parameter = UNSET_PARAMETER | REAL | INTEGER | string | ENTITY_INSTANCE_NAME | ENUMERATION | BINARY | LIST
parameter <<= typed_parameter | untyped_parameter | OMITTED_PARAMETER
parameter_list = (parameter + ZeroOrMore(',' + parameter)).addParseAction(lambda s, l, t: ParameterList(t[0::2]))

simple_record = keyword + Suppress('(') + Optional(parameter_list) + Suppress(')')
simple_record_list = OneOrMore(simple_record)
simple_entity_instance = ENTITY_INSTANCE_NAME + Suppress('=') + simple_record + Suppress(';')
subsuper_record = '(' + simple_record_list + ')'
complex_entity_instance = ENTITY_INSTANCE_NAME + Suppress('=') + subsuper_record + Suppress(';')
entity_instance = simple_entity_instance | complex_entity_instance
entity_instance_list = ZeroOrMore(entity_instance)

data_section = 'DATA' + Optional(
    Suppress('(') + parameter_list + Suppress(')')) + Suppress(';') + entity_instance_list + 'ENDSEC' + Suppress(';')

header_entity = keyword + Suppress('(') + Optional(parameter_list) + Suppress(')') + Suppress(';')
header_entity_list = OneOrMore(header_entity)
header_section = 'HEADER' + Suppress(';') + header_entity + header_entity + header_entity + Optional(
    header_entity_list) + 'ENDSEC' + Suppress(';')
step_file = 'ISO-10303-21' + Suppress(';') + header_section + OneOrMore(data_section) + 'END-ISO-10303-21' + Suppress(
    ';')

step_file.ignore(cStyleComment)


class Tokens:
    def __init__(self, tokens):
        self.stack = list(reversed(tokens))

    @property
    def lookahead(self):
        return self.stack[-1]

    def pop(self):
        return self.stack.pop()


class Entity:
    """ STEP-file entity, `name` is the type of the entity, `params` are the entity parameters as a
    :class:`ParameterList`.
    """

    def __init__(self, name: str, params: ParameterList):
        self.name: str = name
        self.params: ParameterList = params or ParameterList()

    def write(self, fp: TextIO) -> None:
        fp.write(self.name)
        _write_parameter_list(fp, self.params)


END_OF_INSTANCE = ';\n'


class SimpleEntityInstance:
    """ Simple instance entity, `name` is the instance id as string (e.g. ``'#100'``), `entity` is the :class:`Entity`
    object.
    """

    def __init__(self, name: EntityInstanceName, entity: Entity):
        self.name: EntityInstanceName = name
        self.entity = entity

    def write(self, fp: TextIO) -> None:
        fp.write(self.name + '=')
        self.entity.write(fp)
        fp.write(END_OF_INSTANCE)

    @property
    def is_complex(self) -> bool:
        return False


class ComplexEntityInstance:
    """ A complex entity instance consist of multiple :class:`Entity` objects, `name` is the instance id as string
    (e.g. ``'#100'``)
    """

    def __init__(self, name: EntityInstanceName, entities: List[Entity]):
        self.name: EntityInstanceName = name
        self.entities = entities or list()

    def write(self, fp: TextIO) -> None:
        fp.write(self.name + '=')
        for entity in self.entities:
            entity.write(fp)
        fp.write(END_OF_INSTANCE)

    @property
    def is_complex(self) -> bool:
        return True


EntityInstance = Union[SimpleEntityInstance, ComplexEntityInstance]


class HeaderSection:
    """

    The HEADER section has a fixed structure consisting of 3 to 6 groups in the given order. Except for the data fields
    time_stamp and FILE_SCHEMA all fields may contain empty strings.

    :code:`FILE_DESCRIPTION(description: ParameterList, implementation_level: str)`

        - ``description``
        - ``implementation_level``: The version and conformance option of this file. Possible versions are "1" for the
          original standard back in 1994, ``'2'`` for the technical corrigendum in 1995 and "3" for the second edition.
          The conformance option is either ``'1'`` for internal and ``'2'`` for external mapping of complex entity instances.
          Often, one will find here the value ``'2;1'``. The value ``'2;2'`` enforcing external mapping is also possible
          but only very rarely used. The values ``'3;1'`` and ``'3;2'`` indicate extended STEP-Files as defined in the
          2001 standard with several DATA sections, multiple schemas and ``FILE_POPULATION`` support.

    :code:`FILE_NAME(name: str, time_stamp: str, author: str, organization: ParameterList, preprocessor_version: ParameterList, originating_system: str, authorization: str)`

        - ``name`` of this exchange structure. It may correspond to the name of the file in a file system or reflect
          data in this file. There is no strict rule how to use this field.
        - ``time_stamp`` indicates the time when this file was created. The time is given in the international data time
          format ISO 8601, e.g. 2003-12-27T11:57:53 for 27 of December 2003, 2 minutes to noon time.
        - ``author`` the name and mailing address of the person creating this exchange structure
        - ``organization`` the organization to whom the person belongs to
        - ``preprocessor_version`` the name of the system and its version which produces this STEP-file
        - ``originating_system`` the name of the system and its version which originally created the information
          contained in this STEP-file.
        - ``authorization`` the name and mailing address of the person who authorized this file.

    :code:`FILE_SCHEMA(schema: ParameterList)`

        - Specifies one or several Express schema governing the information in the data section(s). For first edition
          files, only one EXPRESS schema together with an optional ASN.1 object identifier of the schema version can
          be listed here. Second edition files may specify several EXPRESS schema.

    The last three header groups are only valid in second edition files.

    :code:`FILE_POPULATION(governing_schema: str, determination_method: str, governed_sections: ParameterList)` (?)

    Indicating a valid population (set of entity instances) which conforms
    to an EXPRESS schemas. This is done by collecting data from several data_sections and referenced instances from
    other data sections.

        - ``governing_schema``, the EXPRESS schema to which the indicated population belongs to and by which it can
          be validated.
        - ``determination_method`` to figure out which instances belong to the population. Three methods are predefined:
          ``'SECTION_BOUNDARY'``, ``'INCLUDE_ALL_COMPATIBLE'``, and ``'INCLUDE_REFERENCED'``.
        - ``governed_sections``, the data sections whose entity instances fully belongs to the population.

    The concept of FILE_POPULATION is very close to schema_instance of SDAI. Unfortunately, during the
    Standardization process, it was not possible to come to an agreement to merge these concepts. Therefore,
    JSDAI adds further attributes to FILE_POPULATION as intelligent comments to cover all missing information
    from schema_instance. This is supported for both import and export.

    :code:`SECTION_LANGUAGE(language: str)` (?)

    HeaderSection['SECTION_LANGUAGE'] allows assignment of a default language for either all or a specific
    data section. This is needed for those Express schemas that do not provide the capability to specify in which
    language string attributes of entities such as name and description are given.

    :code:`SECTION_CONTEXT(context: ParameterList)` (?)

    Provide the capability to specify additional context information for all
    or single data sections. This can be used e.g. for STEP-APs to indicate which conformance class is covered by
    a particular data section.

    """
    REQUIRED_HEADER_ENTITIES = ('FILE_DESCRIPTION', 'FILE_NAME', 'FILE_SCHEMA')
    OPTIONAL_HEADER_ENTITIES = ('FILE_POPULATION', 'SECTION_LANGUAGE', 'SECTION_CONTENT')

    def __init__(self, entities: Dict = None):
        self.entities: Dict[str: Entity] = entities or OrderedDict()

    def add(self, entity: Entity) -> None:
        """ Add or replace header entry. """
        self.entities[entity.name] = entity

    def __getitem__(self, name: str) -> Entity:
        """ Returns header entry by `name`, raise :class:`KeyError` if not found. """
        return self.entities[name]

    def get(self, name: str) -> Opt[Entity]:
        """ Returns header entry by `name` or ``None`` if not found. """
        try:
            return self.entities[name]
        except KeyError:
            return None

    def set_file_description(self, description: Tuple = None, level: str = '2;1'):
        # FILE_DESCRIPTION(description: ParameterList, implementation_level: str)
        # Tuple -> ParameterList()
        description = ParameterList(description) if description else ParameterList()
        self.add(Entity('FILE_DESCRIPTION', ParameterList((
            ParameterList(description), str(level)
        ))))

    def set_file_name(self, name: str,
                      time_stamp: str = None,
                      author: str = "",
                      organization: Tuple = None,
                      preprocessor_version: Tuple = None,
                      organization_system: str = "",
                      autorization: str = "",
                      ):
        # FILE_NAME(
        #   name: str,
        #   time_stamp: str,
        #   author: str,
        #   organization: ParameterList,
        #   preprocessor_version: ParameterList,
        #   originating_system: str,
        #   authorization: str)
        if time_stamp is None:
            time_stamp = datetime.utcnow().isoformat(timespec='seconds')
        # Tuple -> ParameterList()
        organization = ParameterList(organization) if organization else ParameterList()
        preprocessor_version = ParameterList(preprocessor_version) if preprocessor_version else ParameterList()

        self.add(Entity('FILE_NAME', ParameterList((
            str(name),
            time_stamp,
            str(author),
            organization,
            preprocessor_version,
            str(organization_system),
            str(autorization),
        ))))

    def set_file_schema(self, schema: Tuple):
        # FILE_SCHEMA(schema: ParameterList)
        schema = ParameterList(schema) if schema else ParameterList()
        self.add(Entity('FILE_SCHEMA', schema))

    def write(self, fp: TextIO) -> None:
        def write_entities(names, optional=False):
            for name in names:
                try:
                    entity = self[name]
                except KeyError:
                    if not optional:
                        raise StepFileStructureError(f'Missing required header entity: {name}')
                else:
                    entity.write(fp)
                    fp.write(END_OF_INSTANCE)

        fp.write('HEADER' + END_OF_INSTANCE)
        write_entities(names=HeaderSection.REQUIRED_HEADER_ENTITIES, optional=False)
        write_entities(names=HeaderSection.OPTIONAL_HEADER_ENTITIES, optional=True)
        fp.write('ENDSEC' + END_OF_INSTANCE)


class DataSection:
    """
    The DATA section contains application data according to one specific express schema. The encoding of this data
    follows some simple principles.

    Source of Documentation: https://en.wikipedia.org/wiki/ISO_10303-21

    Every entity instance in the exchange structure is given a unique name in the form ``'#1234'``.
    The instance name must consist of a positive number (>0) and is typically smaller than 263. The instance name
    is only valid locally within the STEP-file. If the same content is exported again from a system the instance
    names may be different for the same instances. The instance name is also used to reference other entity
    instances through attribute values or aggregate members. The referenced instance may be defined before or
    after the current instance.

    Instances of single entity data types are represented by writing the name of the entity in capital letters and then
    followed by the attribute values in the defined order within parentheses. See e.g. ``#16=PRODUCT(...)`` above.

    Instances of complex entity data types are represented in the STEP file by using either the internal mapping or
    the external mapping.
    External mapping has always to be used if the complex entity instance consist of more than one leaf entity.
    In this case all the single entity instance values are given independently from each other in alphabetical
    order as defined above with all entity values grouped together in parentheses.
    Internal mapping is used by default for conformance option 1 when the complex entity instance consists of
    only one leaf entity. The encoding is similar to the one of a single entity instance with the additional order
    given by the subtype definition.

    Mapping of attribute values:

    Only explicit attributes get mapped. Inverse, Derived and re-declared attributes are not listed since their
    values can be deduced from the other ones. Unset attribute values are given as ``$``.
    Explicit attributes which got re-declared as derived in a subtype are encoded as ``*`` in the position of the
    supertype attribute.

    Mapping of other data types:

    Enumeration, boolean and logical values are given in capital letters with a leading and trailing dot such as
    ``.TRUE.``.
    String values are given in ``'``. For characters with a code greater than 126 a special encoding is used. The
    character sets as defined in ISO 8859 and 10646 are supported. Note that typical 8 (e.g. west European) or
    16 (Unicode) bit character sets cannot directly be taken for STEP-file strings. They have to be decoded
    in a very special way.
    Integers and real values are used identical to typical programming languages
    Binary values (bit sequences) are encoded as hexadecimal and surrounded by double quotes, with a leading
    character indicating the number of unused bits (0, 1, 2, or 3) followed by uppercase hexadecimal encoding of
    data. It is important to note that the entire binary value is encoded as a single hexadecimal number, with
    the highest order bits in the first hex character and the lowest order bits in the last one.
    The elements of aggregates (SET, BAG, LIST, ARRAY) are given in parentheses, separated by ``,``.
    Care has to be taken for select data types based on defined data types. Here the name of the defined data
    type gets mapped too.

    """

    def __init__(self, params: ParameterList = None, instances: Dict = None):
        self.parameter = params or ParameterList()
        self.instances: Dict[EntityInstanceName, EntityInstance] = instances or OrderedDict()

    def __iter__(self):
        return self.instances.values()

    def append(self, instance: EntityInstance) -> None:
        """
        Append new entity `instance`.

        Args:
            instance: entity instance

        """
        self.instances[instance.name] = instance

    def names(self) -> Iterable[EntityInstanceName]:
        """ Returns iterable of entity instance names. """
        return self.instances.keys()

    def sorted_names(self) -> List[EntityInstanceName]:
        """ Returns sorted list if entity instance names. """
        return sorted(self.instances.keys(), key=lambda e: int(e[1:]))

    def sorted_instances(self) -> Iterable[EntityInstance]:
        """ Returns iterable of entity instances sorted by name. """
        return (self.instances[key] for key in self.sorted_names())

    def __getitem__(self, name: str) -> EntityInstance:
        """ Returns instance by `name`, raise :class:`KeyError` if not found. """
        return self.instances[name]

    def __len__(self) -> int:
        """ Returns count of instances. """
        return len(self.instances)

    def get(self, name: str) -> Opt[EntityInstance]:
        """ Returns instance by `name` of ``None`` if not found. """
        try:
            return self.instances[name]
        except KeyError:
            return None

    def write(self, fp: TextIO):
        fp.write('DATA')
        if len(self.parameter):
            _write_parameter_list(fp, self.parameter)
        fp.write(END_OF_INSTANCE)
        for instance in self.instances.values():
            instance.write(fp)
        fp.write('ENDSEC' + END_OF_INSTANCE)


class StepFile:
    """ STEP physical file representation (STEP-file).

    A STEP-File has one :class:`HeaderSection`, and at least one :class:`DataSection`.

    """

    def __init__(self):
        self.header = HeaderSection()
        # multiple data sections only supported by ISO 10303-21:2002
        # most files in the wild, don't use multiple data sections!
        self.data: List[DataSection] = list()
        self._linked_data_sections: ChainMap = None

    def __getitem__(self, name: EntityInstanceName):
        """ Returns :class:`EntityInstance` by instance `name`. Searches all data sections if more than one exist.

        Args:
            name: entity instance name as string e.g. ``'#100'``

        Raises:
              KeyError: instance `id` not found

        """
        if self._linked_data_sections is None:
            self._rebuild_chain_map()
        return self._linked_data_sections[name]

    def __iter__(self):
        """ Returns unsorted iterable of all instance entities of all data sections."""
        for ds in self.data:
            yield from iter(ds)

    def get(self, name: EntityInstanceName) -> Opt[EntityInstance]:
        """ Returns :class:`EntityInstance` by instance `name` or ``None`` if not found. Searches all data sections
        if more than one exist.

        Args:
            name: entity instance name as string e.g. ``'#100'``

        """
        try:
            return self.__getitem__(name)
        except KeyError:
            return None

    def _rebuild_chain_map(self) -> None:
        """ Rebuild chain map for searching across multiple data sections.
        """
        self._linked_data_sections = ChainMap(*[ds.instances for ds in self.data])

    def append(self, data: DataSection) -> None:
        """
        Append new data section `data`.

        Args:
            data: data section

        """
        self.data.append(data)
        self._rebuild_chain_map()

    def new_data_section(self, params: Iterable = None):
        params = ParameterList(params) if params else ParameterList()
        new_section = DataSection(params=params)
        self.append(new_section)
        return new_section

    def write(self, fp: TextIO) -> None:
        fp.write('ISO-10303-21' + END_OF_INSTANCE)
        self.header.write(fp)
        for data in self.data:
            data.write(fp)
        fp.write('END-ISO-10303-21' + END_OF_INSTANCE)


def _parse_entity(tokens: Tokens) -> Entity:
    name = tokens.pop()
    if isinstance(tokens.lookahead, ParameterList):  # optional parameter list
        params = tokens.pop()
    else:
        params = None
    return Entity(name=name, params=params)


def _parse_instance(tokens: Tokens) -> EntityInstance:
    instance_id = tokens.pop()
    if tokens.lookahead == '(':  # Complex Instance Entity
        tokens.pop()  # (
        entities = list()
        while tokens.lookahead != ')':
            entity = _parse_entity(tokens)
            entities.append(entity)
        tokens.pop()  # )
        return ComplexEntityInstance(name=instance_id, entities=entities)
    else:
        entity = _parse_entity(tokens)
        return SimpleEntityInstance(name=instance_id, entity=entity)


def _parse_header(tokens: Tokens) -> HeaderSection:
    header = HeaderSection()
    t = tokens.pop()
    assert t == 'HEADER'
    while tokens.lookahead != 'ENDSEC':
        entity = _parse_entity(tokens)
        header.add(entity)
    tokens.pop()  # ENDSEC
    return header


def _parse_data_section(tokens: Tokens) -> DataSection:
    data = DataSection()
    t = tokens.pop()
    assert t == 'DATA'
    # optional parameter list of data section: DATA(arg1, list1, ...)
    if isinstance(tokens.lookahead, ParameterList):
        data.parameter = tokens.pop()

    while tokens.lookahead != 'ENDSEC':
        instance = _parse_instance(tokens)
        data.append(instance)
    tokens.pop()  # ENDSEC
    return data


def _parse_step_file(tokens) -> 'StepFile':
    step = StepFile()
    tokens = Tokens(tokens)

    t = tokens.pop()
    assert t == 'ISO-10303-21'

    step.header = _parse_header(tokens)
    while tokens.lookahead != 'END-ISO-10303-21':
        # multiple data sections support
        step.append(_parse_data_section(tokens))

    return step


# loading and storing API similar json package
def loads(s: str) -> StepFile:
    """ Load STEP-file (ISO 10303-21) from unicode string.

    Decoding for special characters > 126 to unicode characters according to ISO 10303-21 standard will
    be applied.

    Args:
        s: STEP-file content as unicode string

    """
    tokens = step_file.parseString(s)
    return _parse_step_file(tokens)


def load(fp: TextIO) -> StepFile:
    """ Load STEP-file (ISO 10303-21) from text stream.

    A special encoding form characters > 126 is applied in STEP-Files, therefore an encoding setting at opening files
    is not necessary, reading as ``'ascii'`` works fine. Decoding of this special characters will be applied.

    Args:
        fp: STEP-file content as text stream yielding unicode strings

    """
    content = fp.read()
    return loads(content)


def dump(data: StepFile, fp: TextIO) -> None:
    """
    Serialize `data` to a STEP-file (ISO 10303-21) formatted stream to ``fp`` (a :meth:`write`-supporting
    file-like object).

    File encoding should be ``'iso-8859-1'`` but can also be ``'ascii'``, because ISO 10303-21 requires special encoding
    for characters > 126 into characters < 127 as unicode compatible characters, which should be compatible with most
    encodings, but don't use 16-bit encodings!

    Args:
        data: step file data object
        fp: text stream

    """
    data.write(fp)


def dumps(data: StepFile) -> str:
    """
    Serialize `data` to a STEP-file (ISO 10303-21) formatted ``str``.

    Special encoding for characters > 126 into characters < 127 as unicode compatible characters according to
    ISO 10303-21 standard will be applied.

    Args:
        data: step file data object

    """
    from io import StringIO
    fp = StringIO()
    data.write(fp)
    s = fp.getvalue()
    fp.close()
    return s
