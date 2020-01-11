# Created: 06.01.2020
# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

from string import ascii_letters
from pyparsing import *

ABS = CaselessKeyword('abs')
ABSTRACT = CaselessKeyword('abstract')
ACOS = CaselessKeyword('acos')
AGGREGATE = CaselessKeyword('aggregate')
ALIAS = CaselessKeyword('alias')
AND = CaselessKeyword('and')
ANDOR = CaselessKeyword('andor')
ARRAY = CaselessKeyword('array')
AS = CaselessKeyword('as')
ASIN = CaselessKeyword('asin')
ATAN = CaselessKeyword('atan')
BAG = CaselessKeyword('bag')
BASED_ON = CaselessKeyword('based_on')
BEGIN = CaselessKeyword('begin')
BINARY = CaselessKeyword('binary')
BLENGTH = CaselessKeyword('blength')
BOOLEAN = CaselessKeyword('boolean')
BY = CaselessKeyword('by')
CASE = CaselessKeyword('case')
CONSTANT = CaselessKeyword('constant')
CONST_E = CaselessKeyword('const_e')
COS = CaselessKeyword('cos')
DERIVE = CaselessKeyword('derive')
DIV = CaselessKeyword('div')
ELSE = CaselessKeyword('else')
END = CaselessKeyword('end')
END_ALIAS = CaselessKeyword('end_alias')
END_CASE = CaselessKeyword('end_case')
END_CONSTANT = CaselessKeyword('end_constant')
END_ENTITY = CaselessKeyword('end_entity')
END_FUNCTION = CaselessKeyword('end_function')
END_IF = CaselessKeyword('end_if')
END_LOCAL = CaselessKeyword('end_local')
END_PROCEDURE = CaselessKeyword('end_procedure')
END_REPEAT = CaselessKeyword('end_repeat')
END_RULE = CaselessKeyword('end_rule')
END_SCHEMA = CaselessKeyword('end_schema')
END_SUBTYPE_CONSTRAINT = CaselessKeyword('end_subtype_constraint')
END_TYPE = CaselessKeyword('end_type')
ENTITY = CaselessKeyword('entity')
ENUMERATION = CaselessKeyword('enumeration')
ESCAPE = CaselessKeyword('escape')
EXISTS = CaselessKeyword('exists')
EXTENSIBLE = CaselessKeyword('extensible')
EXP = CaselessKeyword('exp')
FALSE = CaselessKeyword('false')
FIXED = CaselessKeyword('fixed')
FOR = CaselessKeyword('for')
FORMAT = CaselessKeyword('format')
FROM = CaselessKeyword('from')
FUNCTION = CaselessKeyword('function')
GENERIC = CaselessKeyword('generic')
GENERIC_ENTITY = CaselessKeyword('generic_entity')
HIBOUND = CaselessKeyword('hibound')
HIINDEX = CaselessKeyword('hiindex')
IF = CaselessKeyword('if')
IN = CaselessKeyword('in')
INSERT = CaselessKeyword('insert')
INTEGER = CaselessKeyword('integer')
INVERSE = CaselessKeyword('inverse')
LENGTH = CaselessKeyword('length')
LIKE = CaselessKeyword('like')
LIST = CaselessKeyword('list')
LOBOUND = CaselessKeyword('lobound')
LOCAL = CaselessKeyword('local')
LOG = CaselessKeyword('log')
LOG10 = CaselessKeyword('log10')
LOG2 = CaselessKeyword('log2')
LOGICAL = CaselessKeyword('logical')
LOINDEX = CaselessKeyword('loindex')
MOD = CaselessKeyword('mod')
NOT = CaselessKeyword('not')
NUMBER = CaselessKeyword('number')
NVL = CaselessKeyword('nvl')
ODD = CaselessKeyword('odd')
OF = CaselessKeyword('of')
ONEOF = CaselessKeyword('oneof')
OPTIONAL = CaselessKeyword('optional')
OR = CaselessKeyword('or')
OTHERWISE = CaselessKeyword('otherwise')
PI = CaselessKeyword('pi')
PROCEDURE = CaselessKeyword('procedure')
QUERY = CaselessKeyword('query')
REAL = CaselessKeyword('real')
REFERENCE = CaselessKeyword('reference')
REMOVE = CaselessKeyword('remove')
RENAMED = CaselessKeyword('renamed')
REPEAT = CaselessKeyword('repeat')
RETURN = CaselessKeyword('return')
ROLESOF = CaselessKeyword('rolesof')
RULE = CaselessKeyword('rule')
SCHEMA = CaselessKeyword('schema')
SELECT = CaselessKeyword('select')
SELF = CaselessKeyword('self')
SET = CaselessKeyword('set')
SIN = CaselessKeyword('sin')
SIZEOF = CaselessKeyword('sizeof')
SKIP = CaselessKeyword('skip')
SQRT = CaselessKeyword('sqrt')
STRING = CaselessKeyword('string')
SUBTYPE = CaselessKeyword('subtype')
SUBTYPE_CONSTRAINT = CaselessKeyword('subtype_constraint')
SUPERTYPE = CaselessKeyword('supertype')
TAN = CaselessKeyword('tan')
THEN = CaselessKeyword('then')
TO = CaselessKeyword('to')
TOTAL_OVER = CaselessKeyword('total_over')
TRUE = CaselessKeyword('true')
TYPE = CaselessKeyword('type')
TYPEOF = CaselessKeyword('typeof')
UNIQUE = CaselessKeyword('unique')
UNKNOWN = CaselessKeyword('unknown')
UNTIL = CaselessKeyword('until')
USE = CaselessKeyword('use')
USEDIN = CaselessKeyword('usedin')
VALUE = CaselessKeyword('value')
VALUE_IN = CaselessKeyword('value_in')
VALUE_UNIQUE = CaselessKeyword('value_unique')
VAR = CaselessKeyword('var')
WHERE = CaselessKeyword('where')
WHILE = CaselessKeyword('while')
WITH = CaselessKeyword('with')
XOR = CaselessKeyword('xor')

