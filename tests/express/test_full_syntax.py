# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import pytest
import os
from pathlib import Path

from steputils.express.parser import syntax

DATAPATH = Path(r"\Source\steputils\docs\schema")
IFC4X2 = DATAPATH / 'IFC4x2.exp'
AP203 = DATAPATH / 'ap203.exp'


@pytest.fixture(scope='module')
def ifc4():
    return open(IFC4X2).read()


@pytest.fixture(scope='module')
def ap203():
    return open(AP203).read()


@pytest.mark.skip
@pytest.mark.skipif(not os.path.exists(IFC4X2),
                    reason=f"Required data file '{IFC4X2}' not found. (Not included in PyPI distributions)")
def test_ifc4x2_schema(ifc4):
    syntax.parseString(ifc4)


@pytest.mark.skip
@pytest.mark.skipif(not os.path.exists(AP203),
                    reason=f"Required data file '{AP203}' not found. (Not included in PyPI distributions)")
def test_ap203_schema(ap203):
    syntax.parseString(ap203)


if __name__ == '__main__':
    pytest.main([__file__])
