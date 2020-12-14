# Created: 06.01.2020
# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

from string import ascii_letters
from typing import Iterable

from pyparsing import *
from . import ast

ABS = Keyword('ABS')
ABSTRACT = Keyword('ABSTRACT')
ACOS = Keyword('ACOS')
AGGREGATE = Keyword('AGGREGATE')
ALIAS = Keyword('ALIAS')
AND = Keyword('AND')
ANDOR = Keyword('ANDOR')
ARRAY = Keyword('ARRAY')
AS = Keyword('AS')
ASIN = Keyword('ASIN')
ATAN = Keyword('ATAN')
BAG = Keyword('BAG')
BASED_ON = Keyword('BASED_ON')
BEGIN = Keyword('BEGIN')
BINARY = Keyword('BINARY')
BLENGTH = Keyword('BLENGTH')
BOOLEAN = Keyword('BOOLEAN')
BY = Keyword('BY')
CASE = Keyword('CASE')
CONSTANT = Keyword('CONSTANT')
CONST_E = Keyword('CONST_E')
COS = Keyword('COS')
DERIVE = Keyword('DERIVE')
DIV = Keyword('DIV')
ELSE = Keyword('ELSE')
END = Keyword('END')
END_ALIAS = Keyword('END_ALIAS')
END_CASE = Keyword('END_CASE')
END_CONSTANT = Keyword('END_CONSTANT')
END_ENTITY = Keyword('END_ENTITY')
END_FUNCTION = Keyword('END_FUNCTION')
END_IF = Keyword('END_IF')
END_LOCAL = Keyword('END_LOCAL')
END_PROCEDURE = Keyword('END_PROCEDURE')
END_REPEAT = Keyword('END_REPEAT')
END_RULE = Keyword('END_RULE')
END_SCHEMA = Keyword('END_SCHEMA')
END_SUBTYPE_CONSTRAINT = Keyword('END_SUBTYPE_CONSTRAINT')
END_TYPE = Keyword('END_TYPE')
ENTITY = Keyword('ENTITY')
ENUMERATION = Keyword('ENUMERATION')
ESCAPE = Keyword('ESCAPE')
EXISTS = Keyword('EXISTS')
EXTENSIBLE = Keyword('EXTENSIBLE')
EXP = Keyword('EXP')
FALSE = Keyword('FALSE')
FIXED = Keyword('FIXED')
FOR = Keyword('FOR')
FORMAT = Keyword('FORMAT')
FROM = Keyword('FROM')
FUNCTION = Keyword('FUNCTION')
GENERIC = Keyword('GENERIC')
GENERIC_ENTITY = Keyword('GENERIC_ENTITY')
HIBOUND = Keyword('HIBOUND')
HIINDEX = Keyword('HIINDEX')
IF = Keyword('IF')
IN = Keyword('IN')
INSERT = Keyword('INSERT')
INTEGER = Keyword('INTEGER')
INVERSE = Keyword('INVERSE')
LENGTH = Keyword('LENGTH')
LIKE = Keyword('LIKE')
LIST = Keyword('LIST')
LOBOUND = Keyword('LOBOUND')
LOCAL = Keyword('LOCAL')
LOG = Keyword('LOG')
LOG10 = Keyword('LOG10')
LOG2 = Keyword('LOG2')
LOGICAL = Keyword('LOGICAL')
LOINDEX = Keyword('LOINDEX')
MOD = Keyword('MOD')
NOT = Keyword('NOT')
NUMBER = Keyword('NUMBER')
NVL = Keyword('NVL')
ODD = Keyword('ODD')
OF = Keyword('OF')
ONEOF = Keyword('ONEOF')
OPTIONAL = Keyword('OPTIONAL')
OR = Keyword('OR')
OTHERWISE = Keyword('OTHERWISE')
PI = Keyword('PI')
PROCEDURE = Keyword('PROCEDURE')
QUERY = Keyword('QUERY')
REAL = Keyword('REAL')
REFERENCE = Keyword('REFERENCE')
REMOVE = Keyword('REMOVE')
RENAMED = Keyword('RENAMED')
REPEAT = Keyword('REPEAT')
RETURN = Keyword('RETURN')
ROLESOF = Keyword('ROLESOF')
RULE = Keyword('RULE')
SCHEMA = Keyword('SCHEMA')
SELECT = Keyword('SELECT')
SELF = Keyword('SELF')
SET = Keyword('SET')
SIN = Keyword('SIN')
SIZEOF = Keyword('SIZEOF')
SKIP = Keyword('SKIP')
SQRT = Keyword('SQRT')
STRING = Keyword('STRING')
SUBTYPE = Keyword('SUBTYPE')
SUBTYPE_CONSTRAINT = Keyword('SUBTYPE_CONSTRAINT')
SUPERTYPE = Keyword('SUPERTYPE')
TAN = Keyword('TAN')
THEN = Keyword('THEN')
TO = Keyword('TO')
TOTAL_OVER = Keyword('TOTAL_OVER')
TRUE = Keyword('TRUE')
TYPE = Keyword('TYPE')
TYPEOF = Keyword('TYPEOF')
UNIQUE = Keyword('UNIQUE')
UNKNOWN = Keyword('UNKNOWN')
UNTIL = Keyword('UNTIL')
USE = Keyword('USE')
USEDIN = Keyword('USEDIN')
VALUE = Keyword('VALUE')
VALUE_IN = Keyword('VALUE_IN')
VALUE_UNIQUE = Keyword('VALUE_UNIQUE')
VAR = Keyword('VAR')
WHERE = Keyword('WHERE')
WHILE = Keyword('WHILE')
WITH = Keyword('WITH')
XOR = Keyword('XOR')

