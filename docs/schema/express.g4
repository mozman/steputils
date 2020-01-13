/*
Created: 2020-01-13
Copyright (c) 2020 Manfred Moitzi
License: MIT License
Based on: iso-10303-11--2004.bnf
Author: mozman <me@mozman.at>

*/

grammar express;

attribute_ref :
    attribute_id ;

constant_ref :
    constant_id ;

entity_ref :
    entity_id ;

enumeration_ref :
    enumeration_id ;

function_ref :
    function_id ;

parameter_ref :
    parameter_id ;

procedure_ref :
    procedure_id ;

rule_label_ref :
    rule_label_id ;

rule_ref :
    rule_id ;

schema_ref :
    schema_id ;

subtype_constraint_ref :
    subtype_constraint_id ;

type_label_ref :
    type_label_id ;

type_ref :
    type_id ;

variable_ref :
    variable_id ;

abstract_entity_declaration :
    ABSTRACT ;

abstract_supertype :
    ABSTRACT SUPERTYPE ';' ;

abstract_supertype_declaration :
    ABSTRACT SUPERTYPE subtype_constraint?  ;

actual_parameter_list :
    '(' parameter ( ',' parameter )* ')' ;

add_like_op
    : '+'
    | '-'
    | OR
    | XOR
    ;

aggregate_initializer :
    '[' (element ( ',' element )* )? ']' ;

aggregate_source :
    simple_expression ;

aggregate_type :
    AGGREGATE ( ':' type_label )? OF parameter_type ;

aggregation_types
    : array_type
    | bag_type
    | list_type
    | set_type
    ;

algorithm_head :
    declaration* constant_decl? local_decl? ;

alias_stmt :
    ALIAS variable_id FOR general_ref qualifier* ';' stmt+ END_ALIAS ';' ;

array_type :
    ARRAY bound_spec OF OPTIONAL? UNIQUE? instantiable_type ;

assignment_stmt :
    general_ref qualifier* ':=' expression ';' ;

attribute_decl
    : attribute_id
    | redeclared_attribute
    ;

attribute_id :
    SIMPLE_ID ;

attribute_qualifier :
    '.' attribute_ref ;

bag_type :
    BAG bound_spec? OF instantiable_type ;

binary_type :
    BINARY width_spec? ;

boolean_type :
    BOOLEAN ;

bound_1 :
    numeric_expression ;

bound_2 :
    numeric_expression ;

bound_spec :
    '[' bound_1 ':' bound_2 ']' ;

built_in_constant
    : CONST_E
    | PI
    | SELF
    | '?'
    ;

built_in_function
    : ABS
    | ACOS
    | ASIN
    | ATAN
    | BLENGTH
    | COS
    | EXISTS
    | EXP
    | FORMAT
    | HIBOUND
    | HIINDEX
    | LENGTH
    | LOBOUND
    | LOINDEX
    | LOG
    | LOG2
    | LOG10
    | NVL
    | ODD
    | ROLESOF
    | SIN
    | SIZEOF
    | SQRT
    | TAN
    | TYPEOF
    | USEDIN
    | VALUE
    | VALUE_IN
    | VALUE_UNIQUE
    ;

built_in_procedure
    : INSERT
    | REMOVE
    ;

case_action :
    case_label ( ',' case_label )* ':' stmt ;

case_label :
    expression ;

case_stmt :
    CASE selector OF  case_action* (OTHERWISE ':' stmt)? END_CASE ';' ;

compound_stmt :
    BEGIN stmt+ END ';' ;

concrete_types
    : aggregation_types
    | simple_types
    | type_ref
    ;

constant_body :
    constant_id ':' instantiable_type ':=' expression ';' ;

constant_decl :
    CONSTANT constant_body+ END_CONSTANT ';' ;

constant_factor
    : built_in_constant
    | constant_ref
    ;

constant_id : SIMPLE_ID ;

constructed_types
    : enumeration_type
    | select_type
    ;

declaration
    : entity_decl
    | function_decl
    | procedure_decl
    | subtype_constraint_decl
    | type_decl
    ;

derived_attr :
    attribute_decl ':' parameter_type ':=' expression ';' ;

derive_clause :
    DERIVE derived_attr+ ;

domain_rule :
    (rule_label_id ':')? expression ;

element :
    expression ( ':' repetition )? ;

