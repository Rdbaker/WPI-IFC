# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest

from ifc.models import Capacity


@pytest.mark.usefixtures('db')
class TestCap:
    """Capacity tests."""

    def test_validation_no_errors(self, capacity):
        """Test that there are no validation errors."""
        assert Capacity(male_max=capacity.male_max,
                        female_max=capacity.female_max)
