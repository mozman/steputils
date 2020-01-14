# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import pytest
from steputils.express.pyparser import entity_decl, supertype_constraint, one_of, supertype_rule, Tokens


def test_simple_entity_decl():
    e = Tokens(entity_decl.parseString("""  
    ENTITY action;
        name          : label;
        description   : text;
        chosen_method : action_method;
    END_ENTITY; -- action
    """))
    assert str(e) == "ENTITY action ; name : label ; description : text ; chosen_method : action_method ; END_ENTITY ;"


def test_simple_entity_decl_2():
    e = Tokens(entity_decl.parseString("""
    ENTITY IfcActor
        SUPERTYPE OF (ONEOF(IfcOccupant))
        SUBTYPE OF (IfcObject);
            TheActor : IfcActorSelect;
            INVERSE IsActingUpon : SET [0:?] OF IfcRelAssignsToActor FOR RelatingActor;
        END_ENTITY;
    """))
    assert str(e) == "ENTITY IfcActor SUPERTYPE OF ( ONEOF ( IfcOccupant ) ) " \
                     "SUBTYPE OF ( IfcObject ) ; " \
                     "TheActor : IfcActorSelect ; " \
                     "INVERSE IsActingUpon : SET [ 0 : ? ] OF IfcRelAssignsToActor FOR RelatingActor ; " \
                     "END_ENTITY ;"


"""
    ENTITY IfcActorRole;
        Role : IfcRoleEnum;
        UserDefinedRole : OPTIONAL IfcLabel;
        Description : OPTIONAL IfcText;
        INVERSE
            HasExternalReference : SET [0:?] OF IfcExternalReferenceRelationship FOR RelatedResourceObjects;
        WHERE
            WR1 : (Role <> IfcRoleEnum.USERDEFINED) OR
                  ((Role = IfcRoleEnum.USERDEFINED) AND EXISTS(SELF.UserDefinedRole));
    END_ENTITY;
    """


def test_simple_entity_decl_3():
    e = Tokens(entity_decl.parseString("""
    ENTITY IfcActorRole;
        Role : IfcRoleEnum;
        UserDefinedRole : OPTIONAL IfcLabel;
        Description : OPTIONAL IfcText;
        INVERSE
            HasExternalReference : SET [0:?] OF IfcExternalReferenceRelationship FOR RelatedResourceObjects;
        WHERE SELF > 0;
    END_ENTITY;
    """))
    assert len(e) == 38


def test_simple_entity_decl_4():
    e = Tokens(entity_decl.parseString("""
    ENTITY IfcAddress
        ABSTRACT SUPERTYPE OF (ONEOF
            (IfcPostalAddress
            ,IfcTelecomAddress));
        Purpose : OPTIONAL IfcAddressTypeEnum;
        Description : OPTIONAL IfcText;
        UserDefinedPurpose : OPTIONAL IfcLabel;
        INVERSE
            OfPerson : SET [0:?] OF IfcPerson FOR Addresses;
            OfOrganization : SET [0:?] OF IfcOrganization FOR Addresses;
        WHERE
            WR1 : (NOT(EXISTS(Purpose))) OR
                ((Purpose <> IfcAddressTypeEnum.USERDEFINED) OR
                ((Purpose = IfcAddressTypeEnum.USERDEFINED) AND
                EXISTS(SELF.UserDefinedPurpose)));
    END_ENTITY;
    """))
    assert len(e) == 98


def test_simple_entity_decl_5():
    e = Tokens(entity_decl.parseString(r"""
    ENTITY IfcAdvancedBrep
        SUPERTYPE OF (ONEOF
            (IfcAdvancedBrepWithVoids))
        SUBTYPE OF (IfcManifoldSolidBrep);
        WHERE
            HasAdvancedFaces : SIZEOF(QUERY(Afs <* SELF\IfcManifoldSolidBrep.Outer.CfsFaces |
                (NOT ('IFC4X2.IFCADVANCEDFACE' IN TYPEOF(Afs)))
            )) = 0;
    END_ENTITY;
    """))
    assert len(e) == 51


def test_simple_entity_decl_6():
    e = Tokens(entity_decl.parseString(r"""
    ENTITY IfcAdvancedBrepWithVoids
        SUBTYPE OF (IfcAdvancedBrep);
        Voids : SET [1:?] OF IfcClosedShell;
        WHERE
            VoidsHaveAdvancedFaces : SIZEOF (QUERY (Vsh <* Voids |
                SIZEOF (QUERY (Afs <* Vsh.CfsFaces |
                (NOT ('IFC4X2.IFCADVANCEDFACE' IN TYPEOF(Afs)))
                )) = 0
                )) = 0;
    END_ENTITY;
    """))
    assert len(e) == 62


def test_one_of():
    r = Tokens(one_of.parseString("ONEOF(IfcOccupant)"))
    assert str(r) == "ONEOF ( IfcOccupant )"


def test_supertype_rule():
    s = Tokens(supertype_rule.parseString("SUPERTYPE OF (ONEOF(IfcOccupant))"))
    assert str(s) == "SUPERTYPE OF ( ONEOF ( IfcOccupant ) )"


def test_supertype_constraint():
    s = Tokens(supertype_constraint.parseString("SUPERTYPE OF (ONEOF(IfcOccupant))"))
    assert str(s) == "SUPERTYPE OF ( ONEOF ( IfcOccupant ) )"


if __name__ == '__main__':
    pytest.main([__file__])
