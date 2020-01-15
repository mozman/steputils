import pytest

from steputils.express import pyparser, ast
primary = pyparser.primary.copy().addParseAction(ast.Primary.action)
bound_spec = pyparser.bound_spec.copy().addParseAction(ast.BoundSpec.action)


def test_bound_spec():
    r = bound_spec.parseString('[3:3]')[0]
    assert len(r) == 2
    bound_1 = r[0]
    bound_2 = r[1]
    assert bound_1 == 3
    assert bound_2 == 3
    assert repr(r) == '(BoundSpec, 3, 3)'


def test_primary():
    r = primary.parseString('SELF[1]')[0]
    assert repr(r) == "(Primary, 'SELF', '[', 1, ']')"

    r = primary.parseString('1')[0]
    assert type(r) is int

    r = primary.parseString('1.0')[0]
    assert type(r) is float

    r = primary.parseString("'s'")[0]
    assert type(r) is ast.StringLiteral


if __name__ == '__main__':
    pytest.main([__file__])