built_in_constant = (CONST_E | PI | SELF | '?').addParseAction(ast.BuiltInConstant.action)
built_in_function = (ABS | ACOS | ASIN | ATAN | BLENGTH | COS | EXISTS | EXP | FORMAT | HIBOUND | HIINDEX | LENGTH
                     | LOBOUND | LOINDEX | LOG2 | LOG10 | LOG | NVL | ODD | ROLESOF | SIN | SIZEOF | SQRT | TAN
                     | TYPEOF | USEDIN | VALUE_IN | VALUE_UNIQUE | VALUE
                     ).addParseAction(ast.BuiltInFunction.action)

built_in_procedure = INSERT | REMOVE.addParseAction(ast.BuiltInProcedure.action)

bit = Char('01')
digit = Char('0123456789')
digits = Word('0123456789')
sign = Char('+-')
encoded_character = Word(hexnums, exact=8)


binary_literal = Word('%', '01').addParseAction(lambda toks: int(toks[0][1:], 2))  # convert to int
# TODO: maybe ignoring leading signs [+-] for numbers will fix some errors
integer_literal = pyparsing_common.signed_integer.copy()  # as int
real_literal = pyparsing_common.sci_real.copy()  # as float
encoded_string_literal = Suppress('"') + \
                         OneOrMore(encoded_character).addParseAction(ast.StringLiteral.decode) + \
                         Suppress('"')

logical_literal = (FALSE | TRUE | UNKNOWN).addParseAction(ast.LogicalLiteral.action)
simple_string_literal = sglQuotedString.copy().addParseAction(ast.StringLiteral.action)
string_literal = simple_string_literal | encoded_string_literal
literal = binary_literal | logical_literal | real_literal | integer_literal | string_literal

schema_version_id = string_literal
simple_id = Word(ascii_letters, ascii_letters + '0123456789_').setParseAction(ast.SimpleID.action)
attribute_id = simple_id
constant_id = simple_id
entity_id = simple_id
enumeration_id = simple_id
function_id = simple_id
parameter_id = simple_id
procedure_id = simple_id
rule_label_id = simple_id
rule_id = simple_id
schema_id = simple_id
subtype_constraint_id = simple_id
type_label_id = simple_id
type_id = simple_id
variable_id = simple_id
rename_id = constant_id | entity_id | function_id | procedure_id | type_id

