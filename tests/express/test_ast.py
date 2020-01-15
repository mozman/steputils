# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import pytest
from steputils.express import ast


def test_ast_node():
    root = ast.AST('TEST', (1, 2, "a"))
    assert list(root) == [1, 2, 'a']
    assert root.name == 'TEST'
    assert root[0] == 1
    assert root[2] == 'a'
    assert repr(root) == "(TEST, 1, 2, 'a')"


if __name__ == '__main__':
    pytest.main([__file__])