entity_body :
    explicit_attr* derive_clause? inverse_clause? unique_clause? where_clause? ;

entity_constructor :
    entity_ref '(' ( expression ( ',' expression )* )? ')' ;

entity_decl :
    entity_head entity_body END_ENTITY ';' ;

entity_head :
    ENTITY entity_id subsuper ';' ;

entity_id :
    SIMPLE_ID ;

enumeration_extension :
    BASED_ON type_ref ( WITH enumeration_items )? ;

enumeration_id :
    SIMPLE_ID ;

enumeration_items :
    '(' enumeration_id ( ',' enumeration_id )* ')' ;

enumeration_reference :
    ( type_ref '.' )? enumeration_ref ;

enumeration_type :
    EXTENSIBLE? ENUMERATION ( ( OF enumeration_items ) | enumeration_extension )? ;

escape_stmt :
    ESCAPE ';' ;

explicit_attr :
    attribute_decl ( ',' attribute_decl )? ':' OPTIONAL? parameter_type ';' ;

expression :
    simple_expression ( rel_op_extended simple_expression )? ;

factor :
    simple_factor ( '**' simple_factor )? ;

formal_parameter :
    parameter_id ( ',' parameter_id )? ':' parameter_type ;

function_call :
    ( built_in_function | function_ref ) actual_parameter_list? ;

function_decl :
    function_head algorithm_head stmt+  END_FUNCTION ';' ;

function_head :
    FUNCTION function_id ( '(' formal_parameter ( ';' formal_parameter )* ')' )? ':' parameter_type ';' ;

function_id :
    SIMPLE_ID ;

generalized_types
    : aggregate_type
    | general_aggregation_types
    | generic_entity_type
    | generic_type
    ;

general_aggregation_types
    : general_array_type
    | general_bag_type
    | general_list_type
    | general_set_type
    ;

general_array_type : ARRAY bound_spec? OF OPTIONAL? UNIQUE? parameter_type ;

general_bag_type : BAG bound_spec? OF parameter_type ;

general_list_type : LIST bound_spec? OF UNIQUE? parameter_type ;

general_ref
    : parameter_ref
    | variable_ref
    ;

general_set_type :
    SET bound_spec? OF parameter_type ;

generic_entity_type :
    GENERIC_ENTITY ( ':' type_label )? ;

generic_type :
    GENERIC ( ':' type_label )? ;

group_qualifier :
    '\\' entity_ref ;

if_stmt :
    IF logical_expression THEN stmt+ ( ELSE stmt+ )? END_IF ';' ;

increment :
    numeric_expression ;

increment_control :
    variable_id ':=' bound_1 TO bound_2 ( BY increment )? ;

index :
    numeric_expression ;

index_1 :
    index ;

index_2 :
    index ;

index_qualifier :
    '[' index_1 ( ':' index_2 )? ']' ;

instantiable_type
    : concrete_types
    | entity_ref
    ;

integer_type :
    INTEGER ;

interface_specification
    : reference_clause
    | use_clause
    ;

interval :
    '{' interval_low interval_op interval_item interval_op interval_high '}' ;

interval_high :
    simple_expression ;

interval_item :
    simple_expression ;

interval_low :
    simple_expression ;

interval_op
    : '<'
    | '<='
    ;

inverse_attr :
    attribute_decl ':' ( ( SET | BAG ) bound_spec? OF )? entity_ref FOR ( entity_ref '.' )? attribute_ref ';' ;

inverse_clause :
    INVERSE inverse_attr+ ;

list_type :
    LIST bound_spec? OF UNIQUE? instantiable_type ;

literal
    : BINARY_LITERAL
    | logical_literal
    | REAL_LITERAL
    | INTEGER_LITERAL
    | string_literal
    ;

local_decl :
    LOCAL local_variable+ END_LOCAL ';' ;

local_variable :
    variable_id ( ',' variable_id )* ':' parameter_type ( '::' expression )? ';' ;

logical_expression :
    expression ;

logical_literal
    : FALSE
    | TRUE
    | UNKNOWN
    ;

logical_type :
    LOGICAL ;

multiplication_like_op
    : '*'
    | '/'
    | DIV
    | MOD
    | AND
    | '||'
    ;

named_types
    : entity_ref
    | type_ref
    ;

