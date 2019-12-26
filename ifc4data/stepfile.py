# Created: 26.12.2019
# Copyright (c) 2019 Manfred Moitzi
# License: MIT License

from pyparsing import (
    nums, hexnums, Literal, Char, Word, Regex, Optional, Forward, ZeroOrMore, OneOrMore,
    Combine, Suppress,
)
from string import ascii_lowercase, ascii_uppercase


class ParameterList(tuple):
    pass


class EntityInstanceName(str):
    pass


class Keyword(str):
    pass


BACKSLASH = '\\'
reverse_solidus = Char(BACKSLASH)
sign = Char('+-')
space = Char(' ')
dot = Char('.')
omitted_parameter = Char('*')
apostrophe = Char("'")
special = Char('!"*$%&.#+,-()?/:;<=>@[]{|}^`~')
lower = Char(ascii_lowercase)
upper = Char(ascii_uppercase + '_')
digit = Char(nums)
real = Regex(r"[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?")
integer = Regex(r"[-+]?\d+")
entity_instance_name = Regex(r"[#]\d+").setParseAction(lambda s, l, t: EntityInstanceName(t[0]))

hex1 = Char(hexnums)
hex2 = Word(hexnums, exact=2)
hex4 = Word(hexnums, exact=4)
hex8 = Word(hexnums, exact=8)

binary = '"' + Char('0123') + ZeroOrMore(hex1) + '"'
alphabet = Literal(BACKSLASH + 'P') + upper + reverse_solidus
arbitrary = Literal(BACKSLASH + 'X' + BACKSLASH) + hex2
character = space | digit | lower | upper | special | reverse_solidus | apostrophe
enumeration = Combine(dot + upper + ZeroOrMore(upper | digit) + dot)
page = Literal(BACKSLASH + 'S' + BACKSLASH) + character

non_q_char = special | digit | space | lower | upper
end_extended = Literal(BACKSLASH + 'X0' + BACKSLASH)
extended2 = Literal(BACKSLASH + 'X2' + BACKSLASH) + OneOrMore(hex4) + end_extended
extended4 = Literal(BACKSLASH + 'X4' + BACKSLASH) + OneOrMore(hex8) + end_extended
control_directive = page | alphabet | extended2 | extended4 | arbitrary
string = Combine(Suppress(apostrophe) + ZeroOrMore(
    non_q_char | (apostrophe + apostrophe) | (reverse_solidus + reverse_solidus) | control_directive) + Suppress(
    apostrophe))

standard_keyword = Combine(upper + ZeroOrMore(upper | digit))
user_defined_keyword = Combine('!' + upper + ZeroOrMore(upper | digit))
keyword = Combine(user_defined_keyword | standard_keyword).setParseAction(lambda s, l, t: Keyword(t[0]))

parameter = Forward()
# parse a list of arguments and convert to a tuple
list_ = (Suppress('(') + Optional(parameter + ZeroOrMore(',' + parameter)) + Suppress(')')).addParseAction(
    lambda s, l, t: ParameterList(t[0::2]))
typed_parameter = keyword + '(' + parameter + ')'
untyped_parameter = '$' | integer | real | string | entity_instance_name | enumeration | binary | list_
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

# Included just for documentation:
EXTENDED_BACKUS_NAUR_FORM = r"""
; ISO 10303-21:2002

alphabet = reverse_solidus 'P' upper reverse_solidus .
apostrophe = '''' .
arbitrary = reverse_solidus 'X' reverse_solidus hex_one .
binary = '"' ( '0' | '1' | '2' | '3' ) { hex } '"' .
character = space | digit | lower | upper | special | reverse_solidus | apostrophe .
complex_entity_instance = entity_instance_name '=' subsuper_record ';' .
control_directive = page | alphabet | extended2 | extended4 | arbitrary .
data_section = 'DATA' [ '(' parameter_list ')' ] ';' entity_instance_list 'ENDSEC;' .
digit = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' .
end_extended = reverse_solidus 'X0' reverse_solidus .
entity_instance = simple_entity_instance | complex_entity_instance .
entity_instance_list = { entity_instance } .
entity_instance_name = '#' digit { digit } .
enumeration = '.' upper { upper | digit } '.' .
exchange_file = 'ISO-10303-21;' header_section data_section { data_section } 'END-ISO-10303-21;' .
extended2 = reverse_solidus 'X2' reverse_solidus hex_two { hex_two } end_extended .
extended4 = reverse_solidus 'X4' reverse_solidus hex_four { hex_four } end_extended .
header_entity = keyword '(' [ parameter_list ] ')' ';' .
header_entity_list = header_entity { header_entity } .
header_section = 'HEADER;' header_entity header_entity header_entity [header_entity_list] 'ENDSEC;' .
hex = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' .
hex_four = hex_two hex_two .
hex_one = hex hex .
hex_two = hex_one hex_one .
integer = [ sign ] digit { digit } .
keyword = user_defined_keyword | standard_keyword .
list = '(' [ parameter { ',' parameter } ] ')' .
lower = 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' .
non_q_char = special | digit | space | lower | upper .
omitted_parameter = '*' .
page = reverse_solidus 'S' reverse_solidus character .
parameter = typed_parameter | untyped_parameter | omitted_parameter .
parameter_list = parameter { ',' parameter } .
real = [ sign ] digit { digit } '.' { digit } [ 'E' [ sign ] digit { digit } ] .
reverse_solidus = '\' .
sign = '+' | '-' .
simple_entity_instance = entity_instance_name '=' simple_record ';' .
simple_record = keyword '(' [ parameter_list ] ')' .
simple_record_list = simple_record { simple_record } .
space = ' ' .
special = '!' | '"' | '*' | '$' | '%' | '&' | '.' | '#' | '+' | ',' | '-' | '(' | ')' | '?' | '/' | ':' | ';' | '<' | '=' | '>' | '@' | '[' | ']' | '{' | '|' | '}' | '^' | '`' | '~' .
standard_keyword = upper { upper | digit } .
string = '''' { non_q_char | apostrophe apostrophe | reverse_solidus reverse_solidus | control_directive } '''' .
subsuper_record = '(' simple_record_list ')' .
typed_parameter = keyword '(' parameter ')' .
untyped_parameter = '$' | integer | real | string | entity_instance_name | enumeration | binary | list .
upper = 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | '_' .
user_defined_keyword = '!' upper { upper | digit } .
"""
