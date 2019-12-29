# Created: 26.12.2019
# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
from typing import List, TextIO, Dict, Union, Iterable
from typing import Optional as Opt

from collections import OrderedDict, ChainMap

from pyparsing import (
    nums, hexnums, Literal, Char, Word, Regex, Optional, Forward, ZeroOrMore, OneOrMore,
    Combine, Suppress, cStyleComment,
)
from string import ascii_lowercase, ascii_uppercase


class ParameterList(tuple):
    pass


class EntityInstanceName(str):
    pass


def is_reference(e) -> bool:
    return isinstance(e, EntityInstanceName)


class Keyword(str):
    pass


class Enumeration(str):
    pass


def is_enum(e) -> bool:
    return isinstance(e, Enumeration)


class UnsetParameter(str):
    pass


def is_unset_parameter(e) -> bool:
    return isinstance(e, UnsetParameter)


class TypedParameter:
    def __init__(self, name: str, param):
        self.type_name = name
        self.param = param


def is_typed_parameter(e) -> bool:
    return isinstance(e, TypedParameter)


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
# enum: .ENUM.
#   Enumeration, boolean and logical values are given in capital letters with a leading and trailing dot such as
#   ".TRUE.".
#
# instance_name: #1234
#   Every entity instance in the exchange structure is given a unique name in the form "#1234". The instance name must
#   consist of a positive number (>0) and is typically smaller than 263. The instance name is only valid locally within
#   the STEP-file (?across multiple data sections? - assume: yes!).
#   If the same content is exported again from a system the instance names may be different for the same
#   instances. The instance name is also used to reference other entity instances through attribute values or aggregate
#   members. The referenced instance may be defined before or after the current instance.
#
# list: (arg1, list2, ...)
#   The elements of aggregates (SET, BAG, LIST, ARRAY) are given in parentheses, separated by ",".

def _to_unicode(s, l, t) -> str:
    return ''.join(chr(int(hexstr, 16)) for hexstr in t[1:-1])


BACKSLASH = '\\'
reverse_solidus = Char(BACKSLASH)
sign = Char('+-')
space = Char(' ')
dot = Char('.')
omitted_parameter = Char('*').setParseAction(lambda s, l, t: UnsetParameter(t[0]))
unset_parameter = Char('$').setParseAction(lambda s, l, t: UnsetParameter(t[0]))
apostrophe = Char("'")
special = Char('!"*$%&.#+,-()?/:;<=>@[]{|}^`~')
lower = Char(ascii_lowercase)
upper = Char(ascii_uppercase + '_')
digit = Char(nums)
enumeration = Regex(r'\.[A-Z_][A-Z0-9_]*\.').addParseAction(lambda s, l, t: Enumeration(t[0]))
integer = Regex(r"[-+]?\d+").addParseAction(lambda s, l, t: int(t[0]))
real = Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?").addParseAction(lambda s, l, t: float(t[0]))
entity_instance_name = Regex(r"[#]\d+").setParseAction(lambda s, l, t: EntityInstanceName(t[0]))
binary = Regex(r'"[0-3][0-9A-Fa-f]*"').addParseAction(lambda s, l, t: int(t[0][2:-1], 16))

hex1 = Char(hexnums)
hex2 = Word(hexnums, exact=2)
hex4 = Word(hexnums, exact=4)
hex8 = Word(hexnums, exact=8)


alphabet = Literal(BACKSLASH + 'P') + upper + reverse_solidus
# alphabet= \P?\ - which characters are supported, what do they mean
arbitrary = Literal(BACKSLASH + 'X' + BACKSLASH) + hex2
character = space | digit | lower | upper | special | reverse_solidus | apostrophe
page = Literal(BACKSLASH + 'S' + BACKSLASH) + character
# page= \S\? - which characters are supported, what do they mean

