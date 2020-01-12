# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import pytest
from steputils.express.ast import TypeDecl, WhereClause


def test_ast_node():
    w = WhereClause(('WHERE', 'SELF', '>', 0, ';'))
    assert type(w[3]) is int
    assert len(w) == 5
    assert str(w) == "WHERE SELF > 0 ;"
    assert repr(w) == "WhereClause(('WHERE', 'SELF', '>', 0, ';'))"


def test_ast_tree():
    w = WhereClause(('WHERE', 'SELF', '>', 0, ';'))
    t = TypeDecl(('TYPE', 'XType', '=', 'INTEGER', ';', w, 'END_TYPE', ';'))
    assert len(t) == 8

    assert t == [
        'TYPE', 'XType', '=', 'INTEGER', ';',
        'WHERE', 'SELF', '>', '0', ';', 'END_TYPE', ';'
    ]
    assert str(t) == "TYPE XType = INTEGER ; WHERE SELF > 0 ; END_TYPE ;"
    assert repr(
        t) == "TypeDecl(('TYPE', 'XType', '=', 'INTEGER', ';', WhereClause(('WHERE', 'SELF', '>', 0, ';')), 'END_TYPE', ';'))"


if __name__ == '__main__':
    pytest.main([__file__])