built_in_constant = CONST_E | PI | SELF | '?'
built_in_function = ABS | ACOS | ASIN | ATAN | BLENGTH | COS | EXISTS | EXP | FORMAT | HIBOUND | HIINDEX | LENGTH \
                    | LOBOUND | LOINDEX | LOG2 | LOG10 | LOG | NVL | ODD | ROLESOF | SIN | SIZEOF | SQRT | TAN \
                    | TYPEOF | USEDIN | VALUE_IN | VALUE_UNIQUE | VALUE
built_in_procedure = INSERT | REMOVE

bit = Char('01')
binary_literal = Word('%', '01')

digit = Char('0123456789')
digits = Word('0123456789')
sign = Char('+-')

integer_literal = digits
real_literal = pyparsing_common.real

encoded_character = Word(hexnums, exact=8)
encoded_string_literal = '"' + OneOrMore(encoded_character) + '"'
logical_literal = FALSE | TRUE | UNKNOWN
simple_string_literal = sglQuotedString
string_literal = simple_string_literal | encoded_string_literal
literal = binary_literal | logical_literal | real_literal | string_literal
schema_version_id = string_literal

letter = Char(ascii_letters)
not_paren_star_quote_special = Char('!"#$%&+,-./:;<=>?@[\\]^_‘{|}~')  # special char ‘ ???
not_paren_star_special = not_paren_star_quote_special | "'"
not_paren_star = letter | digit | not_paren_star_special
not_lparen_star = not_paren_star | ')'
not_rparen_star = not_paren_star | '('
not_quote = not_paren_star_quote_special | letter | digit | Char('()*')
special = not_paren_star_quote_special | Char("()*’")
lparen_then_not_lparen_star = OneOrMore('(') + OneOrMore(not_lparen_star)
not_rparen_star_then_rparen = OneOrMore(not_rparen_star) + OneOrMore(')')

simple_id = Word(ascii_letters, ascii_letters + '0123456789_')
attribute_id = simple_id
constant_id = simple_id
entity_id = simple_id
attribute_ref = attribute_id
constant_ref = constant_id
entity_ref = entity_id
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
named_types = entity_ref | type_ref
named_type_or_rename = named_types + Optional(AS + (entity_id | type_id))
attribute_qualifier = '.' + attribute_ref
enumeration_reference = Optional(type_ref + '.') + enumeration_ref
resource_ref = constant_ref | entity_ref | function_ref | procedure_ref | type_ref
resource_or_rename = resource_ref + Optional(AS + rename_id)
constant_factor = built_in_constant | constant_ref

population = entity_ref
group_qualifier = '\\' + entity_ref
type_label = type_label_id | type_label_ref
qualified_attribute = SELF + group_qualifier + attribute_qualifier
referenced_attribute = attribute_ref | qualified_attribute
unique_rule = Optional(rule_label_id + ':') + referenced_attribute + ZeroOrMore(',' + referenced_attribute)

null_stmt = Char(';')
skip_stmt = SKIP + ';'
escape_stmt = ESCAPE + ';'

add_like_op = Char('+-') | OR | XOR
interval_op = Char('<') | '<='
multiplication_like_op = Char('*/|') | DIV | MOD | AND
rel_op = oneOf('< > <= >= <> = :<>: :=:')
rel_op_extended = rel_op | IN | LIKE
unary_op = sign | NOT