non_q_char = special | digit | space | lower | upper
end_extended = Literal(BACKSLASH + 'X0' + BACKSLASH)
extended2 = (Literal(BACKSLASH + 'X2' + BACKSLASH) + OneOrMore(hex4) + end_extended).addParseAction(_to_unicode)
# \X2\00E4\X0\ - encoding ISO 8859 and 10646 (python encoding 'utf-16be')
extended4 = (Literal(BACKSLASH + 'X4' + BACKSLASH) + OneOrMore(hex8) + end_extended).addParseAction(_to_unicode)
# \X4\000000E4\X0\ - encoding ISO 8859 and ISO 10646 (python encoding 'utf-32be')
control_directive = page | alphabet | extended2 | extended4 | arbitrary

string = Combine(Suppress(apostrophe) + ZeroOrMore(
    non_q_char |
    (apostrophe + apostrophe).addParseAction(lambda s, l, t: "'") |
    (reverse_solidus + reverse_solidus).addParseAction(lambda s, l, t: "\\") |
    control_directive) + Suppress(apostrophe))

standard_keyword = Combine(upper + ZeroOrMore(upper | digit))
user_defined_keyword = Combine('!' + upper + ZeroOrMore(upper | digit))
keyword = Combine(user_defined_keyword | standard_keyword).setParseAction(lambda s, l, t: Keyword(t[0]))

parameter = Forward()
# parse a list of arguments and convert to a tuple
list_ = (Suppress('(') + Optional(parameter + ZeroOrMore(',' + parameter)) + Suppress(')')).addParseAction(
    lambda s, l, t: ParameterList(t[0::2]))
typed_parameter = (keyword + '(' + parameter + ')').addParseAction(
    lambda s, l, t: TypedParameter(name=t[0], param=t[2]))

# omitted argument: $ or *
#     Source: https://en.wikipedia.org/wiki/ISO_10303-21
#     Unset attribute values are given as "$".
#     Explicit attributes which got re-declared as derived in a subtype are encoded as "*" in the position of the
#     supertype attribute.

untyped_parameter = unset_parameter | real | integer | string | entity_instance_name | enumeration | binary | list_
parameter <<= typed_parameter | untyped_parameter | omitted_parameter
parameter_list = (parameter + ZeroOrMore(',' + parameter)).addParseAction(lambda s, l, t: ParameterList(t[0::2]))

simple_record = keyword + Suppress('(') + Optional(parameter_list) + Suppress(')')
simple_record_list = OneOrMore(simple_record)
simple_entity_instance = entity_instance_name + Suppress('=') + simple_record + Suppress(';')
subsuper_record = '(' + simple_record_list + ')'
complex_entity_instance = entity_instance_name + Suppress('=') + subsuper_record + Suppress(';')
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
    def __init__(self, name: str, params: ParameterList):
        self.name = name
        self.params = params or ParameterList()


class SimpleEntityInstance:
    def __init__(self, id: EntityInstanceName, entity: Entity):
        self.id: EntityInstanceName = id
        self.entity = entity

    @property
    def is_complex(self) -> bool:
        return False


class ComplexEntityInstance:
    def __init__(self, id: EntityInstanceName, entities: List[Entity]):
        self.id: EntityInstanceName = id
        self.entities = entities or list()

    @property
    def is_complex(self) -> bool:
        return True


EntityInstance = Union[SimpleEntityInstance, ComplexEntityInstance]