attribute_ref = attribute_id
constant_ref = constant_id
entity_ref = entity_id
enumeration_ref = enumeration_id
function_ref = function_id
parameter_ref = parameter_id
procedure_ref = procedure_id
rule_label_ref = rule_label_id
rule_ref = rule_id
schema_ref = schema_id
subtype_constraint_ref = subtype_constraint_id
type_label_ref = type_label_id
type_ref = type_id
variable_ref = variable_id
general_ref = parameter_ref | variable_ref
resource_ref = constant_ref | entity_ref | function_ref | procedure_ref | type_ref

named_types = entity_ref | type_ref

# TODO: attribute_qualifier - added OneOrMore() reason: query_expression (SELF\aaa.bbb.ccc.eee)
attribute_qualifier = OneOrMore('.' + attribute_ref)
enumeration_reference = Optional(type_ref + '.') + enumeration_ref
resource_or_rename = resource_ref + Optional(AS + rename_id)
constant_factor = built_in_constant | constant_ref
named_type_or_rename = named_types + Optional(AS + (entity_id | type_id))
population = entity_ref
group_qualifier = '\\' + entity_ref
type_label = type_label_id | type_label_ref
qualified_attribute = SELF + group_qualifier + attribute_qualifier
referenced_attribute = qualified_attribute | attribute_ref
unique_rule = Optional(rule_label_id + ':') + referenced_attribute + ZeroOrMore(',' + referenced_attribute)

null_stmt = Char(';')  # pass ?
skip_stmt = SKIP + ';'  # continue ?
escape_stmt = ESCAPE + ';'  # break ?

add_like_op = (Char('+-') | OR | XOR).setName('add like operand')
interval_op = oneOf('< <=').setName('interval operand')
multiplication_like_op = ('||' | Char('*/|') | DIV | MOD | AND).setName('multiplication like operand')
rel_op = oneOf('< > <= >= <> = :<>: :=:').setName('relation operand')
rel_op_extended = (rel_op | IN | LIKE).setName('extended relation operand')
unary_op = (sign | NOT).setName('unary operand')
exponentiation_op = '**'

simple_factor = Forward()
factor = simple_factor + Optional(exponentiation_op + simple_factor)
term = factor + ZeroOrMore(multiplication_like_op + factor)
simple_expression = term + ZeroOrMore(add_like_op + term)
numeric_expression = simple_expression
precision_spec = numeric_expression

index = numeric_expression
index_1 = index('index_1')
index_2 = index('index_2')
index_qualifier = '[' + index_1 + Optional(':' + index_2) + ']'
width = numeric_expression
width_spec = '(' + width + ')' + Optional(FIXED)
expression = simple_expression + Optional(rel_op_extended + simple_expression)

bound_1 = numeric_expression('bound_1')
bound_2 = numeric_expression('bound_2')
bound_spec = '[' + bound_1 + ':' + bound_2 + ']'

case_label = expression('case label')
aggregate_source = simple_expression
interval_high = simple_expression
interval_item = simple_expression
interval_low = simple_expression
logical_expression = expression
parameter = expression
repetition = numeric_expression
selector = expression
increment = numeric_expression
element = expression + Optional(':' + repetition)
aggregate_initializer = '[' + Optional(element + ZeroOrMore(',' + element)) + ']'
domain_rule = Optional(rule_label_id + ':') + expression
qualifier = attribute_qualifier | group_qualifier | index_qualifier
redeclared_attribute = qualified_attribute + Optional(RENAMED + attribute_id)
increment_control = variable_id + ':=' + bound_1 + TO + bound_2 + Optional(BY + increment)
attribute_decl = attribute_id | redeclared_attribute
interval = '{' + interval_low + interval_op + interval_item + interval_op + interval_high + '}'

