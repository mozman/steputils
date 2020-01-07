# Created: 07.01.2020
# Copyright (c) 2020 Manfred Moitzi
# License: MIT License


class ParseError(Exception):
    pass


class StringDecodingError(ParseError):
    pass


class StepFileStructureError(Exception):
    pass