class HeaderSection:
    """

    The HEADER section has a fixed structure consisting of 3 to 6 groups in the given order. Except for the data fields
    time_stamp and FILE_SCHEMA all fields may contain empty strings.

    HeaderSection['FILE_DESCRIPTION']
        - description
        - implementation_level. The version and conformance option of this file. Possible versions are "1" for the
          original standard back in 1994, "2" for the technical corrigendum in 1995 and "3" for the second edition.
          The conformance option is either "1" for internal and "2" for external mapping of complex entity instances.
          Often, one will find here the value __'2;1'__. The value '2;2' enforcing external mapping is also possible
          but only very rarely used. The values '3;1' and '3;2' indicate extended STEP-Files as defined in the 2001
          standard with several DATA sections, multiple schemas and FILE_POPULATION support.

    HeaderSection['FILE_NAME']
        - name of this exchange structure. It may correspond to the name of the file in a file system or reflect data
          in this file. There is no strict rule how to use this field.
        - time_stamp indicates the time when this file was created. The time is given in the international data time
          format ISO 8601, e.g. 2003-12-27T11:57:53 for 27 of December 2003, 2 minutes to noon time.
        - author the name and mailing address of the person creating this exchange structure
        - organization the organization to whom the person belongs to
        - preprocessor_version the name of the system and its version which produces this STEP-file
        - originating_system the name of the system and its version which originally created the information contained
          in this STEP-file.
        - authorization the name and mailing address of the person who authorized this file.

    HeaderSection['FILE_SCHEMA']
        - Specifies one or several Express schema governing the information in the data section(s). For first edition
          files, only one EXPRESS schema together with an optional ASN.1 object identifier of the schema version can
          be listed here. Second edition files may specify several EXPRESS schema.

    The last three header groups are only valid in second edition files.

    HeaderSection['FILE_POPULATION'], indicating a valid population (set of entity instances) which conforms
        to an EXPRESS schemas. This is done by collecting data from several data_sections and referenced instances from
        other data sections.
        - governing_schema, the EXPRESS schema to which the indicated population belongs to and by which it can
          be validated.
        - determination_method to figure out which instances belong to the population. Three methods are predefined:
          SECTION_BOUNDARY, INCLUDE_ALL_COMPATIBLE, and INCLUDE_REFERENCED.
        - governed_sections, the data sections whose entity instances fully belongs to the population.
        - The concept of FILE_POPULATION is very close to schema_instance of SDAI. Unfortunately, during the
          standardization process, it was not possible to come to an agreement to merge these concepts. Therefore,
          JSDAI adds further attributes to FILE_POPULATION as intelligent comments to cover all missing information
          from schema_instance. This is supported for both import and export.

    HeaderSection['SECTION_LANGUAGE'] allows assignment of a default language for either all or a specific
         data section. This is needed for those Express schemas that do not provide the capability to specify in which
         language string attributes of entities such as name and description are given.

    HeaderSection['SECTION_CONTEXT'] provide the capability to specify additional context information for all
         or single data sections. This can be used e.g. for STEP-APs to indicate which conformance class is covered by
         a particular data section.

    """
    def __init__(self):
        self.entities: OrderedDict[str: Entity] = OrderedDict()

    def append(self, entity: Entity) -> None:
        self.entities[entity.name] = entity

    def __getitem__(self, name: str) -> Entity:
        return self.entities[name]

    def get(self, name: str) -> Opt[Entity]:
        try:
            return self.entities[name]
        except KeyError:
            return None


class DataSection:
    """
    The DATA section contains application data according to one specific express schema. The encoding of this data
    follows some simple principles.

    Source of Documentation: https://en.wikipedia.org/wiki/ISO_10303-21

    Instance name: Every entity instance in the exchange structure is given a unique name in the form <#1234>.
        The instance name must consist of a positive number (>0) and is typically smaller than 263. The instance name
        is only valid locally within the STEP-file. If the same content is exported again from a system the instance
        names may be different for the same instances. The instance name is also used to reference other entity
        instances through attribute values or aggregate members. The referenced instance may be defined before or
        after the current instance.

    Instances of single entity data types are represented by writing the name of the entity in capital letters and then
        followed by the attribute values in the defined order within parentheses. See e.g. <#16=PRODUCT(...)> above.

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
        values can be deduced from the other ones. Unset attribute values are given as <$>.
        Explicit attributes which got re-declared as derived in a subtype are encoded as <*> in the position of the
        supertype attribute.

    Mapping of other data types:
        Enumeration, boolean and logical values are given in capital letters with a leading and trailing dot such as
        <.TRUE.>.
        String values are given in <'>. For characters with a code greater than 126 a special encoding is used. The
        character sets as defined in ISO 8859 and 10646 are supported. Note that typical 8 (e.g. west European) or
        16 (Unicode) bit character sets cannot directly be taken for STEP-file strings. They have to be decoded
        in a very special way.
        Integers and real values are used identical to typical programming languages
        Binary values (bit sequences) are encoded as hexadecimal and surrounded by double quotes, with a leading
        character indicating the number of unused bits (0, 1, 2, or 3) followed by uppercase hexadecimal encoding of
        data. It is important to note that the entire binary value is encoded as a single hexadecimal number, with
        the highest order bits in the first hex character and the lowest order bits in the last one.
        The elements of aggregates (SET, BAG, LIST, ARRAY) are given in parentheses, separated by <,>.
        Care has to be taken for select data types based on defined data types. Here the name of the defined data
        type gets mapped too.

    """
    def __init__(self):
        self.parameter = ParameterList()
        self.instances: Dict[EntityInstanceName, EntityInstance] = OrderedDict()

    def append(self, instance: EntityInstance) -> None:
        self.instances[instance.id] = instance

    def names(self) -> Iterable[EntityInstanceName]:
        return self.instances.keys()

    def sorted_names(self) -> List[EntityInstanceName]:
        return sorted(self.instances.keys(), key=lambda e: int(e[1:]))

    def instances(self) -> Iterable[EntityInstance]:
        return self.instances.values()

    def sorted_instances(self) -> Iterable[EntityInstance]:
        return (self.instances[key] for key in self.sorted_names())

    def __getitem__(self, name: EntityInstanceName) -> EntityInstance:
        return self.instances[name]

    def __len__(self):
        return len(self.instances)

    def get(self, name: EntityInstanceName) -> Opt[EntityInstance]:
        try:
            return self.instances[name]
        except KeyError:
            return None


