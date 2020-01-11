# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import pytest
import os
from steputils.express.parser import syntax

IFC4X2 = r"\Source\steputils\docs\schema\IFC4x2.exp"


@pytest.fixture(scope='module')
def content():
    return open(IFC4X2).read()


@pytest.mark.skip
@pytest.mark.skipif(not os.path.exists(IFC4X2),
                    reason=f"Required data file '{IFC4X2}' not found. (Not included in PyPI distributions)")
def test_ifc4x2_schema(content):
    syntax.parseString(content)


if __name__ == '__main__':
    pytest.main([__file__])
