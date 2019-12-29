# Created: 28.12.2019
# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
import pytest
from steputils.stepfile import loads, is_reference, is_unset_parameter, is_typed_parameter, is_enum

STEP_FILE = r"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView, SpaceBoundary2ndLevelAddOnView, QuantityTakeOffAddOnView]','Option [Filter: ]'),'2;1');
FILE_NAME('S:\\[IFC]\\[COMPLETE-BUILDINGS]\\xyz.ifc','2011-01-17T09:42:14',('Architect'),('Building Designer Office'),'PreProc - EDM 5.0','ArchiCAD 14.00 Release 1. Windows Build Number of the Ifc 2x3 interface: 3427','The authorising person');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;

DATA;
#8= IFCORGANIZATION('','Nicht definiert','',$,$);
#10= IFCORGANIZATION('GS','Graphisoft','Graphisoft',$,$);
#5= IFCAPPLICATION(#10,'14.0','ArchiCAD 14.0','ArchiCAD');
#6= IFCPERSON('','Nicht definiert','',$,$,$,$,$);

ENDSEC;

END-ISO-10303-21;
"""


@pytest.fixture(scope='module')
def stpfile():
    return loads(STEP_FILE)


def test_header(stpfile):
    assert stpfile.header['FILE_DESCRIPTION'].params[0][
               0] == 'ViewDefinition [CoordinationView, SpaceBoundary2ndLevelAddOnView, QuantityTakeOffAddOnView]'
    assert stpfile.header['FILE_DESCRIPTION'].params[0][1] == 'Option [Filter: ]'
    assert stpfile.header['FILE_DESCRIPTION'].params[1] == '2;1'
    assert stpfile.header['FILE_NAME'].params[0] == 'S:\\[IFC]\\[COMPLETE-BUILDINGS]\\xyz.ifc'
    assert stpfile.header['FILE_SCHEMA'].params[0] == ('IFC2X3',)


def test_data_section(stpfile):
    data = stpfile.data[0]
    instance = data['#5']
    assert instance.name == '#5'
    assert instance.entity.name == 'IFCAPPLICATION'
    assert instance.entity.params == ('#10', '14.0', 'ArchiCAD 14.0', 'ArchiCAD')

    ref = instance.entity.params[0]
    assert is_reference(ref)
    instance2 = stpfile[ref]
    assert instance2.name == ref
    assert instance2.entity.name == 'IFCORGANIZATION'
    assert instance2.entity.params == ('GS', 'Graphisoft', 'Graphisoft', '$', '$')
    assert is_unset_parameter(instance2.entity.params[3]) is True


def test_data_order(stpfile):
    data = stpfile.data[0]
    assert list(data.names()) == ['#8', '#10', '#5', '#6']
    assert data.sorted_names() == ['#5', '#6', '#8', '#10']


# contains comments
# typed parameter
# complex entity instances

COMPLEX_FILE = r"""ISO-10303-21;
HEADER;

FILE_DESCRIPTION(('CATIA V5 STEP'),'2;1');

FILE_NAME('E:\\Public\\Archive_PDES\\TR22\\NativeFiles\\s1\\s1-c5-214.stp','2008-08-18T12:41:46+00:00',('none'),('none'),'CATIA Version 5 Release 19 SP 1 (IN-PROTO)','CATIA V5 STEP AP214','none');

FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));

ENDSEC;
/* file written by CATIA V5R19 */
DATA;
#5=PRODUCT('*MASTER','*MASTER',' ',(#2)) ;
#1=APPLICATION_CONTEXT('automotive design') ;
#175=CARTESIAN_POINT('NONE',(0.,0.,0.)) ;
#176=CARTESIAN_POINT('NONE',(0.,1.43622047244,-0.00905511811024)) ;
#193=CARTESIAN_POINT('NONE',(0.,0.,0.)) ;
#194=CARTESIAN_POINT('NONE',(0.,-1.43622047244,-0.00905511811024)) ;
#57=DIRECTION('NONE',(0.0393700787402,0.,0.)) ;
#58=DIRECTION('NONE',(0.,0.,0.0393700787402)) ;
#59=DIRECTION('NONE',(0.0393700787402,0.,0.)) ;
#24=UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(0.000196850393701),#23,'distance_accuracy_value','CONFUSED CURVE UNCERTAINTY') ;
#17=(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.)) ;
ENDSEC;
END-ISO-10303-21;
"""


@pytest.fixture(scope='module')
def complex_file():
    return loads(COMPLEX_FILE)


def test_typed_parameter(complex_file):
    instance = complex_file['#24']
    assert instance.entity.name == "UNCERTAINTY_MEASURE_WITH_UNIT"
    typed_param = instance.entity.params[0]
    assert is_typed_parameter(typed_param) is True
    assert typed_param.type_name == "LENGTH_MEASURE"
    assert typed_param.param == 0.000196850393701


def test_complex_instance(complex_file):
    instance = complex_file['#17']
    assert instance.is_complex is True
    entities = instance.entities
    assert len(entities) == 3
    assert entities[0].name == "LENGTH_UNIT"
    assert len(entities[0].params) == 0
    assert entities[1].name == "NAMED_UNIT"
    assert entities[1].params[0] == "*"
    assert is_unset_parameter(entities[1].params[0])
    assert entities[2].name == "SI_UNIT"
    assert entities[2].params == ('.MILLI.', '.METRE.')
    assert is_enum(entities[2].params[0]) is True


if __name__ == '__main__':
    pytest.main([__file__])