class StepFile:
    """ STEP physical file representation (STEP-file)

    Source of Documentation: https://en.wikipedia.org/wiki/ISO_10303-21

    STEP-File is the most widely used data exchange form of STEP. ISO 10303 can represent 3D objects in Computer-aided
    design (CAD) and related information. Due to its ASCII structure, a STEP-file is easy to read, with typically one
    instance per line. The format of a STEP-File is defined in ISO 10303-21 Clear Text Encoding of the Exchange Structure.

    ISO 10303-21 defines the encoding mechanism for representing data conforming to a particular schema in the
    EXPRESS data modeling language specified in ISO 10303-11. A STEP-File is also called p21-File and STEP Physical
    File. The file extensions .stp and .step indicate that the file contains data conforming to STEP Application
    Protocols while the extension .p21 should be used for all other purposes.

    A STEP-File has one :class:`HeaderSection`, and at least one :class:`DataSection`.

    """
    def __init__(self):
        self.header = HeaderSection()
        # multiple data sections only supported by ISO 10303-21:2002
        # most files in the wild, don't use multiple data sections!
        self.data: List[DataSection] = list()
        self._chain_map: ChainMap = None

    def __getitem__(self, id: EntityInstanceName):
        if self._chain_map is None:
            self.rebuild_chain_map()
        return self._chain_map[id]

    def get(self, id: EntityInstanceName) -> Opt[EntityInstance]:
        try:
            return self.__getitem__(id)
        except KeyError:
            return None

    def rebuild_chain_map(self):
        self._chain_map = ChainMap(*self.data)


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
        return ComplexEntityInstance(id=instance_id, entities=entities)
    else:
        entity = _parse_entity(tokens)
        return SimpleEntityInstance(id=instance_id, entity=entity)


def _parse_header(tokens: Tokens) -> HeaderSection:
    header = HeaderSection()
    t = tokens.pop()
    assert t == 'HEADER'
    while tokens.lookahead != 'ENDSEC':
        entity = _parse_entity(tokens)
        header.append(entity)
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
        step.data.append(_parse_data_section(tokens))

    return step


def load_string(s: str) -> 'StepFile':
    """ Load STEP-file from unicode string. """
    tokens = step_file.parseString(s)
    return _parse_step_file(tokens)


def load_file(filename: str) -> StepFile:
    """ Load STEP-file from filesystem.

    Special encoding of strings is applied, therefore an encoding setting at opening files is not necessary, reading
    as 'ascii' works fine.

    """
    with open(filename, mode='rt') as fp:
        content = fp.read()
        return load_string(content)


def load_stream(stream: TextIO) -> StepFile:
    """ Load STEP-file from text stream. """
    content = stream.read()
    return load_string(content)
