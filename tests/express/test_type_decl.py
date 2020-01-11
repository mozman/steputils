# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

import pytest
from steputils.express.parser import (
    type_decl, where_clause,
)


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


def test_where_clause_0():
    r = where_clause.parseString("WHERE SELF > 0;").asList()
    assert r == ['WHERE', 'SELF', '>', 0, ';']


def test_where_clause_1():
    r = where_clause.parseString("WHERE GreaterThanZero : SELF > 0;").asList()
    assert r == ['WHERE', 'GreaterThanZero', ':', 'SELF', '>', 0, ';']


def test_where_clause_2():
    r = where_clause.parseString(" WHERE SELF IN ['left', 'middle'];").asList()
    assert r == ['WHERE', 'SELF', 'IN', '[', 'left', ',', 'middle', ']', ';']
    r = where_clause.parseString(" WHERE WR1 : SELF IN ['left', 'middle'];").asList()
    assert r == ['WHERE', 'WR1', ':', 'SELF', 'IN', '[', 'left', ',', 'middle', ']', ';']


def test_where_clause_3():
    r = where_clause.parseString("WHERE SELF > 0; SELF < 2;").asList()
    assert r == ['WHERE', 'SELF', '>', 0, ';', 'SELF', '<', 2, ';']


def test_where_clause_4():
    r = where_clause.parseString("WHERE SELF > 0; SELF < 2; END_TYPE;").asList()
    assert r == ['WHERE', 'SELF', '>', 0, ';', 'SELF', '<', 2, ';']


def test_where_clause_5():
    r = where_clause.parseString("WHERE MinutesInRange : ABS(SELF[2]) < 60;").asList()
    assert r == [
        'WHERE', 'MinutesInRange', ':',
        'ABS', '(', 'SELF', '[', 2, ']', ')',
        '<', 60, ';'
    ]


def test_where_rule_0():
    r = type_decl.parseString("TYPE XType = INTEGER; WHERE SELF > 0; END_TYPE;").asList()
    assert r == [
        'TYPE', 'XType', '=', 'INTEGER', ';',
        'WHERE', 'SELF', '>', 0, ';', 'END_TYPE', ';'
    ]


def test_where_rule_1():
    r = type_decl.parseString("""
    TYPE IfcCardinalPointReference = INTEGER;
    WHERE
        GreaterThanZero : SELF > 0;
    END_TYPE;
    """).asList()

    assert r == [
        'TYPE', 'IfcCardinalPointReference', '=', 'INTEGER', ';',
        'WHERE', 'GreaterThanZero', ':', 'SELF', '>', 0, ';',
        'END_TYPE', ';'
    ]


def test_where_rule_2():
    r = type_decl.parseString("""
    TYPE IfcCompoundPlaneAngleMeasure = LIST [3:4] OF INTEGER;
        WHERE
        MinutesInRange : ABS(SELF[2]) < 60;
        SecondsInRange : ABS(SELF[3]) < 60;
        MicrosecondsInRange : (SIZEOF(SELF) = 3) OR (ABS(SELF[4]) < 1000000);
        ConsistentSign : ((SELF[1] >= 0) AND (SELF[2] >= 0) AND (SELF[3] >= 0) AND ((SIZEOF(SELF) = 3) OR (SELF[4] >= 0)))
        OR
        ((SELF[1] <= 0) AND (SELF[2] <= 0) AND (SELF[3] <= 0) AND ((SIZEOF(SELF) = 3) OR (SELF[4] <= 0)));
    END_TYPE;
    """).asList()
    assert len(r) == 162


if __name__ == '__main__':
    pytest.main([__file__])
