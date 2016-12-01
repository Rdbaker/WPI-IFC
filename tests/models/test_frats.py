# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest

from ifc.constants import fraternityList
from ifc.models import Fraternity


@pytest.mark.usefixtures('db')
class TestFrat:
    """Fraternity tests."""
    @pytest.mark.parametrize('frat_title', fraternityList)
    def test_title_validation_no_errors(self, frat_title):
        assert Fraternity(title=frat_title, capacity=100)

    def test_title_validation_errors(self):
        with pytest.raises(AssertionError):
            Fraternity(title='Sigma Nu', capacity=10)
