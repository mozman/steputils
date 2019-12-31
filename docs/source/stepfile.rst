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

   from steputils.stepfile import Factory

   # load an existing file from file system
   stepfile = Factory.load('example.stp')
   # or create a new STEP-file
   stepfile = Factory.new()
   data = stepfile.new_data_section()
   # Entities are STEP application specific objects and are not checked for correct keywords and
   # parameters, this task belongs to the next application layer.
   data.append(Factory.simple_entity_instance('#1', 'Application', ('MyApp', 'v1.0')))

   # set required header entities
   stepfile.set_file_description(('Example STEP file', 'v1.0'))
   stepfile.set_file_name(name='example.stp', organization=('me', 'myself'), autorization='me')
   stepfile.set_file_schema(('NONE'))

   stepfile.save('example.stp')

Public Interface
----------------

.. autoclass:: Factory

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

   .. automethod:: simple_entity_instance(ref: str, name: str, params) -> SimpleEntityInstance

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

    .. automethod:: __getitem__(name: EntityInstanceName) -> EntityInstance

    .. automethod:: __str__

    .. automethod:: get(name: EntityInstanceName) -> Optional[EntityInstance]

    .. automethod:: new_data_section(self, params: Iterable = None) -> DataSection

    .. automethod:: append(data: DataSection) -> None

    .. automethod:: save

    .. automethod:: write

    .. automethod:: is_unique_reference


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

    .. automethod:: __getitem__(name: EntityInstanceName) -> EntityInstance

    .. automethod:: __iter__

    .. automethod:: get(name: EntityInstanceName) -> Optional[EntityInstance]

    .. automethod:: __len__() -> int

    .. automethod:: names() -> Iterable[EntityInstanceName]

    .. automethod:: append(instance: EntityInstance) -> None

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

    .. attribute:: name

        Instance name as :class:`EntityInstanceName`

    .. attribute:: entity

        Instance entity as :class:`Entity`.

    .. attribute:: is_complex

        Set to ``False``

.. autoclass:: SimpleEntityInstance

    .. attribute:: name

        Instance name as :class:`EntityInstanceName`

    .. attribute:: entities

        Instance entities as list of :class:`Entity` objects.

    .. attribute:: is_complex

        Set to ``True``
