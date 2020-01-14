# Copyright (c) 2020 Manfred Moitzi
# License: MIT License
import pytest
from steputils.express import Parser


def test_schema():
    parser = Parser("""
    SCHEMA test;
    END_SCHEMA;
    """)
    tree = parser.schema()
    assert tree is not None


def test_type_decl():
    parser = Parser("""
    SCHEMA test;
    
    TYPE test = REAL;
    END_TYPE;
    
    TYPE day_in_week_number = INTEGER;
    WHERE 1 <= SELF;
    END_TYPE; -- day_in_week_number

    END_SCHEMA;
    """)
    tree = parser.schema()
    assert tree is not None


def test_function():
    parser = Parser("""
    SCHEMA test;
    
    FUNCTION IfcConsecutiveSegments
    (Segments : LIST [1:?] OF IfcSegmentIndexSelect)
      : BOOLEAN;
    
     LOCAL
      Result : BOOLEAN := TRUE;
     END_LOCAL;
    
      REPEAT i := 1 TO (HIINDEX(Segments)-1);
        IF Segments[i][HIINDEX(Segments[i])] <> Segments[i+1][1] THEN
          BEGIN
            Result := FALSE;
            ESCAPE;
          END;
        END_IF;
      END_REPEAT;
    
      RETURN (Result);
    END_FUNCTION;
    
    END_SCHEMA;
    """)
    tree = parser.schema()
    assert tree is not None


if __name__ == '__main__':
    pytest.main([__file__])
