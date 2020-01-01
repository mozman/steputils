# Created: 26.12.2019
# Copyright (c) 2019-2020 Manfred Moitzi
# License: MIT License
from base64 import encodebytes
from uuid import uuid4


def guid() -> str:
    """
    Returns a globally unique id as unicode string with a length of
    22 characters according to the IFC standard.
    """
    return encodebytes(uuid4().bytes)[:22].decode()
