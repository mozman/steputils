.. method signatures added, because sphinx always use fully qualified type hints, which is not very
   pretty nor readable

.. module:: steputils.stepfile

Stepfile
========

STEP physical file representation (STEP-file) specified by the ISO 10303-21 standard.

STEP-File is data exchange form of STEP. ISO 10303 can represent 3D objects in Computer-aided
design (CAD) and related information. Due to its ASCII structure, a STEP-file is easy to read, with typically one
instance per line. The format of a STEP-File is defined in ISO 10303-21 Clear Text Encoding of the Exchange Structure.

ISO 10303-21 defines the encoding mechanism for representing data conforming to a particular schema in the
EXPRESS data modeling language specified in ISO 10303-11. A STEP-File is also called p21-File and STEP Physical
File. The file extensions .stp and .step indicate that the file contains data conforming to STEP Application
Protocols while the extension .p21 should be used for all other purposes.

Source: https://en.wikipedia.org/wiki/ISO_10303-21

The intended usage is to import the :class:`Factory` class and create new objects by factory functions:

.. code-block:: python

   from steputils.stepfile import Factory as sf  # (S)TEP-file (F)actory
   from pyparsing import ParseException

   FNAME = "example.p21"

   # Create a new STEP-file:
   stepfile = sf.new()

   # Create a new data section:
   data = stepfile.new_data_section()

   # Add entity instances to data section:
   data.add(sf.simple_instance('#1', name='APPLICATION', params=('MyApp', 'v1.0')))

   # Set required header entities:
   stepfile.header.set_file_description(('Example STEP file', 'v1.0'))
   stepfile.header.set_file_name(name=FNAME, organization=('me', 'myself'), autorization='me')
   stepfile.header.set_file_schema(('NONE',))

   # Write STEP-file to file system:
   stepfile.save(FNAME)

   # Read an existing file from file system:
   try:
       stepfile = sf.readfile(FNAME)
   except IOError as e:
       print(str(e))
   except ParseException as e:
       # Invalid STEP-file
       print(str(e))
   else:
       print(f'File {FNAME} is a valid STEP-file')

Public Interface
----------------

.. autoclass:: Factory

   .. automethod:: readfile(filename: str) -> StepFile

   .. automethod:: load(fp: TextIO) -> StepFile

   .. automethod:: loads(s: str) -> StepFile

   .. automethod:: new() -> StepFile

   .. automethod:: keyword(name: str) -> Keyword

   .. automethod:: reference(ref: str) -> EntityInstanceName

   .. automethod:: enum(enum: str) -> Enumeration

   .. automethod:: binary(value: int, unset: int = 0) -> Binary

   .. automethod:: unset_parameter(char: str) -> UnsetParameter

   .. automethod:: parameter_list(*args) -> ParameterList

   .. automethod:: typed_parameter(type_name: str, param) -> TypedParameter

   .. automethod:: entity(name: str, params) -> Entity

   .. automethod:: simple_instance(ref: str, name: str, params) -> SimpleEntityInstance

   .. automethod:: simple_entity_instance(ref: str, entity:Entity) -> SimpleEntityInstance

   .. automethod:: complex_entity_instance(ref: str, entities: List[Entity]) -> ComplexEntityInstance

   .. automethod:: timestamp

   .. automethod:: is_string

   .. automethod:: is_integer

   .. automethod:: is_real

   .. automethod:: is_binary

   .. automethod:: is_reference

   .. automethod:: is_keyword

   .. automethod:: is_enum

   .. automethod:: is_unset_parameter

   .. automethod:: is_typed_parameter

   .. automethod:: is_parameter_list

      Note: It is a single parameter if it's not a :class:`ParameterList`

   .. automethod:: is_entity

   .. automethod:: is_simple_entity_instance

   .. automethod:: is_complex_entity_instance



Classes
-------

StepFile
~~~~~~~~

.. autoclass:: StepFile

    .. attribute:: header

        Header section as :class:`HeaderSection` object.

    .. attribute:: data

        List of data sections as :class:`DataSection` objects

    .. automethod:: __getitem__(ref: EntityInstanceName) -> EntityInstance

    .. automethod:: __iter__() -> Iterable[EntityInstance]

    .. automethod:: __len__

    .. automethod:: __str__

    .. automethod:: get(ref: EntityInstanceName) -> Optional[EntityInstance]

    .. automethod:: new_data_section(params: Iterable = None) -> DataSection

    .. automethod:: append(data: DataSection) -> None

    .. automethod:: save

    .. automethod:: write

    .. automethod:: has_reference


HeaderSection
~~~~~~~~~~~~~

.. autoclass:: HeaderSection

    .. attribute:: entities

        Ordered dict of all header entities as :class:`Entity` objects.

    .. automethod:: __getitem__(name: str) -> Entity

    .. automethod:: get(name: str) -> Optional[Entity]

    .. automethod:: add(self, entity: Entity) -> None

    .. automethod:: set_file_description(description: Tuple = None, level: str = '2;1') -> None

    .. automethod:: set_file_name(name: str, time_stamp: str = None, author: str = '', organization: Tuple = None, preprocessor_version: Tuple = None, organization_system: str = '', autorization: str = '') -> None

    .. automethod:: set_file_schema(schema: Tuple) -> None



DataSection
~~~~~~~~~~~

.. autoclass:: DataSection

    .. attribute:: parameter

        Each data section can have associated parameters stored in attribute :attr:`parameter`.

    .. attribute:: instances

        Ordered dict of all entity instances of this data section. Key is the name of instance as a string
        (e.g. ``'#100'``), values are :class:`EntityInstance` objects.

    .. automethod:: __getitem__(ref: str) -> EntityInstance

    .. automethod:: __iter__

    .. automethod:: get(ref: str) -> Optional[EntityInstance]

    .. automethod:: __len__() -> int

    .. automethod:: references() -> Iterable[EntityInstanceName]

    .. automethod:: add(instance: EntityInstance) -> None

Helper Classes
~~~~~~~~~~~~~~

.. autoclass:: ParameterList

.. autoclass:: EntityInstanceName

.. autoclass:: Keyword

.. autoclass:: Enumeration

.. autoclass:: Binary

    .. attribute:: value

        Value as ``int``.

    .. attribute:: unset

        Count of unset bits in the range from 0 to 3.

.. autoclass:: UnsetParameter

.. autoclass:: TypedParameter

    .. attribute:: type_name

        Type name as :class:`Keyword`

    .. attribute:: param

.. autoclass:: Entity

    .. attribute:: name

        Entity name as :class:`Keyword`

    .. attribute:: params

        Entity parameters as :class:`ParameterList`.

.. autoclass:: SimpleEntityInstance

    .. attribute:: ref

        Instance name as :class:`EntityInstanceName`

    .. attribute:: entity

        Instance entity as :class:`Entity`.

.. autoclass:: ComplexEntityInstance

    .. attribute:: ref

        Instance name as :class:`EntityInstanceName`

    .. attribute:: entities

        Instance entities as list of :class:`Entity` objects.
