# Created: 28.12.2019
# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
import pytest

from steputils.stepfile import StepFile, HeaderSection, DataSection, Entity, ParameterList


def stpfile():
    s = StepFile()
    s.header.add(Entity('FILE_NAME', ParameterList((1, 2, 3))))
    return s


def test_anything():
    assert True == True


if __name__ == '__main__':
    pytest.main([__file__])
