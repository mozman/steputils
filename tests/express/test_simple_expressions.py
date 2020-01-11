# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

import pytest

from steputils.express.parser import (
    list_type, bound_spec, array_type, index_qualifier, simple_expression, string_literal,
    aggregate_initializer, TStringLiteral, real_literal, interval, entity_constructor, primary,
    simple_factor, expression, integer_literal,
)


def parse_and_join(parser, tstr):
    return ''.join(str(t) for t in parser.parseString(tstr))


def test_bound_spec():
    r = bound_spec.parseString('[3:3]').asList()
    assert r == ['[', 3, ':', 3, ']']


def test_list():
    r = list_type.parseString('LIST [3:3] OF IfcPositiveInteger').asList()
    assert r == [
        'LIST', '[', 3, ':', 3, ']',
        'OF', 'IfcPositiveInteger',
    ]


def test_string_literal():
    r = string_literal.parseString("'test'")
    assert r[0] == 'test'


def test_simple_expression():
    r = simple_expression.parseString('SELF').asList()
    assert r == ['SELF']

    r = simple_expression.parseString('1').asList()
    assert r == [1]


def test_simple_expression_as_function_call():
    r = simple_expression.parseString("ABS(100)").asList()
    assert r == ['ABS', '(', 100, ')']
    r = simple_expression.parseString("ABS(SELF[2])").asList()
    assert r == ['ABS', '(', 'SELF', '[', 2, ']', ')']


def test_expression_as_function_call():
    r = expression.parseString("ABS(SELF[2])").asList()
    assert r == ['ABS', '(', 'SELF', '[', 2, ']', ')']


def test_simple_factor_as_function_call():
    r = simple_factor.parseString("ABS(SELF[2])").asList()
    assert r == ['ABS', '(', 'SELF', '[', 2, ']', ')']


def test_primary_as_function_call():
    r = primary.parseString("ABS(SELF[2])").asList()
    assert r == ['ABS', '(', 'SELF', '[', 2, ']', ')']


def test_primary():
    r = primary.parseString('SELF[1]').asList()
    assert r == ['SELF', '[', 1, ']']


def test_aggregate_init():
    assert aggregate_initializer.parseString("[]").asList() == ['[', ']']
    r = aggregate_initializer.parseString("['test', 100]")
    assert r[0] == '['
    assert r[1] == 'test'
    assert type(r[1]) is TStringLiteral
    assert r[2] == ','
    assert r[3] == 100
    assert type(r[3]) is int
    assert r[4] == ']'


def test_array():
    r = array_type.parseString('ARRAY [1:2] OF REAL').asList()
    assert r == ['ARRAY', '[', 1, ':', 2, ']', 'OF', 'REAL']


def test_integer_literal():
    assert integer_literal.parseString('1').asList() == [1]
    assert integer_literal.parseString('-2').asList() == [-2]
    assert integer_literal.parseString('+10000').asList() == [10000]


def test_type_real():
    assert real_literal.parseString('1.0').asList() == [1.0]
    assert real_literal.parseString('0.').asList() == [0.]
    assert real_literal.parseString('-1.0').asList() == [-1.0]
    assert real_literal.parseString('-1.0e-5').asList() == [-1e-5]


def test_index_qualifier():
    r = index_qualifier.parseString('[1]').asList()
    assert r == ['[', 1, ']']
    assert parse_and_join(index_qualifier, '[ 1 : 2+ 3]') == '[1:2+3]'


def test_interval():
    r = interval.parseString('{1 < x < 2}').asList()
    assert r == ['{', 1, '<', 'x', '<', 2, '}']
    assert parse_and_join(interval, '{(1+1) < x < (2+2)}') == '{(1+1)<x<(2+2)}'


def test_entity_constructor():
    r = entity_constructor.parseString("ABS(100)").asList()
    assert r == ['ABS', '(', 100, ')']
    r = entity_constructor.parseString("ABS(SELF)").asList()
    assert r == ['ABS', '(', 'SELF', ')']


def test_simple_factor():
    r = simple_factor.parseString("ABS(100)").asList()
    assert r == ['ABS', '(', 100, ')']
    r = simple_factor.parseString("ABS(SELF)").asList()
    assert r == ['ABS', '(', 'SELF', ')']
    r = simple_factor.parseString("ABS(SELF[2])").asList()
    assert r == ['ABS', '(', 'SELF', '[', 2, ']', ')']


if __name__ == '__main__':
    pytest.main([__file__])
