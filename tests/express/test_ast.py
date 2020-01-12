# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import pytest
from steputils.express.ast import TypeDecl, WhereClause, DomainRule, Expression, Type


def test_ast_node():
    r1 = DomainRule(None, Expression('<', 'SELF', 0))
    r2 = DomainRule('WR2', Expression('=', 'x', 1))
    w = WhereClause(rules=[r1, r2])
    assert len(w) == 2
    assert str(w) == "WHERE(SELF < 0;WR2: x = 1)"


def test_ast_tree():
    r1 = DomainRule(None, Expression('<', 'SELF', 0))
    r2 = DomainRule('WR2', Expression('=', 'x', 1))
    w = WhereClause(rules=[r1, r2])

    t = TypeDecl('XType', Type('INT'), w)
    assert str(t) == "TYPE XType = INT WHERE(SELF < 0;WR2: x = 1)"


if __name__ == '__main__':
    pytest.main([__file__])