abstract_entity_declaration = ABSTRACT
abstract_supertype = ABSTRACT + SUPERTYPE + ';'
boolean_type = BOOLEAN
number_type = NUMBER
logical_type = LOGICAL
integer_type = INTEGER
generic_type = GENERIC + Optional(':' + type_label)
binary_type = BINARY + Optional(width_spec)
string_type = STRING + Optional(width_spec)
real_type = REAL + Optional('(' + precision_spec + ')')
concrete_types = Forward()
instantiable_type = concrete_types | entity_ref
bag_type = BAG + Optional(bound_spec) + OF + instantiable_type
array_type = ARRAY + bound_spec + OF + Optional(OPTIONAL) + Optional(UNIQUE) + instantiable_type
list_type = LIST + Optional(bound_spec) + OF + Optional(UNIQUE) + instantiable_type
set_type = SET + Optional(bound_spec) + OF + instantiable_type
aggregation_types = array_type | bag_type | list_type | set_type
simple_types = binary_type | boolean_type | integer_type | logical_type | number_type | real_type | string_type
concrete_types <<= aggregation_types | simple_types | type_ref
subtype_declaration = SUBTYPE + OF + '(' + entity_ref + ZeroOrMore(',' + entity_ref) + ')'

generalized_types = Forward()
parameter_type = generalized_types | named_types | simple_types
general_array_type = ARRAY + Optional(bound_spec) + OF + Optional(OPTIONAL) + Optional(UNIQUE) + parameter_type
general_bag_type = BAG + Optional(bound_spec) + OF + parameter_type
general_list_type = LIST + Optional(bound_spec) + OF + Optional(UNIQUE) + parameter_type
general_set_type = SET + Optional(bound_spec) + OF + parameter_type
generic_entity_type = GENERIC_ENTITY + Optional(':' + type_label)
general_aggregation_types = general_array_type | general_bag_type | general_list_type | general_set_type
aggregate_type = AGGREGATE + Optional(':' + type_label) + OF + parameter_type
generalized_types <<= aggregate_type | general_aggregation_types | generic_entity_type | generic_type
formal_parameter = parameter_id + ZeroOrMore(',' + parameter_id) + ':' + parameter_type

supertype_expression = Forward()
one_of = ONEOF + '(' + supertype_expression + ZeroOrMore(',' + supertype_expression) + ')'
actual_parameter_list = '(' + parameter + ZeroOrMore(',' + parameter) + ')'
enumeration_items = '(' + enumeration_id + ZeroOrMore(',' + enumeration_id) + ')'
enumeration_extension = BASED_ON + type_ref + Optional(WITH + enumeration_items)
enumeration_type = Optional(EXTENSIBLE) + ENUMERATION + Optional((OF + enumeration_items) | enumeration_extension)
select_list = '(' + named_types + ZeroOrMore(',' + named_types) + ')'
select_extension = BASED_ON + type_ref + Optional(WITH + select_list)
select_type = Optional(EXTENSIBLE + Optional(GENERIC_ENTITY)) + SELECT + Optional(select_list | select_extension)
constructed_types = enumeration_type | select_type
underlying_type = constructed_types | concrete_types

supertype_term = one_of | ('(' + supertype_expression + ')') | entity_ref
supertype_factor = supertype_term + ZeroOrMore(AND + supertype_term)
supertype_expression <<= supertype_factor + ZeroOrMore(ANDOR + supertype_factor)
subtype_constraint = OF + '(' + supertype_expression + ')'

supertype_rule = SUPERTYPE + subtype_constraint
abstract_supertype_declaration = ABSTRACT + SUPERTYPE + Optional(subtype_constraint)
supertype_constraint = abstract_supertype_declaration | abstract_entity_declaration | supertype_rule
subsuper = Optional(supertype_constraint) + Optional(subtype_declaration)
subtype_constraint_head = SUBTYPE_CONSTRAINT + subtype_constraint_id + FOR + entity_ref + ';'
total_over = TOTAL_OVER + '(' + entity_ref + ZeroOrMore(',' + entity_ref) + ')' + ';'
subtype_constraint_body = Optional(abstract_supertype) + Optional(total_over) + Optional(supertype_expression + ';')
subtype_constraint_decl = subtype_constraint_head + subtype_constraint_body + END_SUBTYPE_CONSTRAINT + ';'

