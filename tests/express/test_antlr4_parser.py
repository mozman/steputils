# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import pytest
from steputils.express import Parser


def test_schema():
    parser = Parser("""
    SCHEMA test;
    END_SCHEMA;
    """)
    tree = parser.schema()
    assert tree is not None


def test_type_decl():
    parser = Parser("""
    SCHEMA test;
    
    TYPE test = REAL;
    END_TYPE;

    END_SCHEMA;
    """)
    tree = parser.schema()
    assert tree is not None


if __name__ == '__main__':
    pytest.main([__file__])