named_type_or_rename :
    named_types ( AS ( entity_id | type_id ) )? ;

null_stmt :
    ';' ;

number_type :
    NUMBER ;

numeric_expression :
    simple_expression ;

one_of :
    ONEOF '(' supertype_expression ( ',' supertype_expression )* ')' ;

parameter :
    expression ;

parameter_id :
    SIMPLE_ID ;

parameter_type
    : generalized_types
    | named_types
    | simple_types
    ;

population :
    entity_ref ;

precision_spec :
    numeric_expression ;

primary
    : literal
    | ( qualifiable_factor ( qualifier )* )
    ;

procedure_call_stmt :
    ( built_in_procedure | procedure_ref ) actual_parameter_list+ ';' ;

procedure_decl :
    procedure_head algorithm_head stmt* END_PROCEDURE ';' ;

procedure_head :
    PROCEDURE procedure_id ( '(' VAR? formal_parameter ( ';' VAR? formal_parameter )* ')' )? ';' ;

procedure_id :
    SIMPLE_ID ;

qualifiable_factor
    : attribute_ref
    | constant_factor
    | function_call
    | general_ref
    | population
    ;

qualified_attribute :
    SELF group_qualifier attribute_qualifier ;

qualifier
    : attribute_qualifier
    | group_qualifier
    | index_qualifier
    ;

query_expression :
    QUERY '(' variable_id '<*' aggregate_source '|' logical_expression ')' ;

real_type :
    REAL ( '(' precision_spec ')' )? ;

redeclared_attribute :
    qualified_attribute ( RENAMED attribute_id )? ;

referenced_attribute
    : attribute_ref
    | qualified_attribute
    ;

reference_clause :
    REFERENCE FROM schema_ref ( '(' resource_or_rename ( ',' resource_or_rename )* ')' )? ';' ;

rel_op
    : '<'
    | '>'
    | '<='
    | '>='
    | '<>'
    | '='
    | ':<>:'
    | ':=:'
    ;

rel_op_extended
    : rel_op
    | IN
    | LIKE
    ;

rename_id
    : constant_id
    | entity_id
    | function_id
    | procedure_id
    | type_id
    ;

repeat_control :
    increment_control? while_control? until_control? ;

repeat_stmt :
    REPEAT repeat_control ';' stmt+ END_REPEAT ';' ;

repetition :
    numeric_expression ;

resource_or_rename :
    resource_ref ( AS rename_id )? ;

resource_ref
    : constant_ref
    | entity_ref
    | function_ref
    | procedure_ref
    | type_ref
    ;

return_stmt :
    RETURN ( '(' expression ')' )? ';' ;

rule_decl :
    rule_head algorithm_head stmt* where_clause END_RULE ';' ;

rule_head :
    RULE rule_id FOR '(' entity_ref ( ',' entity_ref )* ')' ';' ;

rule_id :
    SIMPLE_ID ;

rule_label_id :
    SIMPLE_ID ;

schema_body :
    interface_specification* constant_decl? ( declaration | rule_decl )* ;

schema_decl :
    SCHEMA schema_id schema_version_id? ';' schema_body END_SCHEMA ';' ;

schema_id :
    SIMPLE_ID ;

schema_version_id :
    string_literal ;

selector :
    expression ;

select_extension :
    BASED_ON type_ref ( WITH select_list )? ;

select_list :
    '(' named_types ( ',' named_types )* ')' ;

select_type :
    ( EXTENSIBLE GENERIC_ENTITY? )? SELECT ( select_list | select_extension )? ;

set_type :
    SET bound_spec? OF instantiable_type ;

simple_expression :
    term (add_like_op term )* ;

simple_factor : aggregate_initializer
    | entity_constructor
    | enumeration_reference
    | interval
    | query_expression
    | ( unary_op? ( '(' expression ')' | primary ) ) ;

simple_types
    : binary_type
    | boolean_type
    | integer_type
    | logical_type
    | number_type
    | real_type
    | string_type
    ;

skip_stmt :
    SKIP_ ';' ;

stmt : alias_stmt
    | assignment_stmt
    | case_stmt
    | compound_stmt
    | escape_stmt
    | if_stmt
    | null_stmt
    | procedure_call_stmt
    | repeat_stmt
    | return_stmt
    | skip_stmt ;

string_literal
    : SIMPLE_STRING_LITERAL
    | ENCODED_STRING_LITERAL
    ;

