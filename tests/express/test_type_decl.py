# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

import pytest
from steputils.express.parser import (
    type_decl, list_type, bound_spec, array_type, where_clause, index_qualifier, simple_expression
)


def test_bound_spec():
    r = bound_spec.parseString('[3:3]').asList()
    assert r == ['[', 3, ':', 3, ']']


def test_list():
    r = list_type.parseString('LIST [3:3] OF IfcPositiveInteger').asList()
    assert r == [
        'LIST', '[', 3, ':', 3, ']',
        'OF', 'IfcPositiveInteger',
    ]


def test_array():
    r = array_type.parseString('ARRAY [1:2] OF REAL').asList()
    assert r == ['ARRAY', '[', 1, ':', 2, ']', 'OF', 'REAL']


def test_type_real():
    r = type_decl.parseString('TYPE IfcAbsorbedDoseMeasure = REAL;END_TYPE;').asList()
    assert r == [
        'TYPE', 'IfcAbsorbedDoseMeasure', '=', 'REAL', ';',
        'END_TYPE', ';'
    ]


def test_type_list():
    r = type_decl.parseString('TYPE IfcArcIndex = LIST [3:3] OF IfcPositiveInteger;END_TYPE;').asList()
    assert r == [
        'TYPE', 'IfcArcIndex', '=',
        'LIST', '[', 3, ':', 3, ']',
        'OF', 'IfcPositiveInteger', ';',
        'END_TYPE', ';'
    ]


def test_index_qualifier():
    r = index_qualifier.parseString('[1]').asList()
    assert r == ['[', 1, ']']
    r = index_qualifier.parseString('[1:2]').asList()
    assert r == ['[', 1, ':', 2, ']']


def test_simple_expression():
    r = simple_expression.parseString('SELF').asList()
    assert r == ['SELF']

    r = simple_expression.parseString('1').asList()
    assert r == [1]


def test_where_clause_1():
    r = where_clause.parseString("WHERE GreaterThanZero : SELF > 0;").asList()
    assert r == ['WHERE', 'GreaterThanZero', ':', 'SELF', '>', 0, ';']


def test_where_clause_2():
    r = where_clause.parseString(" WHERE WR1 : SELF IN ['left', 'middle'];").asList()
    assert r == ['WHERE', 'WR1', ':', 'SELF', 'IN', '[', 'left', ',', 'middle', ']', ';']


@pytest.mark.skip('Unknown problem.')
def test_where_rule_1():
    r = type_decl.parseString("""
    TYPE IfcCardinalPointReference = INTEGER;
    WHERE
        GreaterThanZero : SELF > 0;
    END_TYPE;""").asList()

    assert r == [
        'TYPE', 'IfcCardinalPointReference', '=', 'INTEGER', ';',
        'WHERE', 'GreaterThanZero', ':', 'SELF', '>', 0, ';',
        'END_TYPE', ';'
    ]


if __name__ == '__main__':
    pytest.main([__file__])