simple_factor = Forward()
factor = simple_factor + Optional('**' + simple_factor)
term = factor + ZeroOrMore(multiplication_like_op + factor)
simple_expression = term + ZeroOrMore(add_like_op + term)
numeric_expression = simple_expression
precision_spec = numeric_expression
index = numeric_expression
index_1 = index
index_2 = index
index_qualifier = '[' + index_1 + Optional(':' + index_2) + ']'
width = numeric_expression
width_spec = '(' + width + ')' + Optional(FIXED)
expression = simple_expression + Optional(rel_op_extended + simple_expression)
bound_1 = numeric_expression
bound_2 = numeric_expression
bound_spec = '[' + bound_1 + ':' + bound_2 + ']'
case_label = expression
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
underlying_type = concrete_types | constructed_types

supertype_term = entity_ref | one_of | ('(' + supertype_expression + ')')
supertype_factor = supertype_term + ZeroOrMore(AND + supertype_term)
supertype_expression <<= supertype_factor + ZeroOrMore(ANDOR + supertype_factor)
subtype_constraint = OF + '(' + supertype_expression + ')'

supertype_rule = SUPERTYPE + subtype_constraint
abstract_supertype_declaration = ABSTRACT + SUPERTYPE + Optional(subtype_constraint)
supertype_constraint = abstract_entity_declaration | abstract_supertype_declaration | supertype_rule
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
where_clause = WHERE + domain_rule + ';' + ZeroOrMore(domain_rule + ';')
type_decl = TYPE + type_id + '=' + underlying_type + ';' + Optional(where_clause) + END_TYPE + ';'
qualifiable_factor = attribute_ref | constant_factor | function_call | general_ref | population
primary = literal | (qualifiable_factor + ZeroOrMore(qualifier))
query_expression = QUERY + '(' + variable_id + '<*' + aggregate_source + '|' + logical_expression + ')'
function_head = FUNCTION + function_id + Optional(
    '(' + formal_parameter + ZeroOrMore(';' + formal_parameter) + ')') + ':' + parameter_type + ';'
function_decl = function_head + algorithm_head + OneOrMore(stmt) + END_FUNCTION + ';'

inverse_attr = attribute_decl + ':' + Optional((SET | BAG) + Optional(bound_spec) + OF) + entity_ref + FOR + Optional(
    entity_ref + '.') + attribute_ref + ';'
inverse_clause = INVERSE + OneOrMore(inverse_attr)
entity_constructor = entity_ref + '(' + Optional(expression + ZeroOrMore(',' + expression)) + ')'
entity_head = ENTITY + entity_id + subsuper + ';'
entity_body = ZeroOrMore(explicit_attr) + Optional(derive_clause) + Optional(inverse_clause) + Optional(
    unique_clause) + Optional(where_clause)
entity_decl = entity_head + entity_body + END_ENTITY + ';'
rule_head = RULE + rule_id + FOR + '(' + entity_ref + ZeroOrMore(',' + entity_ref) + ')' + ';'
rule_decl = rule_head + algorithm_head + ZeroOrMore(stmt) + where_clause + END_RULE + ';'

reference_clause = REFERENCE + FROM + schema_ref + Optional(
    '(' + resource_or_rename + ZeroOrMore(',' + resource_or_rename) + ')') + ';'
use_clause = USE + FROM + schema_ref + Optional(
    '(' + named_type_or_rename + ZeroOrMore(',' + named_type_or_rename) + ')') + ';'
interface_specification = reference_clause | use_clause
schema_body = ZeroOrMore(interface_specification) + Optional(constant_decl) + ZeroOrMore(declaration | rule_decl)
schema_decl = SCHEMA + schema_id + Optional(schema_version_id) + ';' + schema_body + END_SCHEMA + ';'

# Resolving forward declarations
simple_factor <<= aggregate_initializer | entity_constructor | enumeration_reference | interval | query_expression | (
        Optional(unary_op) + ('(' + expression + ')' | primary))
declaration <<= entity_decl | function_decl | procedure_decl | subtype_constraint_decl | type_decl
stmt <<= alias_stmt | assignment_stmt | case_stmt | compound_stmt | escape_stmt | if_stmt | null_stmt | procedure_call_stmt | repeat_stmt | return_stmt | skip_stmt

# Start
syntax = OneOrMore(schema_decl)


remark_tag = '"' + simple_id + ZeroOrMore('.' + simple_id) + '"'
tail_remark = Combine('--' + OneOrMore(remark_tag) + LineEnd()).setName("Tail Remark")

# Replaced by the 'comments' rule
# embedded_remark = Forward()
# embedded_remark <<= ('(*' + OneOrMore(remark_tag) + ZeroOrMore(
#     OneOrMore(not_paren_star) | lparen_then_not_lparen_star | OneOrMore(
#         '*') | not_rparen_star_then_rparen | embedded_remark) + '*)')
#
# remark = embedded_remark | tail_remark

#          Combine(Regex(r"/_\*(?:[^*]|_\*(?!_/))*") + '*/').setName("C style comment")
comments = Combine(Regex(r"\(\*(?:[^*]|\(*(?!\)))*") + '*)').setName("Express Comment")

syntax.ignore(comments)
syntax.ignore(tail_remark)
