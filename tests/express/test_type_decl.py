# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

import pytest
from steputils.express.pyparser import type_decl, where_clause, Tokens


def test_typedef_real():
    r = Tokens(type_decl.parseString('TYPE IfcAbsorbedDoseMeasure = REAL;END_TYPE;'))
    assert str(r) == 'TYPE IfcAbsorbedDoseMeasure = REAL ; END_TYPE ;'


def test_typedef_list():
    r = Tokens(type_decl.parseString('TYPE IfcArcIndex = LIST [3:3] OF IfcPositiveInteger;END_TYPE;'))
    assert str(r) == 'TYPE IfcArcIndex = LIST [ 3 : 3 ] OF IfcPositiveInteger ; END_TYPE ;'


def test_typedef_enum():
    t = Tokens(type_decl.parseString("""
    TYPE IfcActionRequestTypeEnum = ENUMERATION OF
        (EMAIL,
        FAX,
        PHONE,
        POST,
        VERBAL,
        USERDEFINED,
        NOTDEFINED);
    END_TYPE;
    """))
    assert str(t) == "TYPE IfcActionRequestTypeEnum = ENUMERATION OF " \
                     "( EMAIL , FAX , PHONE , POST , VERBAL , USERDEFINED , NOTDEFINED ) ; " \
                     "END_TYPE ;"


def test_typedef_select():
    t = Tokens(type_decl.parseString("""
    TYPE IfcValue = SELECT (
        IfcDerivedMeasureValue,
        IfcMeasureValue,
        IfcSimpleValue);
    END_TYPE;
    """))
    assert str(t) == "TYPE IfcValue = SELECT ( IfcDerivedMeasureValue , IfcMeasureValue , IfcSimpleValue ) ; END_TYPE ;"


def test_where_clause_0():
    r = Tokens(where_clause.parseString("WHERE SELF > 0;"))
    assert str(r) == "WHERE SELF > 0 ;"


def test_where_clause_1():
    r = Tokens(where_clause.parseString("WHERE GreaterThanZero : SELF > 0;"))
    assert str(r) == "WHERE GreaterThanZero : SELF > 0 ;"


def test_where_clause_2():
    r = Tokens(where_clause.parseString(" WHERE SELF IN ['left', 'middle'];"))
    assert str(r) == "WHERE SELF IN [ left , middle ] ;"
    r = Tokens(where_clause.parseString(" WHERE WR1 : SELF IN ['left', 'middle'];"))
    assert str(r) == "WHERE WR1 : SELF IN [ left , middle ] ;"


def test_where_clause_3():
    r = Tokens(where_clause.parseString("WHERE SELF > 0; SELF < 2;"))
    assert str(r) == "WHERE SELF > 0 ; SELF < 2 ;"


def test_where_clause_4():
    r = Tokens(where_clause.parseString("WHERE SELF > 0; SELF < 2; END_TYPE;"))
    assert str(r) == "WHERE SELF > 0 ; SELF < 2 ;", 'should ignore: END_TYPE;'


def test_where_clause_5():
    r = Tokens(where_clause.parseString("WHERE MinutesInRange : ABS(SELF[2]) < 60;"))
    assert str(r) == "WHERE MinutesInRange : ABS ( SELF [ 2 ] ) < 60 ;"


def test_where_clause_6():
    r = Tokens(where_clause.parseString("WHERE WR1 : (Role <> IfcRoleEnum.USERDEFINED) OR "
                                     " ((Role = IfcRoleEnum.USERDEFINED) AND EXISTS(SELF.UserDefinedRole));"))
    assert str(r) == "WHERE WR1 : ( Role <> IfcRoleEnum . USERDEFINED ) OR ( ( Role = IfcRoleEnum . USERDEFINED ) AND " \
                     "EXISTS ( SELF . UserDefinedRole ) ) ;"


def test_where_clause_7():
    r = Tokens(where_clause.parseString(
        r"WHERE HasAdvancedFaces : SIZEOF(QUERY(Afs <* SELF\IfcManifoldSolidBrep.Outer.CfsFaces | "
        r"(NOT ('IFC4X2.IFCADVANCEDFACE' IN TYPEOF(Afs))))) = 0;"
    ))
    assert str(r) == r"WHERE HasAdvancedFaces : SIZEOF ( QUERY ( Afs <* SELF \ IfcManifoldSolidBrep . Outer . CfsFaces | " \
                     "( NOT ( IFC4X2.IFCADVANCEDFACE IN TYPEOF ( Afs ) ) ) ) ) = 0 ;"


def test_where_rule_0():
    r = Tokens(type_decl.parseString("TYPE XType = INTEGER; WHERE SELF > 0; END_TYPE;"))
    assert str(r) == "TYPE XType = INTEGER ; WHERE SELF > 0 ; END_TYPE ;"


def test_where_rule_1():
    r = Tokens(type_decl.parseString("""
    TYPE IfcCardinalPointReference = INTEGER;
    WHERE
        GreaterThanZero : SELF > 0;
    END_TYPE;
    """))

    assert str(r) == "TYPE IfcCardinalPointReference = INTEGER ; WHERE GreaterThanZero : SELF > 0 ; END_TYPE ;"


def test_where_rule_2():
    r = Tokens(type_decl.parseString("""
    TYPE IfcCompoundPlaneAngleMeasure = LIST [3:4] OF INTEGER;
        WHERE
        MinutesInRange : ABS(SELF[2]) < 60;
        SecondsInRange : ABS(SELF[3]) < 60;
        MicrosecondsInRange : (SIZEOF(SELF) = 3) OR (ABS(SELF[4]) < 1000000);
        ConsistentSign : ((SELF[1] >= 0) AND (SELF[2] >= 0) AND (SELF[3] >= 0) AND ((SIZEOF(SELF) = 3) OR (SELF[4] >= 0)))
        OR
        ((SELF[1] <= 0) AND (SELF[2] <= 0) AND (SELF[3] <= 0) AND ((SIZEOF(SELF) = 3) OR (SELF[4] <= 0)));
    END_TYPE;
    """))
    assert len(r) == 162


if __name__ == '__main__':
    pytest.main([__file__])
