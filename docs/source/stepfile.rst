.. method signatures added, because sphinx always use fully qualified type hints, which is not very
   pretty nor readable

.. module:: steputils.stepfile

Stepfile
========

Functions
---------

.. autofunction:: load(fp: TextIO) -> StepFile

.. autofunction:: loads(s: str) -> StepFile

.. autofunction:: dump(data: StepFile, fp: TextIO) -> None

.. autofunction:: dumps(data: StepFile) -> str

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
