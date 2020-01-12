# Created: 12.01.2020
# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
from typing import Iterable, Optional


class AST:
    pass


class Value(AST):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class StringLiteral(Value):
    pass


class LogicalLiteral(Value):
    pass


class BuiltInConstant(Value):
    pass


class BuiltInFunction(Value):
    pass


class BuiltInProcedure(Value):
    pass


class Type(Value):
    pass


class Expression(AST):
    def __init__(self, op, left, right):
        self.operand = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left} {self.operand} {self.right}"


class DomainRule(AST):
    def __init__(self, name: Optional[str], rule: Expression):
        self.name = name
        self.rule = rule

    def __str__(self):
        if self.name is not None:
            return f"{self.name}: {self.rule}"
        else:
            return str(self.rule)


class WhereClause(AST):
    def __init__(self, rules: Iterable[DomainRule]):
        self.rules = list(rules)

    def __len__(self):
        return len(self.rules)

    def __str__(self):
        rules = ';'.join(str(r) for r in self.rules)
        return f"WHERE({rules})"


class TypeDecl(AST):
    def __init__(self, type_id: str, underlying_type: Type, where_clause: WhereClause):
        self.type_id = type_id
        self.under_lying_type = underlying_type
        self.where_clause = where_clause

    def __str__(self):
        return f"TYPE {self.type_id} = {self.under_lying_type} {self.where_clause}"