stmt = Forward()
declaration = Forward()
return_stmt = RETURN + Optional('(' + expression + ')') + ';'
assignment_stmt = general_ref + ZeroOrMore(qualifier) + ':=' + expression + ';'
alias_stmt = ALIAS + variable_id + FOR + general_ref + ZeroOrMore(qualifier) + ';' + OneOrMore(stmt) + END_ALIAS + ';'
compound_stmt = BEGIN + OneOrMore(stmt) + END + ';'
case_action = case_label + ZeroOrMore(',' + case_label) + ':' + stmt
case_stmt = CASE + selector + OF + ZeroOrMore(case_action) + Optional(OTHERWISE + ':' + stmt) + END_CASE + ';'
local_variable = variable_id + ZeroOrMore(',' + variable_id) + ':' + parameter_type + Optional(':=' + expression) + ';'
local_decl = LOCAL + local_variable + ZeroOrMore(local_variable) + END_LOCAL + ';'
constant_body = constant_id + ':' + instantiable_type + ':=' + expression + ';'
constant_decl = CONSTANT + OneOrMore(constant_body) + END_CONSTANT + ';'
derived_attr = attribute_decl + ':' + parameter_type + ':=' + expression + ';'
derive_clause = DERIVE + OneOrMore(derived_attr)
function_call = (built_in_function | function_ref) + Optional(actual_parameter_list)
explicit_attr = attribute_decl + ZeroOrMore(',' + attribute_decl) + ':' + Optional(OPTIONAL) + parameter_type + ';'
unique_clause = UNIQUE + unique_rule + ';' + ZeroOrMore(unique_rule + ';')
while_control = WHILE + logical_expression
until_control = UNTIL + logical_expression
repeat_control = Optional(increment_control) + Optional(while_control) + Optional(until_control)
repeat_stmt = REPEAT + repeat_control + ';' + OneOrMore(stmt) + END_REPEAT + ';'
if_stmt = IF + logical_expression + THEN + OneOrMore(stmt) + Optional(ELSE + OneOrMore(stmt)) + END_IF + ';'
algorithm_head = ZeroOrMore(declaration) + Optional(constant_decl) + Optional(local_decl)
procedure_call_stmt = (built_in_procedure | procedure_ref) + Optional(actual_parameter_list) + ';'
procedure_head = PROCEDURE + procedure_id + Optional(
    '(' + Optional(VAR) + formal_parameter + ZeroOrMore(';' + Optional(VAR) + formal_parameter) + ')') + ';'
procedure_decl = procedure_head + algorithm_head + ZeroOrMore(stmt) + END_PROCEDURE + ';'

# Different where clauses required, because parser need the stopOn argument!
where_clause = WHERE + OneOrMore(domain_rule + ';', stopOn=END_TYPE)
entity_where_clause = WHERE + OneOrMore(domain_rule + ';', stopOn=END_ENTITY)
rule_where_clause = WHERE + OneOrMore(domain_rule + ';', stopOn=END_RULE)

type_decl = TYPE + type_id + '=' + underlying_type + ';' + Optional(where_clause) + END_TYPE + ';'
qualifiable_factor = function_call | constant_factor | general_ref | population | attribute_ref
primary = (qualifiable_factor + ZeroOrMore(qualifier)) | literal

# TODO: restore original expression (_aggregate_source) ???
# original: query_expression = QUERY + '(' + variable_id + '<*' + aggregate_source + '|' + logical_expression + ')'
# aggregate_source = simple_expression
expr_or_primary = Optional(unary_op) + ('(' + expression + ')' | primary)
aggregate_source_ = qualified_attribute | primary | expr_or_primary
query_expression = QUERY + '(' + variable_id + '<*' + aggregate_source_ + '|' + logical_expression + ')'
function_head = FUNCTION + function_id + Optional(
    '(' + formal_parameter + ZeroOrMore(';' + formal_parameter) + ')') + ':' + parameter_type + ';'
function_decl = function_head + algorithm_head + OneOrMore(stmt) + END_FUNCTION + ';'

