import pytest

from steputils import p21
from steputils.p21 import parameter_string


def test_enum():
    enum = p21.enum('.ENUM.')
    assert p21.is_enum(enum) is True
    assert p21.is_enum('.ENUM.') is False, 'Enumerations have to be typed.'


def test_unset_param():
    assert p21.unset_parameter('*') == '*'
    assert p21.unset_parameter('$') == '$'
    pytest.raises(ValueError, p21.unset_parameter, '#')
    assert p21.is_unset_parameter(p21.unset_parameter('*')) is True
    assert p21.is_unset_parameter(p21.unset_parameter('$')) is True
    assert p21.is_unset_parameter('*') is False, 'Unset parameters have to typed.'


def test_parameter_list():
    assert p21.parameter_list(1, 2, 'hello') == (1, 2, 'hello')
    assert str(p21.parameter_list(1, 2, 'hello')) == "(1,2,'hello')"
    assert p21.is_parameter_list(p21.parameter_list(1, 2, 'hello')) is True
    assert p21.is_parameter_list((1, 2, 3)) is False, 'Parameter lists has to be typed.'


def test_binary():
    assert p21.binary(12).value == 12
    assert str(p21.binary(12)) == '"0C"'
    assert p21.is_binary(p21.binary(12)) is True
    b = p21.binary(12, 3)
    assert b.value == 12
    assert b.unused == 3


def test_keyword():
    assert p21.keyword('TEST') == 'TEST'
    assert p21.is_keyword(p21.keyword('TEST')) is True
    assert p21.is_keyword('TEST') is False, 'Keywords have to be typed.'
    # user defined keyword
    assert p21.is_keyword(p21.keyword('!TEST')) is True
    pytest.raises(ValueError, p21.keyword, 'TEST.')


def test_typed_parameter():
    assert str(p21.typed_parameter('TEST', 1)) == 'TEST(1)'
    assert p21.is_typed_parameter(p21.typed_parameter('TEST', 1)) is True
    tp = p21.typed_parameter('TEST', 1)
    assert tp.type_name == 'TEST'
    assert tp.param == 1


def test_reference():
    assert p21.reference('#100') == '#100'
    assert p21.is_reference(p21.reference('#100')) is True
    assert p21.is_reference('#100') is False, 'References have to be typed.'
    pytest.raises(ValueError, p21.reference, '100')


def test_entity():
    e = p21.entity('TEST', (1, 2, 'hello'))
    assert e.name == 'TEST'
    assert p21.is_parameter_list(e.params) is True
    assert e.params == (1, 2, 'hello')
    assert str(e) == "TEST(1,2,'hello')"


def test_simple_entity_instance():
    instance = p21.simple_instance('#100', 'TEST', (1, 2, 3))
    assert instance.ref == '#100'
    assert instance.entity.name == 'TEST'
    assert instance.entity.params == (1, 2, 3)
    assert p21.is_simple_entity_instance(instance) is True
    assert str(instance) == "#100=TEST(1,2,3);\n"


def test_complex_entity_instance():
    instance = p21.complex_entity_instance('#100', [
        p21.entity('TEST', (1, 2, 'hello')),
        p21.entity('TEST2', (3, 4, 'greetings')),
    ])
    assert instance.ref == '#100'
    assert instance.entities[0].name == 'TEST'
    assert instance.entities[1].name == 'TEST2'
    assert str(instance) == "#100=(TEST(1,2,'hello')TEST2(3,4,'greetings'));\n"


def test_parameter_to_string():
    assert parameter_string(p21.unset_parameter('*')) == "*"
    # Untyped strings will always be quoted!!!
    assert parameter_string('*') == "'*'"
    assert parameter_string(p21.unset_parameter('$')) == "$"
    assert parameter_string(None) == "$", 'None should be unset parameter'
    assert parameter_string(p21.keyword('KEY')) == "KEY"
    assert parameter_string(p21.enum('.ENUM.')) == ".ENUM."
    assert parameter_string(p21.reference('#100')) == "#100"
    assert parameter_string(p21.typed_parameter('TYPE', 12)) == "TYPE(12)"
    assert parameter_string(p21.typed_parameter('TYPE', 'hello')) == "TYPE('hello')"
    assert parameter_string('simple string') == "'simple string'"
    assert parameter_string(123) == "123"
    assert parameter_string(1.23) == "1.23"


def test_parameter_list_to_string():
    assert parameter_string((123, 456) == "(123,456)")
    assert parameter_string([123, 456] == "(123,456)")
    assert parameter_string(p21.parameter_list([123, 456]) == "(123,456)")
    assert parameter_string((123, (456, (789, '10')))) == "(123,(456,(789,'10')))"
    assert parameter_string((123, None, 456)) == "(123,$,456)", 'None should be unset parameter'


if __name__ == '__main__':
    pytest.main([__file__])
