# Created: 28.12.2019
# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
import pytest
from io import StringIO

from steputils.stepfile import Factory as sf


@pytest.fixture
def stpfile():
    stp = sf.new()
    timestamp = sf.timestamp()
    stp.header.set_file_description(('notes1', 'notes2'))
    stp.header.set_file_name('test.stp', timestamp)
    stp.header.set_file_schema(('IFC2X3',))
    section = stp.new_data_section()
    section.add(sf.simple_entity_instance('#100', sf.entity('TEST', (1, 2, 3))))
    section.add(sf.simple_entity_instance('#1', sf.entity('TEST', (3, 2, 1))))
    stp.new_data_section(params=('DataSection2',))
    return stp


def test_has_reference(stpfile):
    assert stpfile.has_reference('#100') is True
    assert stpfile.has_reference('#1') is True
    assert stpfile.has_reference('#2') is False


def test_iter_protocol(stpfile):
    result = list(stpfile)
    assert len(result) == 2
    assert sf.is_simple_entity_instance(result[0])


def test_step_file_getter(stpfile):
    assert stpfile['#100'].ref == '#100'
    assert stpfile['#1'].ref == '#1'


def test_len(stpfile):
    assert len(stpfile) == 2


def test_header(stpfile):
    timestamp = stpfile.header['FILE_NAME'].params[1]
    fp = StringIO()
    stpfile.header.write(fp)
    result = fp.getvalue().split('\n')
    assert result[0] == "HEADER;"
    assert result[1] == "FILE_DESCRIPTION(('notes1','notes2'),'2;1');"
    assert result[2] == f"FILE_NAME('test.stp','{timestamp}','',(''),(''),'','');"
    assert result[3] == "FILE_SCHEMA(('IFC2X3'));"
    assert result[4] == "ENDSEC;"


def test_data_section_1(stpfile):
    fp = StringIO()
    stpfile.data[0].write(fp)
    result = fp.getvalue().split('\n')
    assert result[0] == 'DATA;'
    assert result[1] == "#100=TEST(1,2,3);"
    assert result[2] == "#1=TEST(3,2,1);"
    assert result[-2] == 'ENDSEC;'


def test_data_section_2(stpfile):
    fp = StringIO()
    stpfile.data[1].write(fp)
    result = fp.getvalue().split('\n')
    assert result[0] == "DATA('DataSection2');"
    assert result[-2] == 'ENDSEC;'


def test_iso_10303_21_marker(stpfile):
    result = str(stpfile).split('\n')
    assert result[0] == 'ISO-10303-21;'
    # StingIO() last '' marks ends of file
    assert result[-2] == 'END-ISO-10303-21;'


if __name__ == '__main__':
    pytest.main([__file__])
