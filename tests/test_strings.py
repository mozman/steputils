import pytest

from steputils.strings import step_encoder, step_decoder, StringDecodingError, StringBuffer, EOF


def test_buffer():
    b = StringBuffer('test')
    assert b.look() == 't'
    assert b.look(1) == 'e'
    assert b.get() == 't'
    assert b.look() == 'e'
    assert b.get() == 'e'
    assert b.get() == 's'
    assert b.get() == 't'
    assert b.get() == EOF
    assert b.get() == EOF
    assert b.get() == EOF
    assert b.look() == EOF
    assert b.look(3) == EOF


def test_string_encoder():
    assert step_encoder('ABC') == 'ABC'
    assert step_encoder('"') == '"'
    assert step_encoder("'") == "''"
    assert step_encoder('\'') == '\'\''
    assert step_encoder('\\') == '\\\\'
    assert step_encoder('ABCÄ') == 'ABC\\X2\\00C4\\X0\\'
    assert step_encoder('ABCÄÖ') == 'ABC\\X2\\00C400D6\\X0\\'
    assert step_encoder('CÄÖC') == 'C\\X2\\00C400D6\\X0\\C'
    assert step_encoder('CÄ\\ÖC') == 'C\\X2\\00C4\\X0\\\\\\\\X2\\00D6\\X0\\C'
    assert step_encoder('CÄ\'ÖC') == 'C\\X2\\00C4\\X0\\\'\'\\X2\\00D6\\X0\\C'


def test_string_decoder():
    assert step_decoder('ABC') == 'ABC'
    assert step_decoder("\"") == "\""
    assert step_decoder("'") == "'"
    assert step_decoder("''") == "''", "Apostrophe decoding has to be done by the lexer."
    assert step_decoder("x''x") == "x''x"
    assert step_decoder("x\"x") == "x\"x"
    assert step_decoder("\\\\") == "\\"
    assert step_decoder("x\\\\x") == "x\\x"
    assert step_decoder('ABC\\X2\\00C4\\X0\\') == 'ABCÄ'
    assert step_decoder('ABC\\X2\\00C400D6\\X0\\') == 'ABCÄÖ'
    assert step_decoder('C\\X2\\00C400D6\\X0\\C') == 'CÄÖC'
    assert step_decoder('C\\X2\\00C4\\X0\\\\\\\\X2\\00D6\\X0\\C') == 'CÄ\\ÖC'
    # does not decode escaped apostrophes '
    assert step_decoder('C\\X2\\00C4\\X0\\\'\'\\X2\\00D6\\X0\\C') == 'CÄ\'\'ÖC'


def test_extended_string_decoderx2():
    assert step_decoder("\\X2\\00E4\\X0\\") == '\u00E4'


def test_extended_string_decoder_multi_x2():
    assert step_decoder("\\X2\\00E400E4\\X0\\") == '\u00E4\u00E4'


def test_extended_string_decoder_x4():
    assert step_decoder("\\X4\\000000E4\\X0\\") == '\u00E4'


def test_extended_string_decoder_error():
    # invalid count of hex chars
    pytest.raises(StringDecodingError, step_decoder, "\\X2\\0E4\\X0\\")
    pytest.raises(StringDecodingError, step_decoder, "\\X4\\00000E4\\X0\\")


if __name__ == '__main__':
    pytest.main([__file__])