inverse_attr = attribute_decl + ':' + Optional((SET | BAG) + Optional(bound_spec) + OF) + entity_ref + FOR + Optional(
    entity_ref + '.') + attribute_ref + ';'
inverse_clause = INVERSE + OneOrMore(inverse_attr)
entity_constructor = entity_ref + '(' + Optional(expression + ZeroOrMore(',' + expression)) + ')'
entity_head = ENTITY + entity_id + subsuper + ';'
entity_body = ZeroOrMore(explicit_attr) + Optional(derive_clause) + Optional(inverse_clause) + Optional(
    unique_clause) + Optional(entity_where_clause)
entity_decl = entity_head + entity_body + END_ENTITY + ';'
rule_head = RULE + rule_id + FOR + '(' + entity_ref + ZeroOrMore(',' + entity_ref) + ')' + ';'
rule_decl = rule_head + algorithm_head + ZeroOrMore(stmt) + rule_where_clause + END_RULE + ';'

reference_clause = REFERENCE + FROM + schema_ref + Optional(
    '(' + resource_or_rename + ZeroOrMore(',' + resource_or_rename) + ')') + ';'
use_clause = USE + FROM + schema_ref + Optional(
    '(' + named_type_or_rename + ZeroOrMore(',' + named_type_or_rename) + ')') + ';'
interface_specification = reference_clause | use_clause
schema_body = ZeroOrMore(interface_specification) + Optional(constant_decl) + ZeroOrMore(declaration | rule_decl)
schema_decl = SCHEMA + schema_id + Optional(schema_version_id) + ';' + schema_body + END_SCHEMA + ';'

# Resolving forward declarations
simple_factor <<= entity_constructor | query_expression | expr_or_primary | aggregate_initializer | enumeration_reference | interval
simple_factor.addParseAction()
declaration <<= entity_decl | function_decl | procedure_decl | subtype_constraint_decl | type_decl
stmt <<= alias_stmt | assignment_stmt | case_stmt | compound_stmt | if_stmt | procedure_call_stmt | repeat_stmt | return_stmt | skip_stmt | escape_stmt | null_stmt

# Start
syntax = OneOrMore(schema_decl)

# White space enabled for detecting tail remarks
spaces = Suppress(ZeroOrMore(White(' \t')))
remark_tag = spaces + simple_id + ZeroOrMore('.' + simple_id)
tail_remark = ('--' + OneOrMore(remark_tag) + spaces + Suppress(LineEnd())).setName("Tail Remark")
tail_remark.leaveWhitespace()

# Replaced by the 'comments' rule
# embedded_remark = Forward()
# embedded_remark <<= ('(*' + OneOrMore(remark_tag) + ZeroOrMore(
#     OneOrMore(not_paren_star) | lparen_then_not_lparen_star | OneOrMore(
#         '*') | not_rparen_star_then_rparen | embedded_remark) + '*)')
#
# remark = embedded_remark | tail_remark

#          Combine(Regex(r"/_\*(?:[^*]|_\*(?!_/))*") + '*/').setName("C style comment")
comments = Combine(Regex(r"\(\*(?:[^*]|\*(?!\)))*") + '*)').setName("Express Comment")

syntax.ignore(comments)
syntax.ignore(tail_remark)


class Tokens:
    """ Helper class for testing. """
    def __init__(self, it: Iterable):
        self._tokens = tuple(it)

    def __eq__(self, other):
        if type(other) == type(self):
            return self._tokens == other.nodes
        # compare with iterable of string tokens, just for testing
        elif isinstance(other, Iterable):
            return tuple(self.string_tokens) == tuple(other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self._tokens)

    def __len__(self):
        return len(self._tokens)

    def __getitem__(self, item):
        return self._tokens[item]

    def __str__(self):
        return ' '.join(self.string_tokens)

    @property
    def string_tokens(self) -> Iterable:
        for t in self._tokens:
            if hasattr(t, 'string_tokens'):
                yield from t.string_tokens
            else:
                yield str(t)
