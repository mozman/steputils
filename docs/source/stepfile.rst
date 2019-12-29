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

Functions
---------

.. autofunction:: load(fp: TextIO) -> StepFile

.. autofunction:: loads(s: str) -> StepFile

.. autofunction:: dump(data: StepFile, fp: TextIO) -> None

.. autofunction:: dumps(data: StepFile) -> str

Checking for Types
~~~~~~~~~~~~~~~~~~

.. autofunction:: is_string

.. autofunction:: is_integer

.. autofunction:: is_real

.. autofunction:: is_reference

.. autofunction:: is_keyword

.. autofunction:: is_enum

.. autofunction:: is_unset_parameter

.. autofunction:: is_typed_parameter

.. autofunction:: is_parameter_list

   Note: It is a single parameter if it's not a :class:`ParameterList`

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

    .. automethod:: get(name: EntityInstanceName) -> Optional[EntityInstance]

    .. automethod:: append(data: DataSection) -> None

    .. automethod:: append


HeaderSection
~~~~~~~~~~~~~

.. autoclass:: HeaderSection

    .. attribute:: entities

        Ordered dict of all header entities as :class:`Entity` objects.

    .. automethod:: append(entity: Entity) -> None

    .. automethod:: __getitem__(name: str) -> Entity

    .. automethod:: get(name: str) -> Optional[Entity]

DataSection
~~~~~~~~~~~

.. autoclass:: DataSection

    .. attribute:: parameter

        Each data section can have associated parameters stored in attribute :attr:`parameter`.

    .. attribute:: instances

        Ordered dict of all entity instances of this data section. Key is the name of instance as a string
        (e.g. ``'#100'``), values are :class:`EntityInstance` objects.

    .. automethod:: __getitem__(name: EntityInstanceName) -> EntityInstance

    .. automethod:: get(name: EntityInstanceName) -> Optional[EntityInstance]

    .. automethod:: __len__() -> int

    .. automethod:: names() -> Iterable[EntityInstanceName]

    .. automethod:: sorted_names() -> List[EntityInstanceName]

    .. automethod:: instances() -> Iterable[EntityInstance]

    .. automethod:: sorted_instances() -> Iterable[EntityInstance]

    .. automethod:: append(instance: EntityInstance) -> None

Helper Classes
~~~~~~~~~~~~~~

.. autoclass:: ParameterList

.. autoclass:: EntityInstanceName

.. autoclass:: Keyword

.. autoclass:: Enumeration

.. autoclass:: UnsetParameter

.. autoclass:: TypedParameter

    .. attribute:: type_name

    .. attribute:: param
