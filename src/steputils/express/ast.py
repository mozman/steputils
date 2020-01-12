# Created: 12.01.2020
# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
from collections.abc import Iterable


class StringLiteral(str):
    pass


class LogicalLiteral(str):
    pass


class BuiltInConstant(str):
    pass


class BuiltInFunction(str):
    pass


class BuiltInProcedure(str):
    pass


class AST:
    def __init__(self, it: Iterable):
        self.nodes = tuple(it)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.nodes == other.nodes
        # compare with iterable of string tokens, just for testing
        elif isinstance(other, Iterable):
            return tuple(self.string_tokens) == tuple(other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, item):
        return self.nodes[item]

    def __str__(self):
        return ' '.join(self.string_tokens)

    def __repr__(self):
        content = ', '.join(repr(t) for t in self.nodes)
        return f"{self.__class__.__name__}(({content}))"

    @property
    def string_tokens(self) -> Iterable:
        for t in self.nodes:
            if hasattr(t, 'string_tokens'):
                yield from t.string_tokens
            else:
                yield str(t)


class SimpleFactor(AST):
    pass


class TypeDecl(AST):
    pass


class WhereClause(AST):
    pass
