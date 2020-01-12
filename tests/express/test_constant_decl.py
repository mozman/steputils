# Copyright (c) 2020 Manfred Moitzi
# License: MIT License

import pytest
from steputils.express.parser import constant_decl, Tokens


def test_typedef_real():
    c = Tokens(constant_decl.parseString("""
    CONSTANT
    dummy_gri : geometric_representation_item := representation_item('') ||
                geometric_representation_item();
    dummy_tri : topological_representation_item := representation_item('')
                || topological_representation_item();
    END_CONSTANT;
    """))

    assert str(c) == "CONSTANT dummy_gri : geometric_representation_item := representation_item (  ) || " \
                     "geometric_representation_item ( ) ; " \
                     "dummy_tri : topological_representation_item := representation_item (  ) || " \
                     "topological_representation_item ( ) ; " \
                     "END_CONSTANT ;"


if __name__ == '__main__':
    pytest.main([__file__])
