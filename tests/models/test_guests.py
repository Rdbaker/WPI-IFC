# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest
from sqlalchemy.exc import IntegrityError

from ifc.models import Guest
from ifc.utils import InvalidAPIUsage


@pytest.mark.usefixtures('db')
class TestGuest:
    """Guest tests."""
    def test_name_unique_on_party(self, party, guest):
        with pytest.raises(IntegrityError):
            Guest.create(name=guest.name, host=guest.host, party=party,
                         is_male=True)

    @pytest.mark.parametrize('guest_name', ['', 'a', 'aa'])
    def test_name_cannot_be_too_short(self, guest_name, user, party):
        with pytest.raises(InvalidAPIUsage):
            Guest.create(name=guest_name, host=user, party=party)
