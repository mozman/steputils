# Created: 07.01.2020
# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import re
from .exceptions import StringDecodingError

EOF = '\0'
HEX_16BIT = "{:04X}"
HEX_32BIT = "{:08X}"
EXT_START_16 = '\\X2\\'
EXT_START_32 = '\\X4\\'
EXT_END = "\\X0\\"
EXT_ENCODING = {
    16: HEX_16BIT,
    32: HEX_32BIT,
}


def step_encoder(s: str) -> str:
    buffer = []
    encoding = 0  # 0 for no encoding, 16 for 16bit encoding, 32 for 32bit encoding
    for char in s:
        value = ord(char)
        if value < 127:  # just ASCII code
            if encoding:  # stop extended encoding
                buffer.append(EXT_END)
                encoding = 0
            if char == '\\':  # escaping backslash
                char = '\\\\'
            elif char == "'":  # escaping apostrophe
                char = "''"
            buffer.append(char)
        else:  # value > 126
            if not encoding:  # start new extended character sequence
                if value < 65536:  # 16bit character
                    encoding = 16
                    buffer.append(EXT_START_16)
                else:  # 32bit character
                    encoding = 32
                    buffer.append(EXT_START_32)
            elif value >= 65536 and encoding == 16:
                # already extended 16bit encoding, but 32bit encoding is required
                # stop 16bit encoding
                buffer.append(EXT_END)
                # and start 32bit encoding
                encoding = 32
                buffer.append(EXT_START_32)
            buffer.append(EXT_ENCODING[encoding].format(value))
    if encoding:
        buffer.append(EXT_END)
    return ''.join(buffer)


# control_directive = page | alphabet | extended2 | extended4 | arbitrary .
# page = '\S\'  character  - not supported
# alphabet = '\P' upper '\'  - not supported
# arbitrary = '\X\' hex_one - not supported
# extended2 ='\X2\' HEX_16BIT { HEX_16BIT } EXT_END
# extended2 ='\X4\' HEX_32BIT { HEX_32BIT } EXT_END

EXT_MATCH = re.compile(r'\\(X[24])\\([0-9A-F]+)\\X0\\')


def _decode_bytes(ext_type: str, hexstr: str) -> str:
    hex_char_count = 4 if ext_type == 'X2' else 8
    length = len(hexstr)
    if length % hex_char_count:
        raise StringDecodingError
    chars = []
    start = 0

    while start < length:
        char = chr(int(hexstr[start:start + hex_char_count], 16))
        chars.append(char)
        start += hex_char_count
    return ''.join(chars)


def step_decoder(s: str) -> str:
    origin = s
    while True:
        r = EXT_MATCH.search(s)
        if r is None:
            break
        try:
            decoded_chars = _decode_bytes(r[1], r[2])
        except StringDecodingError:
            raise StringDecodingError(f'Invalid extended encoding in string "{origin}".')
        s = s.replace(r[0], decoded_chars)
    return s.replace('\\\\', '\\')


class StringBuffer:
    def __init__(self, buffer: str):
        self._buffer = buffer
        self._cursor = 0
        self.line_number = 1

    def look(self, n: int = 0) -> str:
        try:
            return self._buffer[self._cursor + n]
        except IndexError:
            self._cursor = len(self._buffer)
            return EOF

    def get(self) -> str:
        value = self.look()
        if value == '\n':
            self.line_number += 1
        self._cursor += 1
        return value

    def skip(self, n: int = 1) -> None:
        self._cursor += n
