# Created: 26.12.2019
# Copyright (c) 2019 Manfred Moitzi
# License: MIT License

import pytest
from ifc4data.stepfile import step_file, header_entity, list_

SHORT_STEP_FILE = r"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView, SpaceBoundary2ndLevelAddOnView, QuantityTakeOffAddOnView]','Option [Filter: ]'),'2;1');
FILE_NAME('S:\\[IFC]\\[COMPLETE-BUILDINGS]\\^yz.ifc','2011-01-17T09:42:14',('Architect'),('Building Designer Office'),'PreProc - EDM 5.0','ArchiCAD 14.00 Release 1. Windows Build Number of the Ifc 2x3 interface: 3427','The authorising person');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;

DATA;
#1= IFCORGANIZATION('GS','Graphisoft','Graphisoft',$,$);
#5= IFCAPPLICATION(#1,'14.0','ArchiCAD 14.0','ArchiCAD');
#6= IFCPERSON('','Nicht definiert','',$,$,$,$,$);
#8= IFCORGANIZATION('','Nicht definiert','',$,$);
ENDSEC;

END-ISO-10303-21;
"""


def test_short_step_file():
    result = list(step_file.parseString(SHORT_STEP_FILE))
    assert len(result) > 0


def test_header_entity():
    result = list(header_entity.parseString("FILE_SCHEMA(('IFC2X3'));"))
    assert result == ['FILE_SCHEMA', (('IFC2X3',),), ';']


def test_empty_list():
    result = list(list_.parseString("()"))
    assert result == [tuple()]  # empty tuple


def test_empty_list_1():
    result = list(list_.parseString("('IFC2X3')"))
    assert result[0] == ('IFC2X3', )


if __name__ == '__main__':
    pytest.main([__file__])