string_type :
    STRING width_spec? ;

subsuper :
    supertype_constraint? subtype_declaration? ;

subtype_constraint :
    OF '(' supertype_expression ')' ;

subtype_constraint_body :
    abstract_supertype? total_over? ( supertype_expression ';' )? ;

subtype_constraint_decl :
    subtype_constraint_head subtype_constraint_body END_SUBTYPE_CONSTRAINT ';' ;

subtype_constraint_head :
    SUBTYPE_CONSTRAINT subtype_constraint_id FOR entity_ref ';' ;

subtype_constraint_id :
    SIMPLE_ID ;

subtype_declaration :
    SUBTYPE OF '(' entity_ref ( ',' entity_ref )* ')' ;

supertype_constraint
    : abstract_entity_declaration
    | abstract_supertype_declaration
    | supertype_rule
    ;

supertype_expression :
    supertype_factor ( ANDOR supertype_factor )* ;

supertype_factor :
    supertype_term ( AND supertype_term )* ;

supertype_rule :
    SUPERTYPE subtype_constraint ;

supertype_term
    : entity_ref
    | one_of
    | '(' supertype_expression ')'
    ;

syntax :
    schema_decl+ ;

term :
    factor ( multiplication_like_op factor )* ;

total_over :
    TOTAL_OVER '(' entity_ref ( ',' entity_ref )* ')' ';' ;

type_decl :
    TYPE type_id '=' underlying_type ';' where_clause? END_TYPE ';' ;

type_id :
    SIMPLE_ID ;

type_label
    : type_label_id
    | type_label_ref
    ;

type_label_id :
    SIMPLE_ID ;

unary_op
    : '+'
    | '-'
    | NOT
    ;

underlying_type
    : concrete_types
    | constructed_types
    ;

unique_clause :
    UNIQUE (unique_rule ';')+ ;

unique_rule :
    ( rule_label_id ':' )? referenced_attribute ( ',' referenced_attribute )* ;

until_control :
    UNTIL logical_expression ;

use_clause :
    USE FROM schema_ref ( '(' named_type_or_rename ( ',' named_type_or_rename )* ')' )? ';' ;

variable_id :
    SIMPLE_ID ;

where_clause :
    WHERE (domain_rule ';')+ ;

while_control :
    WHILE logical_expression ;

width :
    numeric_expression ;

width_spec :
    '(' width ')' FIXED? ;

