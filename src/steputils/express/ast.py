# Created: 12.01.2020
# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
from typing import Iterable, Optional


class Literal(str):
    @classmethod
    def action(cls, toks):
        return cls(toks[0])


class StringLiteral(Literal):
    @classmethod
    def action(cls, toks):
        return cls(toks[0][1:-1])  # remove quotes

    @classmethod
    def decode(cls, toks):
        return cls(''.join(chr(int(c, 16)) for c in toks))


class LogicalLiteral(Literal):
    pass


class BuiltInConstant(Literal):
    pass


class BuiltInFunction(Literal):
    pass


class BuiltInProcedure(Literal):
    pass


class Type(Literal):
    pass


class SimpleID(Literal):
    pass


class Operand(Literal):
    pass


def is_literal(item):
    return isinstance(item, (StringLiteral, LogicalLiteral, int, float))


class AST:
    def __init__(self, name: str, children: Iterable):
        self.name = name
        self._children = tuple(children)

    @property
    def children(self):
        return self._children

    @property
    def value(self):
        return self.children[0]

    def __repr__(self):
        content = ', '.join(repr(c) for c in self.children)
        return f'({self.name}, {content})'

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, item):
        return self.children[item]

    @staticmethod
    def action(toks):
        return AST(toks[0], toks[1:])


class Primary(AST):
    @staticmethod
    def action(toks):
        if is_literal(toks[0]):
            return toks[0]
        else:
            return Primary('Primary', toks)


class BoundSpec(AST):
    @staticmethod
    def action(toks):
        return BoundSpec('BoundSpec', (toks[1], toks[3]))


class IndexQualifier(AST):
    @staticmethod
    def action(toks):
        index_1 = toks[1]
        try:
            index_2 = toks[4]
        except IndexError:
            index_2 = None
        return IndexQualifier('IndexQualifier', (index_1, index_2))
