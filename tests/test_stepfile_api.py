# Created: 28.12.2019
# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
import pytest
from datetime import datetime
from io import StringIO

from steputils.stepfile import (
    StepFile, ComplexEntityInstance, SimpleEntityInstance, Entity, ParameterList, step_string_encoder,
    Keyword, Enumeration, EntityInstanceName, TypedParameter, UnsetParameter, parameter_to_string,
)


def test_string_encoder():
    assert step_string_encoder('ABC') == 'ABC'
    assert step_string_encoder('"') == '"'
    assert step_string_encoder('\'') == '\'\''
    assert step_string_encoder('\\') == '\\\\'
    assert step_string_encoder('ABCÄ') == 'ABC\\X4\\00C4\\X0\\'
    assert step_string_encoder('ABCÄÖ') == 'ABC\\X4\\00C400D6\\X0\\'
    assert step_string_encoder('CÄÖC') == 'C\\X4\\00C400D6\\X0\\C'
    assert step_string_encoder('CÄ\\ÖC') == 'C\\X4\\00C4\\X0\\\\\\\\X4\\00D6\\X0\\C'
    assert step_string_encoder('CÄ\'ÖC') == 'C\\X4\\00C4\\X0\\\'\'\\X4\\00D6\\X0\\C'


def test_parameter_to_string():
    assert parameter_to_string(UnsetParameter('*')) == "*"
    # Untyped strings will always be quoted!!!
    assert parameter_to_string('*') == "'*'"
    assert parameter_to_string(UnsetParameter('$')) == "$"
    assert parameter_to_string(None) == "$", 'None should be unset parameter'
    assert parameter_to_string(Keyword('KEY')) == "KEY"
    assert parameter_to_string(Enumeration('.ENUM.')) == ".ENUM."
    assert parameter_to_string(EntityInstanceName('#100')) == "#100"
    assert parameter_to_string(TypedParameter('TYPE', 12)) == "TYPE(12)"
    assert parameter_to_string(TypedParameter('TYPE', 'hello')) == "TYPE('hello')"
    assert parameter_to_string('simple string') == "'simple string'"
    assert parameter_to_string(123) == "123"
    assert parameter_to_string(1.23) == "1.23"


def test_parameter_list_to_string():
    assert parameter_to_string((123, 456) == "(123,456)")
    assert parameter_to_string([123, 456] == "(123,456)")
    assert parameter_to_string(ParameterList([123, 456]) == "(123,456)")
    assert parameter_to_string((123, (456, (789, '10')))) == "(123,(456,(789,'10')))"
    assert parameter_to_string((123, None, 456)) == "(123,$,456)", 'None should be unset parameter'


@pytest.fixture
def entity():
    return Entity('TEST', params=(1, 2, 'hello'))


def test_entity_to_string(entity):
    fp = StringIO()
    entity.write(fp)
    result = fp.getvalue()
    assert result == "TEST(1,2,'hello')"


def test_simple_instance_to_string(entity):
    instance = SimpleEntityInstance('#100', entity)
    fp = StringIO()
    instance.write(fp)
    result = fp.getvalue()
    assert result == "#100=TEST(1,2,'hello');\n"


def test_complex_entity_to_string(entity):
    instance = ComplexEntityInstance('#100', [entity, entity])
    fp = StringIO()
    instance.write(fp)
    result = fp.getvalue()
    assert result == "#100=(TEST(1,2,'hello')TEST(1,2,'hello'));\n"


@pytest.fixture
def stpfile():
    stp = StepFile()
    timestamp = datetime.utcnow().isoformat(timespec='seconds')
    stp.header.set_file_description(('notes1', 'notes2'))
    stp.header.set_file_name('test.stp', timestamp)
    stp.header.set_file_schema(('IFC2X3',))
    section = stp.new_data_section()
    section.append(SimpleEntityInstance('#100', Entity('TEST', (1, 2, 3))))
    section.append(SimpleEntityInstance('#1', Entity('TEST', (3, 2, 1))))
    stp.new_data_section(params=('DataSection2',))
    return stp


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
    fp = StringIO()
    stpfile.write(fp)
    result = fp.getvalue().split('\n')
    assert result[0] == 'ISO-10303-21;'
    # StingIO() last '' marks ends of file
    assert result[-2] == 'END-ISO-10303-21;'


if __name__ == '__main__':
    pytest.main([__file__])
