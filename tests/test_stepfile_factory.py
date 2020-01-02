import pytest

from steputils.stepfile import Factory, step_string_encoder, parameter_string


def test_enum():
    enum = Factory.enum('.ENUM.')
    assert Factory.is_enum(enum) is True
    assert Factory.is_enum('.ENUM.') is False, 'Enumerations have to be typed.'


def test_unset_param():
    assert Factory.unset_parameter('*') == '*'
    assert Factory.unset_parameter('$') == '$'
    pytest.raises(ValueError, Factory.unset_parameter, '#')
    assert Factory.is_unset_parameter(Factory.unset_parameter('*')) is True
    assert Factory.is_unset_parameter(Factory.unset_parameter('$')) is True
    assert Factory.is_unset_parameter('*') is False, 'Unset parameters have to typed.'


def test_parameter_list():
    assert Factory.parameter_list(1, 2, 'hello') == (1, 2, 'hello')
    assert str(Factory.parameter_list(1, 2, 'hello')) == "(1,2,'hello')"
    assert Factory.is_parameter_list(Factory.parameter_list(1, 2, 'hello')) is True
    assert Factory.is_parameter_list((1, 2, 3)) is False, 'Parameter lists has to be typed.'


def test_binary():
    assert Factory.binary(12).value == 12
    assert str(Factory.binary(12)) == '"0C"'
    assert Factory.is_binary(Factory.binary(12)) is True
    b = Factory.binary(12, 3)
    assert b.value == 12
    assert b.unused == 3


def test_keyword():
    assert Factory.keyword('TEST') == 'TEST'
    assert Factory.is_keyword(Factory.keyword('TEST')) is True
    assert Factory.is_keyword('TEST') is False, 'Keywords have to be typed.'
    # user defined keyword
    assert Factory.is_keyword(Factory.keyword('!TEST')) is True
    pytest.raises(ValueError, Factory.keyword, 'TEST.')


def test_typed_parameter():
    assert str(Factory.typed_parameter('TEST', 1)) == 'TEST(1)'
    assert Factory.is_typed_parameter(Factory.typed_parameter('TEST', 1)) is True
    tp = Factory.typed_parameter('TEST', 1)
    assert tp.type_name == 'TEST'
    assert tp.param == 1


def test_reference():
    assert Factory.reference('#100') == '#100'
    assert Factory.is_reference(Factory.reference('#100')) is True
    assert Factory.is_reference('#100') is False, 'References have to be typed.'
    pytest.raises(ValueError, Factory.reference, '100')


def test_entity():
    e = Factory.entity('TEST', (1, 2, 'hello'))
    assert e.name == 'TEST'
    assert Factory.is_parameter_list(e.params) is True
    assert e.params == (1, 2, 'hello')
    assert str(e) == "TEST(1,2,'hello')"


def test_simple_entity_instance():
    instance = Factory.simple_instance('#100', 'TEST', (1, 2, 3))
    assert instance.ref == '#100'
    assert instance.entity.name == 'TEST'
    assert instance.entity.params == (1, 2, 3)
    assert Factory.is_simple_entity_instance(instance) is True
    assert str(instance) == "#100=TEST(1,2,3);\n"


def test_complex_entity_instance():
    instance = Factory.complex_entity_instance('#100', [
        Factory.entity('TEST', (1, 2, 'hello')),
        Factory.entity('TEST2', (3, 4, 'greetings')),
    ])
    assert instance.ref == '#100'
    assert instance.entities[0].name == 'TEST'
    assert instance.entities[1].name == 'TEST2'
    assert str(instance) == "#100=(TEST(1,2,'hello')TEST2(3,4,'greetings'));\n"


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
    assert parameter_string(Factory.unset_parameter('*')) == "*"
    # Untyped strings will always be quoted!!!
    assert parameter_string('*') == "'*'"
    assert parameter_string(Factory.unset_parameter('$')) == "$"
    assert parameter_string(None) == "$", 'None should be unset parameter'
    assert parameter_string(Factory.keyword('KEY')) == "KEY"
    assert parameter_string(Factory.enum('.ENUM.')) == ".ENUM."
    assert parameter_string(Factory.reference('#100')) == "#100"
    assert parameter_string(Factory.typed_parameter('TYPE', 12)) == "TYPE(12)"
    assert parameter_string(Factory.typed_parameter('TYPE', 'hello')) == "TYPE('hello')"
    assert parameter_string('simple string') == "'simple string'"
    assert parameter_string(123) == "123"
    assert parameter_string(1.23) == "1.23"


def test_parameter_list_to_string():
    assert parameter_string((123, 456) == "(123,456)")
    assert parameter_string([123, 456] == "(123,456)")
    assert parameter_string(Factory.parameter_list([123, 456]) == "(123,456)")
    assert parameter_string((123, (456, (789, '10')))) == "(123,(456,(789,'10')))"
    assert parameter_string((123, None, 456)) == "(123,$,456)", 'None should be unset parameter'


if __name__ == '__main__':
    pytest.main([__file__])
