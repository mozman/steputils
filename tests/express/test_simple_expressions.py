# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

import pytest

from steputils.express.parser import (
    list_type, bound_spec, array_type, index_qualifier, simple_expression, string_literal,
    aggregate_initializer, real_literal, interval, entity_constructor, primary,
    simple_factor, expression, integer_literal, ast, enumeration_type, underlying_type,
    select_type, comments, tail_remark, query_expression, aggregate_source_, qualified_attribute,
    attribute_qualifier,
)
from steputils.express.ast import AST


def test_bound_spec():
    r = AST(bound_spec.parseString('[3:3]'))
    assert str(r) == '[ 3 : 3 ]'


def test_list():
    r = AST(list_type.parseString('LIST [3:3] OF IfcPositiveInteger'))
    assert str(r) == 'LIST [ 3 : 3 ] OF IfcPositiveInteger'


def test_string_literal():
    r = AST(string_literal.parseString("'test'"))
    assert r[0] == 'test'
    assert type(r[0]) is ast.StringLiteral


def test_simple_expression():
    r = AST(simple_expression.parseString('SELF'))
    assert str(r) == 'SELF'

    r = AST(simple_expression.parseString('1'))
    assert r[0] == 1


def test_simple_expression_as_function_call():
    r = AST(simple_expression.parseString("ABS(100)"))
    assert str(r) == "ABS ( 100 )"
    r = AST(simple_expression.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_expression_as_function_call():
    r = AST(expression.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_simple_factor_as_function_call():
    r = AST(simple_factor.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_primary_as_function_call():
    r = AST(primary.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_primary():
    r = AST(primary.parseString('SELF[1]'))
    assert str(r) == 'SELF [ 1 ]'


def test_aggregate_init():
    assert AST(aggregate_initializer.parseString("[]")) == ['[', ']']
    r = AST(aggregate_initializer.parseString("['test', 100]"))
    assert r[0] == '['
    assert r[1] == 'test'
    assert type(r[1]) is ast.StringLiteral
    assert r[2] == ','
    assert r[3] == 100
    assert type(r[3]) is int
    assert r[4] == ']'


def test_enumeration():
    e = AST(enumeration_type.parseString("ENUMERATION OF (EMAIL, FAX ,PHONE ,POST,VERBAL,USERDEFINED,NOTDEFINED);"))
    assert str(e) == "ENUMERATION OF ( EMAIL , FAX , PHONE , POST , VERBAL , USERDEFINED , NOTDEFINED )"


def test_underlying_type_enum():
    e = AST(underlying_type.parseString("ENUMERATION OF (EMAIL, FAX ,PHONE ,POST,VERBAL,USERDEFINED,NOTDEFINED);"))
    assert str(e) == "ENUMERATION OF ( EMAIL , FAX , PHONE , POST , VERBAL , USERDEFINED , NOTDEFINED )"


def test_select():
    t = AST(select_type.parseString("SELECT (IfcDerivedMeasureValue, IfcMeasureValue, IfcSimpleValue)"))
    assert str(t) == "SELECT ( IfcDerivedMeasureValue , IfcMeasureValue , IfcSimpleValue )"


def test_array():
    r = AST(array_type.parseString('ARRAY [1:2] OF REAL'))
    assert str(r) == 'ARRAY [ 1 : 2 ] OF REAL'


def test_integer_literal():
    assert AST(integer_literal.parseString('1'))[0] == 1
    assert AST(integer_literal.parseString('-2'))[0] == -2
    assert AST(integer_literal.parseString('+10000'))[0] == 10000


def test_type_real():
    assert AST(real_literal.parseString('1.0'))[0] == 1.0
    assert AST(real_literal.parseString('0.'))[0] == 0.
    assert AST(real_literal.parseString('-1.0'))[0] == -1.0
    assert AST(real_literal.parseString('-1.0e-5'))[0] == -1e-5


def test_index_qualifier():
    r = AST(index_qualifier.parseString('[1]'))
    assert r == ['[', '1', ']']
    r = AST(index_qualifier.parseString('[ 1 : 2+ 3]'))
    assert str(r) == '[ 1 : 2 + 3 ]'


def test_interval():
    r = AST(interval.parseString('{1 < x < 2}'))
    assert str(r) == '{ 1 < x < 2 }'
    r = AST(interval.parseString('{(1+1) < x < (2+2)}'))
    assert str(r) == '{ ( 1 + 1 ) < x < ( 2 + 2 ) }'


def test_entity_constructor():
    r = AST(entity_constructor.parseString("test()"))
    assert str(r) == "test ( )"
    r = AST(entity_constructor.parseString("ABS(100)"))
    assert str(r) == "ABS ( 100 )"
    r = AST(entity_constructor.parseString("ABS(SELF)"))
    assert str(r) == "ABS ( SELF )"


def test_simple_factor():
    r = AST(simple_factor.parseString("test()"))
    assert str(r) == "test ( )"
    r = AST(simple_factor.parseString("ABS(100)"))
    assert str(r) == "ABS ( 100 )"
    r = AST(simple_factor.parseString("ABS(SELF)"))
    assert str(r) == "ABS ( SELF )"
    r = AST(simple_factor.parseString("ABS(SELF[2])"))
    assert str(r) == "ABS ( SELF [ 2 ] )"


def test_sizeof_expr():
    r = AST(expression.parseString(r"SIZEOF(a)"))
    assert str(r) == "SIZEOF ( a )"


def test_aggregate_source():
    r = AST(aggregate_source_.parseString("AAA"))
    assert str(r) == "AAA"
    r = AST(aggregate_source_.parseString("AAA.bbb"))
    assert str(r) == "AAA . bbb"
    r = AST(aggregate_source_.parseString("AAA.bbb.ccc"))
    assert str(r) == "AAA . bbb . ccc"
    r = AST(aggregate_source_.parseString(r"SELF\AAA.bbb"))
    assert str(r) == r"SELF \ AAA . bbb"
    r = AST(aggregate_source_.parseString(r"SELF\AAA.bbb.ccc"))
    assert str(r) == r"SELF \ AAA . bbb . ccc"


def test_query_expr():
    r = AST(query_expression.parseString("QUERY(a <* b | 1 = 1)"))
    assert str(r) == "QUERY ( a <* b | 1 = 1 )"


def test_attr_qualifier():
    r = AST(attribute_qualifier.parseString(".Outer.CfsFaces"))
    assert str(r) == ". Outer . CfsFaces"


def test_qualified_attr():
    r = AST(qualified_attribute.parseString(r"SELF\IfcManifoldSolidBrep.Outer.CfsFaces"))
    assert str(r) == r"SELF \ IfcManifoldSolidBrep . Outer . CfsFaces"


def test_query_expr_2():
    r = AST(query_expression.parseString(r"QUERY(Afs <* SELF\IfcManifoldSolidBrep.Outer.CfsFaces | "
                                         r"(NOT ('IFC4X2.IFCADVANCEDFACE' IN TYPEOF(Afs))))"))
    assert str(r) == r"QUERY ( Afs <* SELF \ IfcManifoldSolidBrep . Outer . CfsFaces | " \
                     r"( NOT ( IFC4X2.IFCADVANCEDFACE IN TYPEOF ( Afs ) ) ) )"


def test_query_expr_3():
    r = AST(query_expression.parseString("QUERY (Vsh <* Voids | SIZEOF (QUERY (Afs <* Vsh.CfsFaces | "
                                         "(NOT ('IFC4X2.IFCADVANCEDFACE' IN TYPEOF(Afs)))  )) = 0))"))
    assert str(r) == "QUERY ( Vsh <* Voids | SIZEOF ( QUERY ( Afs <* Vsh . CfsFaces | ( NOT ( IFC4X2.IFCADVANCEDFACE IN " \
                     "TYPEOF ( Afs ) ) ) ) ) = 0 )"


def test_complex_expr_1():
    r = AST(expression.parseString(r"SIZEOF(a) = 0"))
    assert str(r) == r"SIZEOF ( a ) = 0"


def test_complex_expr_2():
    r = AST(expression.parseString(r"SIZEOF(QUERY(Afs <* SELF\IfcManifoldSolidBrep.Outer.CfsFaces | "
                                   r"(NOT ('IFC4X2.IFCADVANCEDFACE' IN TYPEOF(Afs))))) = 0"))
    assert str(r) == r"SIZEOF ( QUERY ( Afs <* SELF \ IfcManifoldSolidBrep . Outer . CfsFaces | " \
                     r"( NOT ( IFC4X2.IFCADVANCEDFACE IN TYPEOF ( Afs ) ) ) ) ) = 0"


def test_comments():
    assert str(AST(comments.parseString("(* comment  *)"))) == '(* comment  *)'
    assert str(AST(comments.parseString("(* comment * *)"))) == '(* comment * *)'
    assert str(AST(comments.parseString("(** comment **)"))) == '(** comment **)'
    assert str(AST(comments.parseString("(** (* comment **)"))) == '(** (* comment **)'


def test_tail_remark():
    assert str(AST(tail_remark.parseString("-- approved_item \n"))) == '-- approved_item'
    assert str(AST(tail_remark.parseString("-- approved_item.test \n next line"))) == '-- approved_item . test'


def test_ignore_tail_remark():
    expr_test = simple_expression('TEST')
    expr_test.ignore(tail_remark)
    assert str(AST(expr_test.parseString(" 1 + 1 -- approved_item \n xxx"))) == '1 + 1'
    assert str(AST(expr_test.parseString(" 1 + 1 -- approved_item simple.name \n END_TYPE;"))) == '1 + 1'


if __name__ == '__main__':
    pytest.main([__file__])