ABS : 'ABS' ;
ABSTRACT : 'ABSTRACT' ;
ACOS : 'ACOS' ;
AGGREGATE : 'AGGREGATE' ;
ALIAS : 'ALIAS' ;
AND : 'AND' ;
ANDOR : 'ANDOR' ;
ARRAY : 'ARRAY' ;
AS : 'AS' ;
ASIN : 'ASIN' ;
ATAN : 'ATAN' ;
BAG : 'BAG' ;
BASED_ON : 'BASED_ON' ;
BEGIN : 'BEGIN' ;
BINARY : 'BINARY' ;
BLENGTH : 'BLENGTH' ;
BOOLEAN : 'BOOLEAN' ;
BY : 'BY' ;
CASE : 'CASE' ;
CONSTANT : 'CONSTANT' ;
CONST_E : 'CONST_E' ;
COS : 'COS' ;
DERIVE : 'DERIVE' ;
DIV : 'DIV' ;
ELSE : 'ELSE' ;
END : 'END' ;
END_ALIAS : 'END_ALIAS' ;
END_CASE : 'END_CASE' ;
END_CONSTANT : 'END_CONSTANT' ;
END_ENTITY : 'END_ENTITY' ;
END_FUNCTION : 'END_FUNCTION' ;
END_IF : 'END_IF' ;
END_LOCAL : 'END_LOCAL' ;
END_PROCEDURE : 'END_PROCEDURE' ;
END_REPEAT : 'END_REPEAT' ;
END_RULE : 'END_RULE' ;
END_SCHEMA : 'END_SCHEMA' ;
END_SUBTYPE_CONSTRAINT : 'END_SUBTYPE_CONSTRAINT' ;
END_TYPE : 'END_TYPE' ;
ENTITY : 'ENTITY' ;
ENUMERATION : 'ENUMERATION' ;
ESCAPE : 'ESCAPE' ;
EXISTS : 'EXISTS' ;
EXTENSIBLE : 'EXTENSIBLE' ;
EXP : 'EXP' ;
FALSE : 'FALSE' ;
FIXED : 'FIXED' ;
FOR : 'FOR' ;
FORMAT : 'FORMAT' ;
FROM : 'FROM' ;
FUNCTION : 'FUNCTION' ;
GENERIC : 'GENERIC' ;
GENERIC_ENTITY : 'GENERIC_ENTITY' ;
HIBOUND : 'HIBOUND' ;
HIINDEX : 'HIINDEX' ;
IF : 'IF' ;
IN : 'IN' ;
INSERT : 'INSERT' ;
INTEGER : 'INTEGER' ;
INVERSE : 'INVERSE' ;
LENGTH : 'LENGTH' ;
LIKE : 'LIKE' ;
LIST : 'LIST' ;
LOBOUND : 'LOBOUND' ;
LOCAL : 'LOCAL' ;
LOG : 'LOG' ;
LOG10 : 'LOG10' ;
LOG2 : 'LOG2' ;
LOGICAL : 'LOGICAL' ;
LOINDEX : 'LOINDEX' ;
MOD : 'MOD' ;
NOT : 'NOT' ;
NUMBER : 'NUMBER' ;
NVL : 'NVL' ;
ODD : 'ODD' ;
OF : 'OF' ;
ONEOF : 'ONEOF' ;
OPTIONAL : 'OPTIONAL' ;
OR : 'OR' ;
OTHERWISE : 'OTHERWISE' ;
PI : 'PI' ;
PROCEDURE : 'PROCEDURE' ;
QUERY : 'QUERY' ;
REAL : 'REAL' ;
REFERENCE : 'REFERENCE' ;
REMOVE : 'REMOVE' ;
RENAMED : 'RENAMED' ;
REPEAT : 'REPEAT' ;
RETURN : 'RETURN' ;
ROLESOF : 'ROLESOF' ;
RULE : 'RULE' ;
SCHEMA : 'SCHEMA' ;
SELECT : 'SELECT' ;
SELF : 'SELF' ;
SET : 'SET' ;
SIN : 'SIN' ;
SIZEOF : 'SIZEOF' ;
SKIP_ : 'SKIP' ;
SQRT : 'SQRT' ;
STRING : 'STRING' ;
SUBTYPE : 'SUBTYPE' ;
SUBTYPE_CONSTRAINT : 'SUBTYPE_CONSTRAINT' ;
SUPERTYPE : 'SUPERTYPE' ;
TAN : 'TAN' ;
THEN : 'THEN' ;
TO : 'TO' ;
TOTAL_OVER : 'TOTAL_OVER' ;
TRUE : 'TRUE' ;
TYPE : 'TYPE' ;
TYPEOF : 'TYPEOF' ;
UNIQUE : 'UNIQUE' ;
UNKNOWN : 'UNKNOWN' ;
UNTIL : 'UNTIL' ;
USE : 'USE' ;
USEDIN : 'USEDIN' ;
VALUE : 'VALUE' ;
VALUE_IN : 'VALUE_IN' ;
VALUE_UNIQUE : 'VALUE_UNIQUE' ;
VAR : 'VAR' ;
WHERE : 'WHERE' ;
WHILE : 'WHILE' ;
WITH : 'WITH' ;
XOR : 'XOR' ;
BIT : [0-1] ;
DIGIT : [0-9] ;
DIGITS : [0-9]+ ;
LETTER : [a-zA-Z];
BINARY_LITERAL : '%' [01]+ ;
ENCODED_STRING_LITERAL : '"' [0-9a-fA-F]+ '"' ;
INTEGER_LITERAL : '-'? DIGITS ;
REAL_LITERAL : '-'? DIGITS '.' DIGIT* (('e'|'E') ('+'|'-') DIGITS)? ;
SIMPLE_ID : LETTER (LETTER | DIGIT | '_' )* ;
QUOTECHAR : '\'';
SIMPLE_STRING_LITERAL : QUOTECHAR .*? QUOTECHAR ;
SIGN : '+' | '-' ;
COMMENTS : '(*' .*? '*)' -> skip ;
TAIL_REMARK : '--' .*? [\r\n]+ -> skip;
WS : [ \t\r\n]+ -> skip ;
