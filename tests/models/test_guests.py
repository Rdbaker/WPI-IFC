# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest

from ifc.models import Guest


@pytest.mark.usefixtures('db')
class TestGuest:
    """Guest tests."""
    def test_name_unique_on_party(self, party, guest):
        with pytest.raises(AssertionError):
            Guest.create(name=guest.name, host=guest.host, party=party)

    @pytest.mark.parametrize('guest_name', ['', 'a', 'aa', 'aaa'])
    def test_name_cannot_be_too_short(self, guest_name, user, party):
        with pytest.raises(AssertionError):
            Guest.create(name=guest_name, host=user, party=party)
