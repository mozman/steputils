# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

import pytest

from steputils.express.parser import (
    list_type, bound_spec, array_type, index_qualifier, simple_expression, string_literal,
    aggregate_initializer, real_literal, interval, entity_constructor, primary,
    simple_factor, expression, integer_literal, ast, enumeration_type, underlying_type,
    select_type,
)
from steputils.express.ast import AST


def test_bound_spec():
    r = AST(bound_spec.parseString('[3:3]'))
    assert str(r) == '[ 3 : 3 ]'


def test_list():
    r = AST(list_type.parseString('LIST [3:3] OF IfcPositiveInteger'))
    assert str(r) == 'LIST [ 3 : 3 ] OF IfcPositiveInteger'


def test_string_literal():
    r = AST(string_literal.parseString("'test'"))
    assert r[0] == 'test'
    assert type(r[0]) is ast.StringLiteral


def test_simple_expression():
    r = AST(simple_expression.parseString('SELF'))
    assert str(r) == 'SELF'

    r = AST(simple_expression.parseString('1'))
    assert r[0] == 1


def test_simple_expression_as_function_call():
    r = AST(simple_expression.parseString("ABS(100)"))
    assert str(r) == "ABS ( 100 )"
    r = AST(simple_expression.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_expression_as_function_call():
    r = AST(expression.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_simple_factor_as_function_call():
    r = AST(simple_factor.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_primary_as_function_call():
    r = AST(primary.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_primary():
    r = AST(primary.parseString('SELF[1]'))
    assert str(r) == 'SELF [ 1 ]'


def test_aggregate_init():
    assert AST(aggregate_initializer.parseString("[]")) == ['[', ']']
    r = AST(aggregate_initializer.parseString("['test', 100]"))
    assert r[0] == '['
    assert r[1] == 'test'
    assert type(r[1]) is ast.StringLiteral
    assert r[2] == ','
    assert r[3] == 100
    assert type(r[3]) is int
    assert r[4] == ']'


def test_enumeration():
    e = AST(enumeration_type.parseString("ENUMERATION OF (EMAIL, FAX ,PHONE ,POST,VERBAL,USERDEFINED,NOTDEFINED);"))
    assert str(e) == "ENUMERATION OF ( EMAIL , FAX , PHONE , POST , VERBAL , USERDEFINED , NOTDEFINED )"


def test_underlying_type_enum():
    e = AST(underlying_type.parseString("ENUMERATION OF (EMAIL, FAX ,PHONE ,POST,VERBAL,USERDEFINED,NOTDEFINED);"))
    assert str(e) == "ENUMERATION OF ( EMAIL , FAX , PHONE , POST , VERBAL , USERDEFINED , NOTDEFINED )"


def test_select():
    t = AST(select_type.parseString("SELECT (IfcDerivedMeasureValue, IfcMeasureValue, IfcSimpleValue)"))
    assert str(t) == "SELECT ( IfcDerivedMeasureValue , IfcMeasureValue , IfcSimpleValue )"


def test_array():
    r = AST(array_type.parseString('ARRAY [1:2] OF REAL'))
    assert str(r) == 'ARRAY [ 1 : 2 ] OF REAL'


def test_integer_literal():
    assert AST(integer_literal.parseString('1'))[0] == 1
    assert AST(integer_literal.parseString('-2'))[0] == -2
    assert AST(integer_literal.parseString('+10000'))[0] == 10000


def test_type_real():
    assert AST(real_literal.parseString('1.0'))[0] == 1.0
    assert AST(real_literal.parseString('0.'))[0] == 0.
    assert AST(real_literal.parseString('-1.0'))[0] == -1.0
    assert AST(real_literal.parseString('-1.0e-5'))[0] == -1e-5


def test_index_qualifier():
    r = AST(index_qualifier.parseString('[1]'))
    assert r == ['[', '1', ']']
    r = AST(index_qualifier.parseString('[ 1 : 2+ 3]'))
    assert str(r) == '[ 1 : 2 + 3 ]'


def test_interval():
    r = AST(interval.parseString('{1 < x < 2}'))
    assert str(r) == '{ 1 < x < 2 }'
    r = AST(interval.parseString('{(1+1) < x < (2+2)}'))
    assert str(r) == '{ ( 1 + 1 ) < x < ( 2 + 2 ) }'


def test_entity_constructor():
    r = AST(entity_constructor.parseString("ABS(100)"))
    assert str(r) == "ABS ( 100 )"
    r = AST(entity_constructor.parseString("ABS(SELF)"))
    assert str(r) == "ABS ( SELF )"


def test_simple_factor():
    r = AST(simple_factor.parseString("ABS(100)"))
    assert str(r) == "ABS ( 100 )"
    r = AST(simple_factor.parseString("ABS(SELF)"))
    assert str(r) == "ABS ( SELF )"
    r = AST(simple_factor.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


if __name__ == '__main__':
    pytest.main([__file__])
