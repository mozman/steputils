# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import antlr4
from .expressLexer import expressLexer
from .expressParser import expressParser


def tokens(text):
    stream = antlr4.InputStream(text)
    lexer = expressLexer(stream)
    return antlr4.CommonTokenStream(lexer)


class Parser:
    def __init__(self, text):
        self.parser = expressParser(tokens(text))

    def schema(self):
        return self.parser.syntax().children[0]  # just return first schema
